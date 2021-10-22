import json
import threading, queue
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from leds import new_strip
from parse import *

# INTI control 
strip = new_strip(300)
strip.show()
strip.changeBrightness(255)

# INIT
funcs = {
    'colorWipe': strip.colorWipe,
    'setColor': strip.setColor,
    'rainbow': strip.rainbow,
    'theaterChaseRainbow': strip.theaterChaseRainbow,
    'theaterChase': strip.theaterChase,
}

funcs_no_repeat = {
    'colorWipe': strip.colorWipe,
    'setColor': strip.setColor,
}

q = queue.Queue()

def stripLoop():
    while True:
        func, color, params = q.get()
        q.task_done()

        if q.qsize() == 0 and func not in funcs_no_repeat:
            q.put((func, color, params))

        if color:
            color = strip.getColor(*color)
            func(color, *params)
        else:
            func(*params)
        #print(func, color, *params)

threading.Thread(target=stripLoop, daemon=True).start()

app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def FUN_root():
    return render_template("index.html")

@app.route("/led", methods = ["GET"])
def FUN_led():
    return render_template("led.html")

@app.route("/led", methods = ["POST"])
def FUN_led_p():
    global rgb, brightness, funcs

    func = funcs.get(request.form.get('func'))
    color = parse_arg(request.form.get('color'))
    args = parse_arg(request.form.get('args'))

    if not func:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}
    
    if q.qsize() == 0 or q.queue[-1] != (func, args):
        q.put((func, color, args))

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/led/brightness", methods = ["POST"])
def FUN_led_b():
    global strip
    brightness = int(request.form.get('brightness', 0)) * 255 // 100

    strip.changeBrightness(brightness)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/led/queue", methods = ["GET"])
def FUN_led_q():
    return json.dumps({'success':True, 'queue':q.qsize()}), 200, {'ContentType':'application/json'}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")