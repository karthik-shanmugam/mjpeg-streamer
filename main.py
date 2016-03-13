# main.py
from threading import Thread, Lock
from flask import Flask, render_template, Response
from camera import VideoCamera
import time
app = Flask(__name__)



#camera_lock = Lock()
cams = []# VideoCamera()
threads = []
for i in range(100):
    try:
        cam = VideoCamera(i)
    except:
        print "no camera with index: %d" % i
        break
    else:
        cams.append(cam)


def update(i):
    print "cameraaaa"
    global frame
    while True:
        time.sleep(.05)
        cams[i].update_frame()
threads = [Thread(target=update, args=(i, )) for i in range(len(cams))]
for thread in threads:
    thread.start()

@app.route('/')
def index():
    return render_template('index.html')

def gen(index):
    while True:
        time.sleep(.1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cams[index].get_frame() + b'\r\n\r\n')

@app.route('/video_feed/<int:cam_id>')
def video_feed(cam_id):
    if 0 <= cam_id < len(cams):
        return Response(gen(cam_id),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
    