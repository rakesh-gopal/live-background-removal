# OpenCV program to detect face in real time
# import libraries of python OpenCV
# where its functionality resides
import cv2
import sys
import numpy as np
from vidgear.gears import WriteGear


def process_vid(url_path, out_id=''):
    # load the required trained XML classifiers
    # https://github.com/Itseez/opencv/blob/master/
    # data/haarcascades/haarcascade_frontalface_default.xml
    # Trained XML classifiers describes some features of some
    # object we want to detect a cascade function is trained
    # from a lot of positive(faces) and negative(non-faces)
    # images.
    face_cascade = cv2.CascadeClassifier('lib/haarcascade_frontalface_default.xml')

    source = url_path

    cap = cv2.VideoCapture(source)    # Start the video source
    if not cap:
        return

    mask_width = 214
    mask_height = 295
    mask_face_x = 60
    mask_face_y = 65
    mask_face_height = 95
    mask = cv2.imread('lib/mask-sm.png', 0)

    last_face = None

    def get_crop(face, img):
        (fx, fy, fw, fh) = face
        ih, iw, _ = img.shape
        scale = fh/mask_face_height
        minx = int(fx - (mask_face_x*scale))
        miny = int(fy - (mask_face_y*scale))
        remw = iw - minx
        remh = ih - miny
        width = min(int(mask_width*scale), remw)
        height = min(int(mask_height*scale), remh)
        return (minx, miny, width, height)

    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # video_out = cv2.VideoWriter(
    #     '/Users/rakesh/git/hacks/live-background-removal/front-end/media/video-out.mp4', fourcc, 20.0, (mask_width, mask_height))

    # define (Codec,CRF,preset) FFmpeg tweak parameters for writer
    output_params = {
                     "-vcodec": "libx264", "-crf": "22", "-preset": "fast",
                    "-s": "%dx%d" % (mask_width, mask_height),
                    "-movflags": "faststart",
                    }
    video_out = WriteGear(output_filename='/Users/rakesh/git/hacks/live-background-removal/front-end/media/video-out%s.mp4' % out_id, compression_mode=True, logging=True, **output_params)

    while True:
        ret, img = cap.read()
        if not ret:
            break

        try:
            # convert to gray scale of each frames
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            continue

        # Detects faces of different sizes in the input image
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        face = None
        if len(faces) > 0:
            face = faces[0]

        if face is not None and last_face is not None:
            (fx, fy, fw, fh) = face
            (lfx, lfy, lfw, lfh) = last_face
            face = (int((fx*0.2+lfx*0.8)), int((fy*0.2+lfy*0.8)),
                    int((fw*0.2+lfw*0.8)), int((fh*0.2+lfh*0.8)))

        if face is None:
            face = last_face

        last_face = face

        if face is not None:
            try:
                (cx, cy, cw, ch) = get_crop(face, img)
                img = img[cy:cy+ch, cx:cx+cw]
                img = cv2.resize(img, (mask_width, mask_height))
                # img = cv2.bitwise_and(img,img,mask=mask)
            except:
                continue

        # Display an image in a window
        # cv2.imshow('img',img)
        video_out.write(img)

    # Close the window
    cap.release()
    # video_out.release()
    video_out.close()

