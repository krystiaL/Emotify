# Emotify
### Tune in your emotion 😄😭😱😡😌, tune out your playlist 📀
*An automated playlist generation system based on an identified facial emotion.*

## Project Overview
As a team of four music enthusiast, this application was created to personalize music selection based on the emotional responses.<br/>


This application is a **Multimodal Emotion Recognition and Playlist Generation System** that is built with a comprehensive machine learning pipeline that incorporates:
   1. **Facial Expression Analysis** 
        - A pipeline for detecting and interpreting emotional cues from facial movements. 
   2. **Music labeling Function** 
        - A pipeline that uses music metadata to label emotion scores and dominant emotion of each song in a music dataset.
   3. **External data integration**
        - Use of Spotify API for playlist generation. 

## Demo 

[Link](https://www.canva.com/design/DAF-UIQAC9E/2Arrd_L3-KkWw7DI3VfYWg/view?utm_content=DAF-UIQAC9E&utm_campaign=share_your_design&utm_medium=link&utm_source=shareyourdesignpanel) to Demo Slides

## Table of Contents
- [Application Features](#application-features)
- [Package Summary](#package-summary)
- [Dependencies](#dependecies)
- [Getting Started](#setting-up-the-project)
- [System Pipelines](#system-pipelines)
  
<br/><br/>
## Application Features
  - **Sidebar FAQs**: contains instruction on application usage, reset, and other interesting facts.
  - **2 input modes**: <br/>
    📸 Real time camera capture using device webcam. <br/>
    📥 Image Upload for a specific face image.
  - **Embedded playlist**: You can play songs from the spotify embedding or get redirected to your Spotify library.

## Package Summary
- **face_detect_module**: Contains model files and module for image preprocess and emotion prediction. 
- **interface**: 
- notebooks
- playlist_module
- raw_data
- tests
- app.py
- requirements.txt

## Dependencies
- TensorFlow
- Spotipy
- OpenCV
- mediapipe
- scikit-learn
- torch
- pillow
- torchvision
- torchsummary
- Requests
- pandas
- datetime
- xdg
- numpy
- streamlit
- streamlit-webrtc

## Setting up the project
- tba
<br/><br/>  
## System Pipelines
**Facial Expression Analysis** 
- Face Mesh by MediaPipe
     - Model that detects facial landmarks and extracts facial features.
- VGG16 from Keras
     - A pre-trained VGGNet model variant for object detection.
     - Optimized (tuned) the network architecture to output 7 targets (emotion categories).
     - Re-trained on FER-2013 face emotion image dataset comprising of 35, 887 images.
- LSTM
     - RNN to handle frame sequences of a video input.

[🔝 back to top](#emotify)
