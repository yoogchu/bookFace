import numpy as np
import cv2
import face_recognition
import compare_face as cf
import os
import glob
from datetime import datetime


def recog(people, cap, webcam=True, video_name = 'fuhax.mov'):

    # Initialize some variables
    face_locations = []
    face_encodings = []

    process_frame = True

    # Grab a single frame of video
    ret, frame = cap.read()
    if ret:
        face_names = []
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                people, name = cf.manageFaces(people, face_encoding)
                face_names.append(name)

        process_frame = not process_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            crop = frame[top:bottom, left:right]
            p = cf.Person.getPerson(name, people)
            p.addFace((crop, str(datetime.now())))

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        return frame[:,:,::-1], people

def save_faces(people, folder='webcam', webcam=True):
    try:
        face_folder = folder[0:folder.index('.')]+'/'
    except Exception:
        face_folder = folder+'/'

    if not os.path.exists(face_folder):
        try:
            os.mkdir(face_folder)
        except OSError as e:
            print e
    else:
        for f in glob.glob(face_folder+'*'):
            os.remove(f)
    for person in people:
        count = 0
        for faces in person.getFaces():
            face, timestamp = faces
            count+=1
            if webcam:
                if count % 5 == 0:
                    print face_folder+person.getName()+'_'+str(count/5)+'.jpg | '+timestamp
                    cv2.imwrite(face_folder+person.getName()+'_'+str(count/5)+'.jpg', face)
                else:
                    continue
            else:
                print face_folder+person.getName()+'_'+str(count)+'.jpg'
                cv2.imwrite(face_folder+person.getName()+'_'+str(count)+'.jpg', face)
    return 1
