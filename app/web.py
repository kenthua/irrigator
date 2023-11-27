from flask import Flask, render_template, request
import gpiozero
import time
import datetime
import os
import json

dt_format = "%Y-%m-%d %H:%M:%S"
RELAY_PIN = 23
status = ""
filePath = "/tmp/irrigate.out"

relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=False)

app = Flask(__name__)

@app.route("/api", methods=['GET'])
def api():
    json_output = {}
    if(os.path.isfile(filePath)):
        file = open("/tmp/irrigate.out", "r")
        history = file.read()
        file.close()
        history_list = history.split("|| ")
        output = {
            "status": relay.value,
            "history": history_list
        }
        json_output = json.dumps(output, indent=2)
        print(json_output, flush=True)

    return json_output

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        status = ""
        output = {
            "status": str(relay.value),
            "history": ""
        }

        if request.method == 'POST':
            if request.form['i-action']  == 'on':
                relay.on()
                output.update(status = "on")
                print("water on " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format), flush=True)
            elif request.form['i-action']  == 'off':
                relay.off()
                output.update(status = "off")
                print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format), flush=True)
            else:
                relay.off()
                output.update(status = "off")
                print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format), flush=True)
        elif request.method == 'GET':
            if(os.path.isfile(filePath)):
                file = open("/tmp/irrigate.out", "r")
                output.update(history = file.read())
                file.close()

            return render_template('index.html', output=output)
        return render_template("index.html", output=output)
    except GPIOZeroError:
        print('A GPIO Zero error occurred', flush=True)
        relay.off()

    return render_template("index.html", output=output)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=False)