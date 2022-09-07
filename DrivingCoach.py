# USAGE
# python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav

from scipy.spatial import distance as dist
from imutils.video import VideoStream, FileVideoStream, FPS
from imutils import face_utils
from threading import Thread  
import numpy as np
import playsound    
import argparse
import imutils     
import time 
import dlib 
import cv2 
import logging
from numpy_ringbuffer import RingBuffer

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)

def sound_alarm(path):
   
    playsound.playsound(path)


def eye_aspect_ratio(eye):
   
    a = dist.euclidean(eye[1], eye[5])
    b = dist.euclidean(eye[2], eye[4])

    c = dist.euclidean(eye[0], eye[3])

    return (a + b) / (2.0 * c)

def rect_to_bb(rect):

    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y

    return (x, y, w, h)

ap = argparse.ArgumentParser()

ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
ap.add_argument("-a", "--alarm", type=str, default="",
                help="path alarm .WAV file")
ap.add_argument("-m", "--movie", type=str, default="",
                help="movie file")
ap.add_argument("-i", "--image", type=str, default="",
                help="image file")
ap.add_argument("-w", "--webcam", type=int, default=0,
                help="index of webcam on system")
ap.add_argument("-l", "--log", type=str, default="",
                help="path to logfile")
args = vars(ap.parse_args())


EYE_AR_THRESH = 2
EYE_AR_CONSEC_FRAMES = 8 #48


COUNTER = 0
ALARM_ON = False

earBuf = RingBuffer(capacity=120, dtype=np.float, allow_overwrite=True)


def calculate_score(value):
    if earBuf.is_full:
        std = np.std(earBuf)
        if std == 0:
            score = 0
        else:
            score = (value - np.mean(earBuf)) / std
    else:
        score = 0
    earBuf.append(value)
    return score


def nothing(x): return 0


print("[INFO] loading facial landmark predictor...")

# hog + svm based face detector
face_detector = dlib.get_frontal_face_detector()


predictor = dlib.shape_predictor(args["shape_predictor"])

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

log_file = None
ear = 0
z_score = 0

cv2.namedWindow("Frame")
cv2.createTrackbar('Threshold', 'Frame', 0, 100, nothing)
cv2.setTrackbarPos('Threshold', 'Frame', EYE_AR_THRESH * 10)

print("[INFO] starting video stream thread...")

MOVIE = 1
IMAGE = 2
WEBCAM = 3

imageSrc = 0
if args["movie"]:
    vs = FileVideoStream(args["movie"])
    imageSrc = MOVIE
elif args["image"]:
    vs = FileVideoStream(args["image"])
    imageSrc = IMAGE
else:
    vs = VideoStream(src=args["webcam"])
    imageSrc = WEBCAM
    time.sleep(1.0)

if args["log"]:
    log_file = open(args["log"], "w")

vs.start()
fps = FPS().start()
log_start = time.time()
frameID = -1
eventID = 0
frame = None
faces = []

while True:

    frameID += 1

    if imageSrc in [MOVIE,WEBCAM]:
        frame = vs.read()


    if imageSrc == IMAGE and frameID==0:
        frame = vs.read()

    log_time = time.time() - log_start
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    if frameID % 10 == 0:
        faces = face_detector(gray, 0)

    # loop over the face detections
    for rect in faces:

        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)


        ear = (leftEAR + rightEAR) / 2.0


        z_score = calculate_score(ear)

        EYE_AR_THRESH = cv2.getTrackbarPos('Threshold', 'Frame') / 10

        if z_score < 0 and abs(z_score) > EYE_AR_THRESH:
            if COUNTER == 0: eventID += 1
            COUNTER += 1

            cv2.imwrite(f'snapshots/img-{frameID:d}-closed.jpg', frame)

            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                # if the alarm is not on, turn it on
                if not ALARM_ON:
                    ALARM_ON = True

                    if args["alarm"] != "":
                        t = Thread(target=sound_alarm,
                                   args=(args["alarm"],))
                        t.deamon = True
                        t.start()

                # draw an alarm on the frame
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        else:
            COUNTER = 0
            ALARM_ON = False

        cv2.putText(frame, f"EAR: {np.mean(earBuf):.3f} {eventID:3d} {COUNTER:3d}",
                    (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    fps.update()


    if key in [ord("q"), 27]:
        break

    if log_file:
        log_file.write(f'{frameID:9d}, {log_time:12.3f}, {ear:.3f}, {z_score:6.3f}, {eventID:3d}, {COUNTER:3d}, {int(ALARM_ON):d}\n')

cv2.destroyAllWindows()
fps.stop()
vs.stop()

print(f"Fps:{fps.fps():.2f} elapsed:{fps.elapsed():.2f}")

if log_file:
    log_file.close()
