# opencv_scheme
OpenCV-Scheme - Computer Vision bindings for Scheme

### Author: Mehar Samra

### Introduction

This project creates OpenCV bindings for the scheme language using the scheme interpreter for CS61A at UC Berkeley. 

[Robotics](./image.png)

To create a video file capture device:

(define video (cv2.videocapture "/Users/mehar/Documents/course_footage/GOPR1142.MP4"))

Or you can capture from your webcamera:

(define webcam (cv2.videocapture 0))

To read a frame:

(define img (device 'read))

To display a frame:

(cv2.imshow "Scheme CV2 Demo" img)

### Bindings

The complete set of bindings are implemented are as follows: cv2.videocapture, which allows you to capture frames from an mp4 video file or images from your web camera; cv2.imshow, which displays an OpenCV image; cv2.cvtcolor, which converts an image to a different color space, such as HSV; cv2.inrange, which applies a filter that creates a black-and-white threshold image; and draw_contours, which is a utility method that detects contours in a threshold image and draws bounding box rectangles around the detected objects. 

### Samples

Additionally, the [video_detect.scm](/video_detect.scm) that is a port of my original [video_detect.py](/video_detect.py) Python video detection script. Note, the typical approach of grabbing frames in a while loop in Python is replaced with recursion in Scheme. The limitations were that the contour detection and the drawing of bounding boxes required dozens more OpenCV bindings, so instead I exposed one utility function, draw_contours, to do the same procedure, but in principle it is possible to do a port with all of the same OpenCV calls as my original Python script. 


 
