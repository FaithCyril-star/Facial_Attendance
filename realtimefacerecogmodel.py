#import required libraries
import cv2
import face_recognition as FR
from mockcsvcreater import updater
from mockcsvcreater import writer
import os
import time
from mockcsvcreater import useRegex
import pickle

#initialise headers,filename, names and default states for attendancesheet
filename = "Attendance Sheet.csv"
header = ("Name", "Roll Number", "Absent/Present","Course","Level","Gender")
data = [
["Faith Cyril", "10201100091", "Absent","Computer Engineering","200","Male"],
["Louisa Ayamga", "10201100156", "Absent","Electrical Engineering","200","Female"],
["David Mensah", "10201100004", "Absent","Mechanical Engineering","200","Male"],
["Joleen Akrofi", "10201100122", "Absent","Computer Science","200","Female"],
["Doris Akuetteh", "10201100132", "Absent","Marketing","200","Female"],
["Maame Yaa Twumasi", "10201100088", "Absent","Computer Engineering","200","Female"]
]



writer(header,data,filename)
width=1280
height=720

Camera=cv2.VideoCapture(0,cv2.CAP_DSHOW)
Camera.set(cv2.CAP_PROP_FRAME_WIDTH,width)
Camera.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
Camera.set(cv2.CAP_PROP_FPS,10)
Camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*"MJPG"))
#initialise fonts and take out names and encodings from picklefile
font = cv2.FONT_HERSHEY_SIMPLEX
with open('train.pkl','rb') as model:
    names = pickle.load(model)
    encodings = pickle.load(model)


# The main loop of the program. It is the loop that is responsible for capturing the video and
# processing it.
end = 0
while True:
    ignore, frame=Camera.read()
    if end == 0:
        cv2.putText(frame,"Taking attendance...",(0,50),font,1,(0,165,255),2)
        timing = time.strftime("%I:%M:%S %p",time.localtime())
        cv2.putText(frame,f"Time:{timing}",(980,50),font,1,(0,165,255),2)
        frameBGR = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        facelocations = FR.face_locations(frameBGR)
        frameencodings = FR.face_encodings(frameBGR,known_face_locations = facelocations)
        # A for loop that is iterating over the face locations and face encodings.
        for facelocation,frameencoding in zip(facelocations,frameencodings):
            top,right,bottom,left = facelocation
            print(facelocation)
            cv2.rectangle(frame,(left,top),(right,bottom),(255,0,0),3)
            matches = FR.compare_faces(encodings,frameencoding,tolerance = 0.5)
            print(matches)
            # Checking if the face is recognized or not. If it is recognized, it will update the csv file
            # with the name of the person.
            name = "unknown person"
            if True in matches:
                print(names[matches.index(True)])
                name = names[matches.index(True)]
                updater(name,header,data,filename)
            if name!= 'unknown person':
                Roll = [i[1] for i in data if name in i][0]
            else:
                Roll = ''   
            cv2.putText(frame,f'{name}',(left-30,top-30),font,.75,(0,165,255),2)
            cv2.putText(frame,f'{Roll}',(left-30,top),font,.75,(0,165,255),2)
    else:
        cv2.putText(frame,"Attendance Time is Over",(100,100),font,3,(0,165,255),2)
    cv2.imshow('myscreen',frame)
    cv2.moveWindow('myscreen',0,0)
    
   # Checking if the user has pressed the q key or if the time is equal to the time that the user has
   # specified.
    if useRegex(time.asctime( time.localtime(time.time()) )):
        os.system('python automaticemail.py')
        end = 1
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
    # #or useRegex(time.asctime( time.localtime(time.time()) )):
        break
