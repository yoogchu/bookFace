import numpy as np
import cv2
import face_recognition
import compare_face as cf
import os
import glob

video = 'fuhax1.mov'
face_folder = video[0:video.index('.')]+'/'

# cap = cv2.VideoCapture(video)
cap = cv2.VideoCapture(0)


(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
if int(major_ver)  < 3 :
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
else :
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600,600)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
frame_count = 0
people = ([], 0)

while True:
    # Grab a single frame of video
    ret, frame = cap.read()
    if ret:

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)

            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left) in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # # Label
            # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            # font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            crop = frame[top:bottom, left:right]

            people = cf.manageFaces(people, crop, face_encodings)
            cv2.imshow('cropped', crop)

            #cv2.waitKey(0)

        # Display the resulting image
        cv2.imshow('image', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release handle to the webcam
cap.release()
cv2.destroyAllWindows()


print 'saving faces...'

if not os.path.exists(face_folder):
    print 'trying to make: ' + face_folder
    try:
        os.mkdir(face_folder)
    except OSError as e:
        print e
else:
    print 'deleting faces that already exist...'
    for f in glob.glob(face_folder+'*'):
        os.remove(f)
for person in people[0]:
    count = 0
    for face in person.getFaces():
        print face_folder+'p'+person.getName()+'_'+str(count)+'.jpg'
        cv2.imwrite(face_folder+'p'+person.getName()+'_'+str(count)+'.jpg', face[0])
        count+=1

