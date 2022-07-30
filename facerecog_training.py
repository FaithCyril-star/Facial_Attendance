
import face_recognition as FR
import os
import pickle
import cv2


imageDIR = r"C:\Users\Owner\Downloads\FIE_Files\Attendance"##this was my directory lol
encodings = []
names = []
for root,dirs,files in os.walk(imageDIR):
    print("my Working folder (root): ",root)
    print("dirs in root: ",dirs)
    for file in files:
        name = os.path.splitext(file)[0]
        names.append(name)

        fullpath = os.path.join(root,file)
        # print(fullpath)
        myPicture = FR.load_image_file(fullpath) 
        myPicture = cv2.cvtColor(myPicture,cv2.COLOR_RGB2BGR)
        locations = FR.face_locations(myPicture)
        myencoding = FR.face_encodings(myPicture,known_face_locations = locations,num_jitters=100)[0]
        encodings.append(myencoding)

with open('train.pkl','wb') as model:
    pickle.dump(names,model)
    pickle.dump(encodings,model)
 