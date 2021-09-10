import json
import threading, queue
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
#from leds import new_strip
from parse import *

# INTI control 
#strip = new_strip(300)

# INIT
funcs = {
    'colorWipe': print
}

q = queue.Queue()

def stripLoop():
    while True:
        if q.qsize() == 1:
            func, params = q.get()
            q.put((func, params))
        else:
            func, params = q.get()
            q.task_done()

        func(*params)

#threading.Thread(target=stripLoop, daemon=True).start()

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
    args = parse_arg(request.form.get('args'))

    if not func:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}
    
    q.put(func, args)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/led/brightness", methods = ["POST"])
def FUN_led_b():
    brightness = int(request.form.get('brightness', 0)) * 255 // 100
    #strip.changeBrightness(brightness)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")