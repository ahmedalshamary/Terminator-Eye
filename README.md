# Terminators Eye
This was a project for Local Hack Day Georgetown 2016:

We used Python3 and OpenCV to process a Video Stream and track faces and report back age and gender. 

The Age and Gender were sent to an API to process so we really dind't do that part. API LINK - 

We also used Twillio to send a text message to the user alerting them of the gender and age of the person using their computer. 

Lastly, we built in a "fps" style mini-map that displays the people that the camera is capturing. 

Cool things to try to add would be to make this run in the background and have it recognize only the user and send a text if its not the user. 
Also make this less intensive on the computer using the cuda OpenCV library and building in age and gender recognition natively.

There are to run this project with twillio or without. 

With Twilio:
1. Create a env with virtualenv(recoommended) or not then run a
    pip install -r requiremnts.txt
    
2. Go to API Link Generate key - https://www.angus.ai/ + follow additional steps for recogintion

3. Look through code on terminatory.py and find the update for twilio account. 
   Update your twilio account information in there

You should be good now. If you have multiple webcams connected to your computer you might need to change the 0 for webcam to whatever number yours is. 

Without Twilio:

1. Create a env with virtualenv(recoommended) or not then run a
    pip install -r requiremnts.txt
    
2. Go to API Link Generate key - https://www.angus.ai/ + follow additional steps for recogintion

You should be good now. If you have multiple webcams connected to your computer you might need to change the 0 for webcam to whatever number yours is. 
