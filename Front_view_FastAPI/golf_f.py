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
import math
import time
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
fsw_g=1
fsw_b=1
bsw_g=1
bsw_b=1
cap=None
lock=threading.Lock()
text=""

with open('backswing_classifier.pkl', 'rb') as model_file:
    backswing_model = pickle.load(model_file)
with open('backswing_scaler.pkl', 'rb') as scaler_file:
    backswing_scaler = pickle.load(scaler_file)
with open('ball_position_classifier.pkl', 'rb') as model_file:
    ball_position_model = pickle.load(model_file)
with open('ball_position_scaler.pkl', 'rb') as scaler_file:
    ball_position_scaler = pickle.load(scaler_file)
with open('leg_width_classifier.pkl', 'rb') as model_file:
    leg_width_model = pickle.load(model_file)
with open('leg_width_scaler.pkl', 'rb') as scaler_file:
    leg_width_scaler = pickle.load(scaler_file)
with open('frontswing_classifier.pkl', 'rb') as model_file:
    frontswing_model = pickle.load(model_file)
with open('frontswing_scaler.pkl', 'rb') as scaler_file:
    frontswing_scaler = pickle.load(scaler_file)

def calculate_angle(points):
    x1, y1, x2, y2, x3, y3 = points
    v1 = (x1 - x2, y1 - y2)
    v2 = (x3 - x2, y3 - y2)
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    magnitude_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    magnitude_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    angle_radians = math.acos(dot_product / (magnitude_v1 * magnitude_v2))
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def calculate_ratio(points):
    x1, y1, x2, y2, x3, y3, x4, y4=points
    distance1=math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    distance2=math.sqrt((x4 - x3)**2 + (y4 - y3)**2)
    if distance2==0:
        distance2=distance1+0.001
    ratio=distance1/distance2
    return ratio

def state0(results):
    a=[None]*20
    c=[11,13,15,15,11,23,11,12,27,28]
    b=0
    for i in range(len(c)):
        try:
            a[2*i]=results.pose_landmarks.landmark[c[i]].x
            a[2*i+1]=results.pose_landmarks.landmark[c[i]].y
        except:
            b+=1;
    if b==0:
        d1=calculate_angle(a[:6])
        s1=np.array(d1).reshape(1,-1)
        sc1=backswing_scaler.transform(s1)
        res= backswing_model.predict(sc1)
        if res[0]!="Correct":
            return("Straighten out your elbows")
        d2=calculate_angle(a[6:12])
        s2=np.array(d2).reshape(1,-1)
        sc2=ball_position_scaler.transform(s2)
        res=ball_position_model.predict(sc2)
        if res[0]!="Correct":
            return(res[0])
        d3=calculate_ratio(a[12:])
        s3=np.array(d3).reshape(1,-1)
        sc3=leg_width_scaler.transform(s3)
        res= leg_width_model.predict(sc3)
        if res[0]!="Correct":
            return(res[0])
        return("Correct Stance")
    return ("Ensure entire body is visible to the camera")

def state2(results):
    a=[None]*6
    c=[11,13,15]
    b=0
    global bsw_g
    global bsw_b
    for i in range(len(c)):
        try:
            a[2*i]=results.pose_landmarks.landmark[c[i]].x
            a[2*i+1]=results.pose_landmarks.landmark[c[i]].y
        except:
            b+=1;
    if b==0:
        d1=calculate_angle(a[:6])
        s1=np.array(d1).reshape(1,-1)
        sc1=backswing_scaler.transform(s1)
        res= backswing_model.predict(sc1)
        if res[0]!="Correct":
            bsw_b+=1
        else:
            bsw_g+=1
    try:
        t1=results.pose_landmarks.landmark[11].y
        t2=results.pose_landmarks.landmark[23].y
        t3=results.pose_landmarks.landmark[15].y
        t1+=(t2-t1)*0.25
        if t3<=t1:
            return 1
    except:
        pass
    return 0

def state4(results):
    a=[None]*6
    c=[11,13,15]
    b=0
    global fsw_g
    global fsw_b
    for i in range(len(c)):
        try:
            a[2*i]=results.pose_landmarks.landmark[c[i]].x
            a[2*i+1]=results.pose_landmarks.landmark[c[i]].y
        except:
            b+=1;
    if b==0:
        d1=calculate_angle(a[:6])
        s1=np.array(d1).reshape(1,-1)
        sc1=frontswing_scaler.transform(s1)
        res=frontswing_model.predict(sc1)
        if res[0]!="Correct":
            fsw_b+=1
        else:
            fsw_g+=1
    try:
        t1=results.pose_landmarks.landmark[11].x
        t3=results.pose_landmarks.landmark[15].x
        if t3>=t1:
            return 5
    except:
        pass
    return 4

def start_capture():
    global cap
    if cap is not None and cap.isOpened():
        return
    cap=cv2.VideoCapture(0)

def stop_capture():
    global cap
    global text
    global state
    global fsw_g
    global fsw_b
    global bsw_g
    global bsw_b
    if cap is not None:
        cap.release()
        cap=None
        text=""
        state=0
        fsw_g=1
        fsw_b=1
        bsw_g=1
        bsw_b=1

def main():
    global cap
    global mpd
    global mpp
    global state
    global fsw_b
    global fsw_g
    global bsw_b
    global bsw_g
    global text
    
    text=""
    backswing_text=""
    time1=time.time()
    time2=time.time()
    hands1=0
    hands2=0

    with mpp.Pose(min_detection_confidence=0.9, min_tracking_confidence=0.9) as pose:
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
            if state==0:
                text=state0(results)
                time2=time.time()
                if text!="Correct Stance":
                    time1=time.time()
                if time2-time1>=4:
                    state=1
                    hands1=results.pose_landmarks.landmark[15].x
            elif state==1:
                try:
                    hands2=results.pose_landmarks.landmark[15].x
                    if(abs(hands2-hands1)>0.01):
                        state=2
                        text=""
                except:
                    pass
            elif state==2:
                text=""
                state+=state2(results)
            elif state==3:
                text="inter"
                try:
                    t2=results.pose_landmarks.landmark[23].y
                    t3=results.pose_landmarks.landmark[15].y
                    if t3>=t2:
                        state=4
                except:
                    pass
            elif state==4:
                text=""
                state=state4(results)
            elif state==5:
                if fsw_g/fsw_b>=0.7 and bsw_g/bsw_b>=1:
                    text="Correct swing"
                elif fsw_g/fsw_b<0.7 and bsw_g/bsw_b<1:
                    text="Straignten out arms for front and backswings"
                elif fsw_g/fsw_b<0.7:
                    text="Straighten out arms for frontswing"
                else:
                    text="Straignten out arms for backswing"
                state=6
                time1=time.time()
                time2=time.time()
            else:
                fsw_b=1
                fsw_g=1
                bsw_g=1
                bsw_b=1
                time2=time.time()
                if(time2-time1)>=6:
                    state=0
            position = (10, 30)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            color = (255, 255, 255)
            thickness = 2
            cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
            #cv2.imshow("Mediapipe Feed", image)
            temp_12, buff=cv2.imencode('.jpg',image)
            snd=buff.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + snd + b'\r\n')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # if cap.isOpened():
            # cap.release()
            # cap=None
        #cv2.destroyAllWindows()
        if cap!=None:
            cap=None
            text=""
            state=0
            fsw_g=1
            fsw_b=1
            bsw_g=1
            bsw_b=1

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
    uvicorn.run(app,host="127.0.0.1",port=5000)