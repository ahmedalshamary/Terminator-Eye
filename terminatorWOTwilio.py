# import the necessary packages
import datetime
import imutils
import cv2
import angus
import io
import numpy as np

#Set up Age + Gender API
conn = angus.connect()
service = conn.services.get_service('age_and_gender_estimation', version=1)
service.enable_session()

# Set up Camera Read Object
camera = cv2.VideoCapture(0)

# initialize the first frame in the video stream
firstFrame = None
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')

#body_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
z = 1
# loop over the frames of the video
while True:
        #Gets first frame
        (grabbed, frame) = camera.read()

        # If there is no frame don't do anything
        if not grabbed:
                break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, buff = cv2.imencode(".jpg", gray,  [cv2.IMWRITE_JPEG_QUALITY, 80])
        buff = io.BytesIO(np.array(buff).tostring())
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        job = service.process({"image": buff})
        res = job.result
        counter = 1

        for face in res['faces']:
            x, y, dx, dy = face['roi']
            age = face['age']
            gender = face['gender']
            cv2.putText(frame, "Person {:.1f}".format(counter),
                (13+(200*(counter - 1)),frame.shape[0] - 94), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 255, 255), 2)
            cv2.putText(frame, "Age = {:.1f}".format(age),
                (13+(200*(counter - 1)),frame.shape[0] - 69), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 255, 255), 2)
            cv2.putText(frame, "Gender = {}".format(gender),
                (13+ (200*(counter - 1)),frame.shape[0] - 44), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 255, 255), 2)
            counter = counter + 1

            #cv2.rectangle(frame,(x,y),(x+dx,y+dy),(255,0,0),2)
            cv2.circle(frame,(int(x+(dx/2)),int(y+(dy/2))),int(dy/2),(0,0,255),2)
            cv2.line(frame,(x,int(y+(dy/2))),(x+dx,int(y+(dy/2))),(0,0,255),2)
            cv2.line(frame,(int(x+(dx/2)),y),(int(x+(dx/2)),y+dy),(0,0,255),2)
            cv2.putText(frame, "Person {:.1f}".format(counter),
            (int(x+(dx/5)),y-15), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)

            cv2.putText(frame, "Target Acquired: Human",(0,25), cv2.FONT_HERSHEY_SIMPLEX, 1.00, (0, 0, 0), 2)
            cv2.line(frame,(340,55),(410,110),(255,0,0),2)
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

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
        cv2.circle(frame,(410,90),60,(196,158,41),-1)
        cv2.line(frame,(480,55),(410,110),(255,0,0),2)

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
