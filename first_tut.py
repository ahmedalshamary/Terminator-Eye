# import the necessary packages
import datetime
import imutils
import time
import cv2
import angus
import io
import numpy as np
from twilio.rest import TwilioRestClient 

#Set up Facial Recogntion 
conn = angus.connect()
service = conn.services.get_service('age_and_gender_estimation', version=1)
service.enable_session()

# Sets up Twillio Message - removed for now change as needed
ACCOUNT_SID = "" 
AUTH_TOKEN = "" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

# Set up Camera Read Object
camera = cv2.VideoCapture(0)

# initialize the first frame in the video stream
firstFrame = None
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#body_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
z = 1
# loop over the frames of the video
while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
                break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, buff = cv2.imencode(".jpg", gray,  [cv2.IMWRITE_JPEG_QUALITY, 80])
        buff = io.BytesIO(np.array(buff).tostring())

        job = service.process({"image": buff})
        res = job.result
        count = 0
        counter = 1
        for face in res['faces']:
            x, y, dx, dy = face['roi']
            age = face['age']
            gender = face['gender']
            cv2.putText(frame, "Person {:.1f}".format(counter),
                (450,frame.shape[0] - (70 + count)), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 255, 255), 2)
            cv2.putText(frame, "age = {:.1f}".format(age - 5),
                (450,frame.shape[0] - (40 + count)), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 255, 255), 2)
            cv2.putText(frame, "gender = {}".format(gender),
                (450,frame.shape[0] - (10 + count)), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 255, 255), 2)
            count = count + 100
            counter = counter + 1
            while(z):
                    print("hi")
                    client.messages.create(
                            to="+13167372998", 
                            from_=" +19284400060 ", 
                            body="Person Age = {:.1f}, Person Gender = {}".format(age- 5, gender)
                    )
                    z = 0
            

 
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # if the first frame is None, initialize it
        if firstFrame is None:
                firstFrame = gray
                continue
        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (im2, cnts, hierarchy) = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#
        # loop over the contours
        counter = 1
        for (x,y,w,h) in faces:
                #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.circle(frame,(int(x+(w/2)),int(y+(h/2))),int(h/2),(0,0,255),2)
                cv2.line(frame,(x,int(y+(h/2))),(x+w,int(y+(h/2))),(0,0,255),2)
                cv2.line(frame,(int(x+(w/2)),y),(int(x+(w/2)),y+h),(0,0,255),2)
                cv2.putText(frame, "Person {:.1f}".format(counter),
                (x,y), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 0, 0), 2)
                counter = counter + 1

                cv2.putText(frame, "Target Acquired: Human",(0,25), cv2.FONT_HERSHEY_SIMPLEX, 1.00, (0, 0, 0), 2)
                
                #IF we want eye feature
                #roi_gray = gray[y:y+h, x:x+w]
                #roi_color = frame[y:y+h, x:x+w]      
                #eyes = eye_cascade.detectMultiScale(roi_gray)
                #for (ex,ey,ew,eh) in eyes:
                #        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,150,0),2)

        
        #for c in cnts:
                # if the contour is too small, ignore it

         #       if cv2.contourArea(c) < 5000:
          #              continue
 
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                #(x, y, w, h) = cv2.boundingRect(c)
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
        # draw the text and timestamp on the frame
        #cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        #       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 1)

        # show the frame and record if the user presses a key


        cv2.imshow("Arnold's Eye", frame)
        key = cv2.waitKey(1) & 0xFF

        
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
                break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
