from flask import Flask, render_template, request
import time
import datetime
import os
import json
import sys

# Import VenusRelay from root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from irrigator import VenusRelay

dt_format = "%Y-%m-%d %H:%M:%S"
filePath = "/tmp/irrigate.out"

# Relay 2 (index 1) via DBus / sysfs fallback
relay = VenusRelay(relay_index=1)

app = Flask(__name__)

@app.route("/api", methods=['GET'])
def api():
    json_output = {}
    if os.path.isfile(filePath):
        file = open(filePath, "r")
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
            if request.form.get('i-action') == 'on':
                relay.on()
                output.update(status="on")
                print("water on " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format), flush=True)
            elif request.form.get('i-action') == 'off':
                relay.off()
                output.update(status="off")
                print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format), flush=True)
            else:
                relay.off()
                output.update(status="off")
                print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format), flush=True)
        elif request.method == 'GET':
            if os.path.isfile(filePath):
                file = open(filePath, "r")
                output.update(history=file.read())
                file.close()

            return render_template('index.html', output=output)
        return render_template("index.html", output=output)
    except Exception as e:
        print(f"Error in web interface: {e}", flush=True)
        relay.off()

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)