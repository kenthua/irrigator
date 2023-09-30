from flask import Flask, render_template, request
# import gpiozero
import time
import datetime
import os
import json
from weather import *

dt_format = "%Y-%m-%d %H:%M:%S"
RELAY_PIN = 23
status = ""
filePath = "/tmp/irrigate.out"

# relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=False)

weather = Weather()

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
            "status": "off",
            "history": history_list
        }
        json_output = json.dumps(output, indent=2)
        print(json_output)

    return json_output

@app.route("/", methods=['GET', 'POST'])
def index():
    # try:
    status = "0"

    output = {
        "status": "0",
        "weather": {
            "precipitation": weather.precipitation(),
            "yesterdayPrecipitation": weather.yesterdayPrecipitation()
        }
    }
    
    if request.method == 'POST':
        if request.form['i-action']  == 'on':
            # relay.on()
            output.update(status = "on")
            # print("water on " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format))
        elif request.form['i-action']  == 'off':
            # relay.off()
            output.update(status = "off")
            # print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format))
        else:
            print("nothing")
            output.update(status = "off")
            # relay.off()
            # print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format))
    elif request.method == 'GET':
        if(os.path.isfile(filePath)):
            file = open("/tmp/irrigate.out", "r")
            status = str(output.get(status)) + "|" + file.read()
            output.update(status = status)
            file.close()
            
        return render_template('index.html', output=output)
    return render_template("index.html", output=output)
    # except GPIOZeroError:
    #     print('A GPIO Zero error occurred')
        # relay.off()



if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=False)