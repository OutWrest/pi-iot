import os
import datetime
import hashlib
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from leds import new_strip

strip = new_strip(300)

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
    
    rgb = colors.get(color, (0, 0, 0))
    brightness = int(request.form.get('brightness', 0)) * 255 // 100

    strip.changeBrightness(brightness)
    strip.colorWipe(strip.getColor(*rgb))

    return render_template("led.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")