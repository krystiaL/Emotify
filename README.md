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
- [Getting Started](#setting-up-the-project)
- [Application Pipelines](#application-pipelines)

<br/>

## Application Features
  - **Sidebar FAQs**: contains instruction on application usage, reset, and other interesting facts.
  - **2 input modes**: <br/>
    📸 Real time camera capture using device webcam. <br/>
    📥 Image Upload for a specific face image.
  - **Embedded playlist**: You can play songs from the spotify embedding or get redirected to your Spotify library.

## Package Summary
1. **face_detect_module**
   > Model files and module for image preprocess and emotion prediction.
3. **interface**
   > Streamlit ui drafts, pages, and file handling functions. 
5. **notebooks**
   > Jupyter notebooks used for model experiments and data exploration. 
7. **playlist_module**
   > Modules for music dataset emotion labelling pipeline, playlist generation functions, and Spotify API params. 
9. **raw_data**
    > Includes csv files for original music dataset without emotion labels and DIY music dataset labeled with emotion scores. 
11. **tests**
    > Test files to check functionality of extract_emotion function from face_emotion_detector module and playlist generation functions from generate_playlist module.  
13. **app.py**
    > Streamlit application file.  
15. **requirements.txt**
    > List of dependencies used to create the application. 

## Setting up the project
- tba
<br/><br/>  
## Application Pipelines
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
