import os
import time
import json
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
device = config['device']

# Need split because GET request for just the state uri is not available
desk_lamp_uri_light = f'{hue_bridge_ip}/api/{uuid}/lights/{light_id}'
desk_lamp_uri_light_state = f'{desk_lamp_uri_light}/state'

command_on_standard = '{"on": true,"bri": 254, "hue": 10208,"sat": 254,"xy": [0.3131,0.3288],"colormode": "xy"}'
command_on_ping = '{"on": true,"bri": 165, "hue": 31528, "sat": 57, "xy": [0.4654, 0.4714], "colormode": "xy"}'
command_on_angry = '{"on": true,"bri": 254,"hue": 65125,"sat": 253,"xy": [0.6626,0.3159],"colormode": "xy"}'
command_on_love = '{"on": true,"bri": 254,"hue": 34113,"sat": 254,"xy": [0.3806,0.1896],"colormode": "xy"}'
command_on_tea  = '{"on": true,"bri": 254, "hue": 25600,"sat": 254,"xy": [ 0.1772, 0.6946 ], "colormode": "xy"}'
command_on = '{"on": true,"bri": 254, "hue": 10208,"sat": 254,"xy": [0.3131,0.3288],"colormode": "xy"}'
command_off = '{"on":false}'
command_authorize = '{"devicetype":"alert_app#' + device + '"}'

app = Flask(__name__)

class ThreadCommandExecution_Base(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.reset_to_initial_state = True
        self.initial_state = get_current_state()

    def __del__(self):
        if self.reset_to_initial_state:
            time.sleep(1)
            send_command(self.initial_state)

class ThreadCommandExecution_Standard(ThreadCommandExecution_Base):
    def __init__(self, name):
        super().__init__(name)

    def run(self):
        threading.Thread.run(self)
        for x in range(0, 3):
            send_command(command_on_standard)
            time.sleep(1)
            send_command(command_off)
            time.sleep(1)

class ThreadCommandExecution_Angry(ThreadCommandExecution_Base):
    def __init__(self, name):
        super().__init__(name)
        self.reset_to_initial_state = False

    def run(self):
        threading.Thread.run(self)
        for x in range(0, 5):
            send_command(command_on_angry)
            time.sleep(0.5)
            send_command(command_off)
            time.sleep(0.5)
        send_command(command_on_angry)

class ThreadCommandExecution_Love(ThreadCommandExecution_Base):
    def __init__(self, name):
        super().__init__(name)

    def run(self):
        threading.Thread.run(self)
        send_command(command_on_love)
        time.sleep(2)
        send_command(command_off)

class ThreadCommandExecution_Ping(ThreadCommandExecution_Base):
    def __init__(self, name):
        super().__init__(name)

    def run(self):
        threading.Thread.run(self)
        for x in range(0, 2):
            send_command(command_on_ping)
            time.sleep(0.5)
            send_command(command_off)
            time.sleep(0.5)

class ThreadCommandExecution_Tea(ThreadCommandExecution_Base):
    def __init__(self, name):
        super().__init__(name)

    def run(self):
        threading.Thread.run(self)
        for x in range(0, 2):
            send_command(command_on_tea)
            time.sleep(1.5)
            send_command(command_off)
            time.sleep(0.5)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/authorize')
def authorize():
    r = requests.post(hue_bridge_ip + '/api', data=command_authorize)
    return r.text

@app.route('/check')
def check():
    return 'Access is Authorized: ' + str(check_connected())

@app.route('/on')
def turn_on():
    r = requests.put(desk_lamp_uri_light_state, data=command_on)
    if r.status_code == 200:
        return 'turned on'
    else:
        return 'Failed to turn on'

@app.route('/off')
def turn_off():
    r = requests.put(desk_lamp_uri_light_state, data=command_off)
    if r.status_code == 200:
        return 'turned off'
    else:
        return 'Failed to turn off'

@app.route('/current')
def get_current():
    cur = get_current_state()
    return cur


@app.route('/standard')
def alert_fishes_standard():
    try:
        success = check_connected()
        if not success:
            raise Exception('Check connection failed')

        thread = ThreadCommandExecution_Standard('Standard Alert')
        thread.daemon = True
        thread.start()
        
        return render_template('success.html')
    except Exception as e:
        print(e)
        return 'Failed to alert fish...'

@app.route('/ping')
def alert_fishes_ping():
    try:
        success = check_connected()
        if not success:
            raise Exception('Check connection failed')

        thread = ThreadCommandExecution_Ping('Ping Alert')
        thread.daemon = True
        thread.start()

        return render_template('pinged.html')
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

        return render_template('anger.html')
    except Exception as e:
        print(e)
        return 'Failed to alert fish, he''s in even more trouble now...'

@app.route('/love')
def alert_fishes_love():
    try:
        success = check_connected()
        if not success:
            raise Exception('Check connection failed')

        thread = ThreadCommandExecution_Love('Love Alert')
        thread.daemon = True
        thread.start()

        return render_template('love.html')
    except Exception as e:
        print(e)
        return 'Failed to alert fish of your loves'

@app.route('/tea')
def alert_fishes_tea():
    try:
        success = check_connected()
        if not success:
            raise Exception('Check connection failed')

        thread = ThreadCommandExecution_Tea('Tea Alert')
        thread.daemon = True
        thread.start()

        return render_template('tea.html')
    except Exception as e:
        print(e)
        return 'Fish is missing out on some gossip'

@app.route('/lights')
def get_lights():
    r = requests.get(hue_bridge_ip + '/api/' + uuid + '/lights')
    return r.text

def check_connected():
    r = requests.get(hue_bridge_ip + '/api/' + uuid + '/lights')
    if 'error' in r.text:
        return False
    else:
        return True

def get_current_state():
    r = requests.get(desk_lamp_uri_light)
    if r.status_code == 200:
        obj = json.loads(r.text)['state']
        return json.dumps(obj)
    else:
        return ''

def send_command(command):
    r = requests.put(desk_lamp_uri_light_state, command)
    if r.status_code == 200:
        return True
    else:
        raise Exception('Command Failed', command)

if __name__ == "__main__":
    app.run()
