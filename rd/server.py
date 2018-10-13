from flask import Flask,Response,render_template,request
from PIL import ImageGrab,ImageDraw
import cv2
import sys
import numpy as np
import  pyautogui
import base64
app=Flask(__name__)

def grabImg():
    while True:
        allframes=frames()
        for frame in allframes:
            yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def frames():
    while True:
        img=ImageGrab.grab()
        img = draw_mouse(img)
        # convert image to numpy array
        img_np = np.array(img)
        # convert color space from BGR to RGB
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        # convert image to jpg format
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield jpeg.tobytes()

def draw_mouse(img):
    """
    utility function to draw mouse pointer
    """
    # generate Draw object for PIL image
    draw = ImageDraw.Draw(img)
    # find current position of mouse pointer
    pos = pyautogui.position()
    # coordinates of ellipse
    ax, ay, bx, by = pos[0], pos[1], pos[0] + 10, pos[1] + 10
    # draw ellipse on image
    draw.ellipse((ax, ay, bx, by), fill="yellow")
    return img
@app.route('/sendImg')
def sendImg():
    return Response(grabImg(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/mouse',methods=['GET','POST'])
def mouse():
    type = request.form['type']
    ex=request.form['x']
    ey=request.form['y']
    imX = request.form['X']
    imY = request.form['Y']
    dx, dy = pyautogui.size()
    print(ex,ey,imX,imY,dx,dy,file=sys.stderr)
    print(type)
    x, y = dx * (float(ex) / float(imX)), dy * (float(ey) / float(imY))
    if type =="mousemove":
        pyautogui.moveTo(x, y)
    elif type == "click":
        pyautogui.click(x,y)
    elif type == 'rightclick':
        pyautogui.click(x, y, button='right')
    elif type == 'dblclick':
        pyautogui.doubleClick(x, y)

    return ""
@app.route('/keyboard', methods=['POST'])
def keyboard_event():
# keyoard event
    event = request.form.get('type')
    print(event)
    pyautogui.press(event)
    return ""
@app.route('/text', methods=['POST'])
def text_event():
    chars = request.form['type']

    pyautogui.typewrite(chars)
    return ""
@app.route('/char', methods=['POST'])
def char_event():
    shift = request.form['shift']
    char = request.form['type']
    if(shift=='true'):
        pyautogui.keyDown('shift')

        pyautogui.keyDown(char)
        pyautogui.keyUp('shift')
        pyautogui.keyUp(char)
    else:
        pyautogui.typewrite(char)
    #pyautogui.typewrite(chars)
    return ""
@app.route('/')
def screen():
    return render_template('screen.html')

if __name__ == '__main__':
    app.run(host='10.5.4.234',port=8003)
    #app.run(debug=True)