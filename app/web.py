from flask import Flask, render_template, request
import gpiozero
import time
import datetime

dt_format = "%Y-%m-%d %H:%M:%S"
RELAY_PIN = 23
status = ""

relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=False)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        status = str(relay.value)
        if request.method == 'POST':
            if request.form.get('on') == 'on':
                relay.on()
                status = "on"
                print("water on " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format))
            elif  request.form.get('off') == 'off':
                relay.off()
                status = "off"
                print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format))
            else:
                relay.off()
                print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format))
        elif request.method == 'GET':
            return render_template('index.html', status=status)
        return render_template("index.html", status=status)
    except GPIOZeroError:
        print('A GPIO Zero error occurred')
        relay.off()

    return render_template("index.html", status=status)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=False)