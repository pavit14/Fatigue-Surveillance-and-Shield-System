import cv2
import dlib
from scipy.spatial import distance
import playsound
import time
from threading import Thread
import urllib.request
EYE_AR_THRESH = 0.26
EYE_AR_CONSEC_FRAMES = 38
COUNTER = 0
ALARM_ON = False
baseURL = 'https://api.thingspeak.com/update?api_key=CN7EJ8EIHYQZNMZU&field1='

def sound_alarm(path):
   
    playsound.playsound(path)

def calculate_EAR(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear_aspect_ratio = (A+B)/(2.0*C)
    return ear_aspect_ratio

cap = cv2.VideoCapture(0)
hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor(
    "shape_predictor_68_face_landmarks.dat")
while True:
    _, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = hog_face_detector(gray)
    for face in faces:
        
        face_landmarks = dlib_facelandmark(gray, face)
        leftEye = []
        rightEye = []
        
        for n in range(36, 42):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            leftEye.append((x, y))
            next_point = n+1
            if n == 41:
                next_point = 36
            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y
            cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)

       
        for n in range(42, 48):
         
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            rightEye.append((x, y))
            next_point = n+1
            if n == 47:
                next_point = 42
            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y
            cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)

     
        left_ear = calculate_EAR(leftEye)

        right_ear = calculate_EAR(rightEye)

        EAR = (left_ear+right_ear)/2
        EAR = round(EAR, 2)
       
        if EAR < EYE_AR_THRESH:
            # 0.26
            COUNTER += 1
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                if not ALARM_ON:
                    ALARM_ON = True
                    t = Thread(target=sound_alarm,
                               args=('alarm_sound.wav',))
                    t.daemon = True
                    t.start()

                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if (COUNTER==EYE_AR_CONSEC_FRAMES) :
                f = urllib.request.urlopen(baseURL+str(1))

            print("Drowsy")
        else:
            COUNTER = 0
            ALARM_ON = False
            #f = urllib.request.urlopen(baseURL+str(0))
            
        print(EAR)
        #
    cv2.imshow("Driver Drowsiness Detection System", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
