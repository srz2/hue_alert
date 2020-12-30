import os
import time
import requests
import threading
import configparser
from flask import Flask, render_template, redirect, send_from_directory

if not os.path.exists('config.ini'):
    print('Config file doesn''t exist')
    exit(1)

parser = configparser.ConfigParser()
parser.read('config.ini')
config = parser['DEFAULT']

hue_bridge_ip = config['ip_address']
uuid = config['uuid']
light_id = config['light_id']

desk_lamp_uri = f'{hue_bridge_ip}/api/{uuid}/lights/{light_id}/state'
command_on_standard = '{"on": true,"bri": 254, "hue": 10208,"sat": 254,"xy": [0.3131,0.3288],"colormode": "xy"}'
command_on_angry = '{"on": true,"bri": 254,"hue": 65125,"sat": 253,"xy": [0.6626,0.3159],"colormode": "xy","reachable": true}'
command_on = '{"on": true,"bri": 254, "hue": 10208,"sat": 254,"xy": [0.3131,0.3288],"colormode": "xy"}'
command_off = '{"on":false}'
command_authorize = '{"devicetype":"alert_app#raspberry_pi"}'

app = Flask(__name__)


class ThreadCommandExecution_Standard(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        threading.Thread.run(self)
        for x in range(0, 3):
            send_command(command_on_standard)
            time.sleep(1)
            send_command(command_off)
            time.sleep(1)


class ThreadCommandExecution_Angry(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        threading.Thread.run(self)
        for x in range(0, 5):
            send_command(command_on_angry)
            time.sleep(0.5)
            send_command(command_off)
            time.sleep(0.5)
        send_command(command_on_angry)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/authorize')
def authorize():
    r = requests.put(hue_bridge_ip + '/api', data=command_authorize)
    return r.text

@app.route('/check')
def check():
    return 'Access is Authorized: ' + str(check_connected())

@app.route('/on')
def turn_on():
    r = requests.put(desk_lamp_uri, data=command_on)
    if r.status_code == 200:
        return 'turned on'
    else:
        return 'Failed to turn on'

@app.route('/off')
def turn_off():
    r = requests.put(desk_lamp_uri, data=command_off)
    if r.status_code == 200:
        return 'turned off'
    else:
        return 'Failed to turn off'


@app.route('/standard')
def alert_fishes_standard():
    try:
        success = check_connected()
        if not success:
            raise Exception('Check connection failed')

        thread = ThreadCommandExecution_Standard('Standard Alert')
        thread.daemon = True
        thread.start()
        
        return 'Alerted Fish!'
    except Exception as e:
        print(e)
        return 'Failed to alert fish...'


@app.route('/angry')
def alert_fishes_angry():
    try:
        success = check_connected()
        if not success:
            raise Exception('Check connection failed')

        thread = ThreadCommandExecution_Angry('Angry Alert')
        thread.daemon = True
        thread.start()

        return 'Fish is in trouble....'
    except Exception as e:
        print(e)
        return 'Failed to alert fish, he''s in even more trouble now...'

def check_connected():
    r = requests.get(hue_bridge_ip + '/api' + '/' + uuid + '/lights')
    if 'error' in r.text:
        return False
    else:
        return True

def send_command(command):
    r = requests.put(desk_lamp_uri, command)
    if r.status_code == 200:
        return True
    else:
        raise Exception('Command Failed', command)

if __name__ == "__main__":
    app.run()
