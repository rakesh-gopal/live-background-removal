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

mask_width = 214
mask_height = 295
mask_face_x = 65
mask_face_y = 72
mask_face_height = 95
mask = cv2.imread('mask-sm.png',0)

last_face = None

def should_show(px, py):
    if mask[py, px] == 0:
        return False
    return True

def get_crop(face):
    (fx,fy,fw,fh) = face
    scale = fh/mask_face_height
    minx = int(fx - (mask_face_x*scale))
    miny = int(fy - (mask_face_y*scale))
    width = int(mask_width*scale)
    height = int(mask_height*scale)
    return (minx, miny, width, height)

while True: 
    ret, img = cap.read()

    # convert to gray scale of each frames 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detects faces of different sizes in the input image 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    face = None
    if len(faces) > 0:
        face = faces[0]

    if face is not None and last_face is not None:
        (fx,fy,fw,fh) = face
        (lfx,lfy,lfw,lfh) = last_face
        face = (int((fx*0.1+lfx*0.9)), int((fy*0.1+lfy*0.9)),
                int((fw*0.1+lfw*0.9)), int((fh*0.1+lfh*0.9)))

    if face is None:
        face = last_face

    last_face = face

    if face is not None:
        try:
            (cx, cy, cw, ch) = get_crop(face)
            img = img[cy:cy+ch, cx:cx+cw]
            img = cv2.resize(img, (mask_width, mask_height))
            img = cv2.bitwise_and(img,img,mask = mask)
        except:
            continue

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

