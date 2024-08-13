from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import cv2
import mediapipe as mp
import numpy as np
import csv
import os
import glob
import pickle
import time
import math
import threading

app=FastAPI()
origins=["http://localhost:5173",]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mpd=mp.solutions.drawing_utils
mpp=mp.solutions.pose
state=0
knee_g=1
knee_b=1
cap=None
lock=threading.Lock()
text=""

with open('svm_classifier_knee.pkl', 'rb') as model_file:
    loaded_model_knee = pickle.load(model_file)

with open('scaler_knee.pkl', 'rb') as scaler_file:
    loaded_scaler_knee = pickle.load(scaler_file)

with open('svm_classifier.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

with open('scaler.pkl', 'rb') as scaler_file:
    loaded_scaler = pickle.load(scaler_file)

with open('svm_classifier_leg_swing.pkl', 'rb') as model_file:
    loaded_model_legs = pickle.load(model_file)

with open('scaler_leg_swing.pkl', 'rb') as scaler_file:
    loaded_scaler_legs = pickle.load(scaler_file)

def calculate_angle(points):
    x1, y1, x2, y2, x3, y3 = points
    vector1 = (x1 - x2, y1 - y2)
    vector2 = (x3 - x2, y3 - y2)
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    angle_radians = math.acos(dot_product / (magnitude1 * magnitude2))
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def state0(results):
    a=[None]*6
    knee_a=[None]*6
    c=[12,24,26]
    knee_c=[24,26,28]
    b=0;
    inp=[None]*1
    knee_inp=[None]*1
    for i in range(len(c)):
        try:
            a[2*i]=results.pose_landmarks.landmark[c[i]].x
            a[2*i+1]=results.pose_landmarks.landmark[c[i]].y
            knee_a[2*i]=results.pose_landmarks.landmark[c[i]].x
            knee_a[2*i+1]=results.pose_landmarks.landmark[c[i]].y
        except:
            b+=1;
    if b==0:
        inp[0]=calculate_angle(a[:6])
        knee_inp[0]=calculate_angle(knee_a[:6])
        s1=np.array(inp).reshape(1,-1)
        sc1=loaded_scaler.transform(s1)
        res= loaded_model.predict(sc1)
        if res[0]!="Correct":
            return res[0]
        s2=np.array(knee_inp).reshape(1,-1)
        sc2=loaded_scaler_knee.transform(s2)
        knee_res=loaded_model_knee.predict(sc2)
        if knee_res[0]!="Correct":
            return knee_res[0]
        return "Correct Stance"
    return "Position the camera such that your entire body is visible"

def state1(results):
    #print("state1")
    import time
    a=[None]*6
    c=[24,26,28]
    b=0;
    res=[""]
    inp=[None]
    global knee_b
    global knee_g
    for i in range(len(c)):
        try:
            a[2*i]=results.pose_landmarks.landmark[c[i]].x
            a[2*i+1]=results.pose_landmarks.landmark[c[i]].y
        except:
            b+=1;
    if b==0:
        inp[0]=calculate_angle(a)
        s1=np.array(inp).reshape(1,-1)
        sc1=loaded_scaler_legs.transform(s1)
        res= loaded_model_legs.predict(sc1)
        text=res[0]
        if text=="Correct":
            knee_g+=1
        else:
            knee_b+=1

def start_capture():
    global cap
    if cap is not None and cap.isOpened():
        return
    cap=cv2.VideoCapture(0)

def stop_capture():
    global cap
    global text
    global state
    global knee_g
    global knee_b
    if cap is not None:
        cap.release()
        cap=None
        text=""
        state=0
        knee_g=1
        knee_b=1

def main():
    global cap
    global mpd
    global mpp
    global state
    global text
    global knee_b
    global knee_g
    
    #cap=cv2.VideoCapture(0)
    #cap=cv2.VideoCapture("Tiger_back_swing.mp4")
    text=""
    time1=time.time()
    time2=time.time()

    with mpp.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
        while True:
            b=0;
            ret, frame=cap.read()
            if not ret:
                break
            image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable=False
            results=pose.process(image)
            image.flags.writeable=True
            image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
            mpd.draw_landmarks(image, results.pose_landmarks, mpp.POSE_CONNECTIONS)
            position = (10, 30)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            color = (0, 0, 0)
            thickness = 2
            if state==0:
                text=state0(results)
                time2=time.time()
                if text!="Correct Stance":
                    time1=time.time()
                if time2-time1>=4:
                    state=0.5
                #cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
            elif state == 0.5:
                try:
                    T1=results.pose_landmarks.landmark[16].y
                    T2=results.pose_landmarks.landmark[24].y
                    if (T1<=T2):
                        state = 1
                except:
                    pass
                    #print("error")               
            elif state == 1:
                state1(results)
                try:
                    T1=results.pose_landmarks.landmark[16].y
                    T2=results.pose_landmarks.landmark[24].y
                    if(T1>=T2):
                        state = 1.5
                        #print("hello")
                    #print(T1,T3)
                except:
                    pass    
            elif state==1.5:
                if knee_g>=knee_b:
                    text="Correct"
                else:
                    text="Bend knees correctly"
                #position2=(10,30)
                #cv2.putText(image, text2, position2, font, font_scale, color, thickness, cv2.LINE_AA)
                state=2
                time1=time.time()
                time2=time.time()
            elif state==2:
                #position2=(10,30)
                #cv2.putText(image, text2, position2, font, font_scale, color, thickness, cv2.LINE_AA)
                knee_g=1
                knee_b=1
                time2=time.time()
                if(time2-time1>=6):
                    state=0
                    time1=time.time()
                    time2=time.time()
            cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
            #cv2.imshow("Mediapipe Feed", image)
            temp_12, buff=cv2.imencode('.jpg',image)
            snd=buff.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + snd + b'\r\n')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        #cap.release()
        #cv2.destroyAllWindows()
        if cap!=None:
            cap=None
            text=""
            state=0
            knee_g=1
            knee_b=1

@app.get("/start_feed")
def start_feed():
    with lock:
        start_capture()
    return {"status":"video feed started"}

@app.get("/stop_feed")
def stop_feed():
    with lock:
        stop_capture()
    return {"status":"video feed stopped"}

@app.get('/get_feed')
def fed():
    global cap
    if cap==None or not cap.isOpened():
        return {"status":"feed must be started"}
    else:
        return StreamingResponse(main(),
                    media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/feedback')
def feedback():
    return {"status":"->"+text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=5001)