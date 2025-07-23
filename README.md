# Golf-Swing-and-Stance-Analysis-Using-Supervised-Learning

A real-time golf swing and stance analysis tool built using **MediaPipe** and **computer vision**, designed to help golfers correct poor posture and improve their swing technique.

We combine human pose estimation with machine learning (SVM classifiers) to detect improper movements and offer real-time feedback during a swing.

---

## Project Highlights

- **Real-Time Pose Estimation** using [MediaPipe](https://github.com/google/mediapipe)
- **Golf-Specific Pose Detection** (stance, back angle, arm alignment, rotation)
- **Support Vector Machines (SVMs)** trained on custom-labeled swing data
- **Feedback System** to detect and correct:
  - Poor stance
  - Incomplete backswing
  - Incorrect follow-through
  - Unbalanced weight shift
- **Custom Dataset** of golf poses:  
  [Golf Pose Dataset on Kaggle](https://www.kaggle.com/datasets/rakshitgirish/golf-pose)

---

## Dataset

We created and annotated our own dataset of golf swings and postures:

**Kaggle Link:** [Golf Pose Dataset](https://www.kaggle.com/datasets/rakshitgirish/golf-pose)

The dataset includes:
- Frame-wise joint locations from MediaPipe
- Swing phase annotations
- Posture quality labels (good/bad)
- Videos and frame sequences

---

## Tech Stack

- **Language:** Python
- **Pose Estimation:** [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose.html)
- **Model:** Scikit-learn's SVM Classifier
- **Visualization:** OpenCV
- **Data Handling:** NumPy

---

Requirements: Python version 3.11+ and Node.js version 20.15+

Run the python programs in the Front_view_FastAPI and Back_view_FastAPI folders (Install requirements in the same folder)
Run the Vite APP using the the "npm install" and "npm run dev" commands. Follow the link
