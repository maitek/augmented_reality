import cv2
import base64
import numpy as np
from time import time
import dlib
import imutils
from imutils import face_utils

class Camera(object):
    def __init__(self):

        self.cap = cv2.VideoCapture(0)
        self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

        self.detector = dlib.get_frontal_face_detector()
        #import pdb; pdb.set_trace()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    def get_frame_jpeg(self):
        frame = self.get_frame()
        retval, buffer = cv2.imencode('.jpg', frame) 

        return (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


    def get_frame(self):
        #while(True):
        ret, frame = self.cap.read()
        #frame = cv2.resize(frame,(256,256))
        frame_width = 400
        d0 = 10
        frame = imutils.resize(frame, width=frame_width)

        # LINE DETECTION
        # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rects = self.detector(rgb_frame, 1)

        
        #print(len(rects))
        for rect in rects:
            cv2.rectangle(frame, (rect.left(),rect.top()), (rect.right(),rect.bottom()), (0, 255, 0), 1)
            shape = self.predictor(frame, rect)
            shape = face_utils.shape_to_np(shape)

            (x, y, w, h) = face_utils.rect_to_bb(rect)
            #import pdb; pdb.set_trace()
            face_width = np.linalg.norm(shape[16]- shape[2]) 
            z = d0*float(frame_width)/face_width
            # loop over the (x, y)-coordinates for the facial landmarks
            # and draw each of them
            for (i, (x, y)) in enumerate(shape):
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
			
            print(x,y,z)
        return frame
       

if __name__ == "__main__":
    cam = Camera()
    while(True):
        frame = cam.get_frame()
        cv2.imshow("frmae",frame)
        cv2.waitKey(10)