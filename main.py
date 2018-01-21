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
from camera import VideoCamera
from PIL import Image
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
    while True:
        frame = camera.get_frame()[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        people = camera.get_frame()[1]

        # faces = person.getFaces();

        latestFaces = [person.getFaces()[len(person.getFaces()) - 1] for person in people]
        # print(str(latestFaces), file=sys.stderr)
        # print len(latestFaces);

        # print [len(person.getFaces()[0]) for person in people]

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
    print(len(latestFaces))
    #img = Image.fromarray(people[i].getFaces()[0][0][:,:,::-1])
    # print('SERVING IMAGE', file=sys.stderr)
    # print(str(session['latestFaces']), file=sys.stderr) 
    # print(str(latestFaces), file=sys.stderr)
    if (len(latestFaces) > face_index):

        last_face = latestFaces[face_index];
        print('face_index', file=sys.stderr)
        print(face_index, file=sys.stderr)
        img = Image.fromarray(last_face[0][:,:,::-1])
        # img = Image.new('RGB', ...)
    else:
        img = img = Image.new('RGB', (800,1280), (255, 0, 255))
    return serve_pil_image(img)



if __name__ == '__main__':
    app.secret_key = 'Jason'
    app.run(host='0.0.0.0', debug=True, threaded=True)






