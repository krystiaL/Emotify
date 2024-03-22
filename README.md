<div>
   <img src="https://github.com/Atsuto-LeWagon/Emotify/blob/master/interface/images/emotify_banner.png"/>
</div>


## Project Overview
As a team of four music enthusiast, this application was created to personalize music selection based on the emotional responses. <br/>
Specifically, emotify automates playlist generation based on an identified emotion from a face image. <br/>


This application is a **Multimodal Emotion Recognition and Playlist Generation System** that is built with a comprehensive machine learning pipeline that incorporates:
   1. **Facial Expression Analysis** 
        - A pipeline for detecting and interpreting emotional cues from facial movements. 
   2. **Music labeling Function** 
        - A pipeline that uses music metadata to label emotion scores and dominant emotion of each song in a music dataset.
   3. **External data integration**
        - Use of Spotify API for playlist generation. 

## Demo 

[Link](https://www.canva.com/design/DAF-UIQAC9E/2Arrd_L3-KkWw7DI3VfYWg/view?utm_content=DAF-UIQAC9E&utm_campaign=share_your_design&utm_medium=link&utm_source=shareyourdesignpanel) to Demo Slides

<br/>

## Table of Contents
- [Application Features](#application-features)
- [Package Summary](#package-summary)
- [Getting Started](#setting-up-the-project)
- [Models](#models)
- [Creators](#creators)

--- 

## Application Features
  - **Sidebar FAQs**: contains instruction on application usage, reset, and other interesting facts.
  - **2 input modes**: <br/>
    📸 Real time camera capture using device webcam. <br/>
    📥 Image Upload for a specific face image.
  - **Embedded playlist**: You can play songs from the spotify embedding or get redirected to your Spotify library.
    
---  

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
    
--- 

## Setting up the project
1. Download the project by cloning the repository:
   
   ```bash
   git clone git@github.com:Atsuto-LeWagon/Emotify.git
   cd Emotify
   ```
2.  Create a new virtual env for the project directory:
   
      ```bash
      pyenv virtualenv emotify
      pyenv local emotify
      ```
3. Install the required dependencies:
   
   ```bash
   make install_requirements
   pip list 
   ```
4. Run the application with streamlit:
   
      ```bash
      make streamlit_main_ui
      ```
--- 

## Models
**Facial Expression Analysis Pipe** 
- Face Mesh by MediaPipe
     - Model that detects facial landmarks and extracts facial features.
- VGG16 from Keras
     - A pre-trained VGGNet model variant for object detection.
     - Optimized (tuned) the network architecture to output 7 targets (emotion categories).
     - Re-trained on FER-2013 face emotion image dataset comprising of 35, 887 images.
- LSTM
     - RNN to handle frame sequences of a video input.

**Music labeling Pipeline**
- DIY music emotion labeling model
     - Neural Network trained on a DIY music dataset with emotion labels to perform music emotion classification task.
	  - Added a function that calculates the mean squared error between user's emotion probability mixture and an array of probabilty each track has in the predicted dataset from the neural network. 
- Selected tracks with the minimum MSE and randomly pick 10 tracks from the selection as an output. 

--- 

## Creators

<img src="https://github.com/Atsuto-LeWagon/Emotify/blob/master/interface/images/team_pics/team_photo.png"/>

We are a diverse team of data scientists and alumni of Le Wagon Tokyo's Data Science and AI course (#batch-1384-tokyo). 
Emotify is our final project to conclude our six-month bootcamp journey which showcases our expertise. 

[🔝 back to top](#emotify)
