# OpenCV program to detect face in real time 
# import libraries of python OpenCV 
# where its functionality resides 
import cv2
import sys

# load the required trained XML classifiers 
# https://github.com/Itseez/opencv/blob/master/ 
# data/haarcascades/haarcascade_frontalface_default.xml 
# Trained XML classifiers describes some features of some 
# object we want to detect a cascade function is trained 
# from a lot of positive(faces) and negative(non-faces) 
# images. 
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 

source = 0   					# defaults to local (laptop) camera

if len(sys.argv) > 1:
	if ('-h' == sys.argv[1]) or ('--help'==sys.argv[1]):
		print("usage: greenscreen.py [-h,--help] [input_file]")
		print("   If input_file is blank, defaults to live camera capture")
		sys.exit()
	source = sys.argv[1]

cap = cv2.VideoCapture(source)    # Start the video source


# loop runs if capturing has been initialized. 
while True: 

    # reads frames from a camera 
    ret, img = cap.read() 

    # convert to gray scale of each frames 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

    # Detects faces of different sizes in the input image 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 

    for (x,y,w,h) in faces: 
        # To draw a rectangle in a face 
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2) 

    # Display an image in a window 
    cv2.imshow('img',img) 

    # Wait for Esc key to stop 
    k = cv2.waitKey(30) & 0xff
    if k == 27: 
        break

# Close the window 
cap.release() 

# De-allocate any associated memory usage 
cv2.destroyAllWindows() 

