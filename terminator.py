# import the necessary packages
import datetime
import imutils
import cv2
import angus
import io
import numpy as np
from twilio.rest import TwilioRestClient

#Set up Age + Gender API
conn = angus.connect()
service = conn.services.get_service('age_and_gender_estimation', version=1)
service.enable_session()

# Sets up Twillio Message put in your info here
ACCOUNT_SID = ""
AUTH_TOKEN = ""

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

# Amount of Messages to send
z = 1

# Set up Camera Read Object
camera = cv2.VideoCapture(0)

# initialize the first frame in the video stream
firstFrame = None
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')

# loop over the frames of the video
while True:
        #Gets first frame
        (grabbed, frame) = camera.read()

        # If there is no frame don't do anything
        if not grabbed:
                break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, buff = cv2.imencode(".jpg", gray,  [cv2.IMWRITE_JPEG_QUALITY, 80])
        buff = io.BytesIO(np.array(buff).tostring())
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        job = service.process({"image": buff})
        res = job.result
        counter = 0

        #Draws Mini-Map
        cv2.circle(frame,(410,90),60,(196,158,41),-1)
        cv2.line(frame,(480,55),(410,110),(255,0,0),2)
        cv2.line(frame,(340,55),(410,110),(255,0,0),2)

        for face in res['faces']:
            counter = counter + 1

            #Prints Out Gender and Age of Person
            x, y, dx, dy = face['roi']
            age = face['age']
            gender = face['gender']
            cv2.putText(frame, "Person {:.1f}".format(counter),
                (13+(200*(counter - 1)),frame.shape[0] - 94), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 255, 255), 2)
            cv2.putText(frame, "Age = {:.1f}".format(age),
                (13+(200*(counter - 1)),frame.shape[0] - 69), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 255, 255), 2)
            cv2.putText(frame, "Gender = {}".format(gender),
                (13+ (200*(counter - 1)),frame.shape[0] - 44), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 255, 255), 2)

            #Circle Over Person
            cv2.circle(frame,(int(x+(dx/2)),int(y+(dy/2))),int(dy/2),(0,0,255),2)
            cv2.line(frame,(x,int(y+(dy/2))),(x+dx,int(y+(dy/2))),(0,0,255),2)
            cv2.line(frame,(int(x+(dx/2)),y),(int(x+(dx/2)),y+dy),(0,0,255),2)
            cv2.putText(frame, "Person {:.1f}".format(counter),
            (int(x+(dx/5)),y-15), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)

            #Adds Individual Dots for Mini-Map
            cv2.putText(frame, "Target Acquired: Human",(0,25), cv2.FONT_HERSHEY_SIMPLEX, 1.00, (0, 0, 0), 2)
            if x<90:
                    cv2.circle(frame,(390,70),3,(0,0,255),-1)
            if 90<x<180:
                    cv2.circle(frame,(400,60),3,(0,0,255),-1)
            if 180<x<270:
                    cv2.circle(frame,(410,50),3,(0,0,255),-1)
            if 270<x<345:
                    cv2.circle(frame,(420,60),3,(0,0,255),-1)
            if x>345:
                    cv2.circle(frame,(430,70),3,(0,0,255),-1)
''' Uncomment this out and add the information from Twillio 
            while(z):
                print("hi")
                client.messages.create(
                        to="",
                        from_="",
                        body="Person Age = {:.1f}, Person Gender = {}".format(age- 5, gender)
                    )
                z = 0
'''
        #Adds Date and Time
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, .71, (255, 255, 255), 2)

        # Stop if
        cv2.imshow("Terminator's Eye", frame)
        # If the `q` key is pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
                break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
