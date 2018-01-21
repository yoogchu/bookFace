#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from __future__ import print_function
from flask import Flask, render_template, Response, send_file, session
from camera import VideoCamera, VideoFeedback
import subprocess
from PIL import Image
import os.path
import cv2
from io import BytesIO

import sys


people = []
latestFaces = []



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    global latestFaces
    count = 0
    out = cv2.VideoWriter('full_out_video.mp4', cv2.VideoWriter_fourcc('M', 'P', 'J', 'G'), camera.get_fps()/2 - 9, (1280,720),True)    
    while True:
        real_frame = camera.get_frame()[0]
        ret, jpeg = cv2.imencode('.jpg', real_frame)
        frame = jpeg.tobytes()

        count = count + 1;

        if out.isOpened():
            out.write(real_frame)

            if (count % 50 == 0):
                out.release()
                cmd_str = "ffmpeg -i full_out_video.mp4 -vcodec h264 -s 160x90 current_low_output.mp4 -y"
                subprocess.Popen(
                [cmd_str],
                stdout=subprocess.PIPE, shell=True)
        else:
            if os.path.exists("full_out_video.mp4"):
                os.remove("full_out_video.mp4")
            out = cv2.VideoWriter('full_out_video.mp4', cv2.VideoWriter_fourcc('M', 'P', 'J', 'G'), camera.get_fps()/2 - 9, (1280,720),True)    

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        people = camera.get_frame()[1]

        # faces = person.getFaces();

        latestFaces = [person.getFaces()[len(person.getFaces()) - 1] for person in people]
        # print(str(latestFaces), file=sys.stderr)
        # print len(latestFaces);

        # print [len(person.getFaces()[0]) for person in people]

def gen_feed(camera):
    while True:
        real_frame = camera.get_frame()
        ret, jpeg = cv2.imencode('.jpg', real_frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    session['latestFaces'] = ['pls']
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/face/<int:face_index>')
def serve_img(face_index):
    global latestFaces
  #  print(len(latestFaces))
    #img = Image.fromarray(people[i].getFaces()[0][0][:,:,::-1])
    # print('SERVING IMAGE', file=sys.stderr)
    # print(str(session['latestFaces']), file=sys.stderr) 
    # print(str(latestFaces), file=sys.stderr)

    if (len(latestFaces) > face_index):

        last_face = latestFaces[face_index];
        img = Image.fromarray(last_face[0][:,:,::-1])

    else:
        img = Image.open('avatar.png')
        img = img.convert("RGB")
    return serve_pil_image(img)
@app.route('/ts/<int:face_index>',methods=['GET'])
def serve_ts(face_index):
    global latestFaces

    print(str(latestFaces), file=sys.stderr)

    if (len(latestFaces) > face_index):

        last_face = latestFaces[face_index];
        # print(last_face, file=sys.stderr)
        return last_face[1]
    else:
        return None

if __name__ == '__main__':
    if os.path.exists("full_out_video.mp4"):
        os.remove("full_out_video.mp4")
    app.secret_key = 'Jason'
    app.run(host='0.0.0.0', debug=True, threaded=True)






