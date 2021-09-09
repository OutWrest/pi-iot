import os
import datetime
import hashlib
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from lib.leds import *

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
    colors = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
    }

    color = request.form.get('color').lower()
    
    print(color)

    return render_template("led.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")