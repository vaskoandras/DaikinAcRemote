from config import Config
import os
from flask import Flask
from flask import jsonify, request
from flask import render_template
from peewee import *

app = Flask(__name__)
app.config.from_object(Config)

db = SqliteDatabase('data.db')
db.connect()

class AcData(Model):
    key = TextField()
    value = TextField()

    class Meta:
        database = db
        db_table = 'acdata'

AcData.create_table()

@app.route('/get/<key>')
def get_key(key):
    item = AcData.get_or_none(key=key)
    if item:
       item = item.value

    return jsonify(item)

def get_config_json():
    ac_on, _ = AcData.get_or_create(key='ac_on', defaults={'value': '0'})
    temp, _ = AcData.get_or_create(key='temperature', defaults={'value': '22'})
    mode, _ = AcData.get_or_create(key='mode', defaults={'value': 'auto'})
    swing, _ = AcData.get_or_create(key='swing', defaults={'value': '1'})
    fan_mode, _ = AcData.get_or_create(key='fan_mode', defaults={'value': 'auto'})
    eco, _ = AcData.get_or_create(key='is_eco', defaults={'value': '0'})
    powerful, _ = AcData.get_or_create(key='is_powerful', defaults={'value': '0'})
    comfort, _ = AcData.get_or_create(key='comfort', defaults={'value': '0'})
    return {
        'ac_on':ac_on.value,
        'temperature': temp.value,
        'mode': mode.value,
        'swing': swing.value,
        'fan_mode': fan_mode.value,
        'eco': eco.value,
        'powerful': powerful.value,
        'comfort': comfort.value
    }

@app.route('/get_config')
def get_config():
    return jsonify(get_config_json())

@app.route('/set_config', methods = ['POST'])
def set_config():
    json = request.get_json()

    ac_on = json.get("ac_on", None)
    if ac_on is not None:
        query = AcData.update(value=ac_on).where(AcData.key == 'ac_on')
        query.execute()
    temp = json.get("temp", None)
    if temp is not None:
        query = AcData.update(value=temp).where(AcData.key == 'temp')
        query.execute()
    mode = json.get("mode", None)
    if mode is not None:
        query = AcData.update(value=mode).where(AcData.key == 'mode')
        query.execute()
    swing = json.get("swing", None)
    if swing is not None:
        query = AcData.update(value=swing).where(AcData.key == 'swing')
        query.execute()
    fan_mode = json.get("fan_mode", None)
    if fan_mode is not None:
        query = AcData.update(value=fan_mode).where(AcData.key == 'fan_mode')
        query.execute()
    eco = json.get("eco", None)
    if eco is not None:
        query = AcData.update(value=eco).where(AcData.key == 'eco')
        query.execute()
    powerful = json.get("powerful", None)
    if powerful is not None:
        query = AcData.update(value=powerful).where(AcData.key == 'powerful')
        query.execute()
    comfort = json.get("comfort", None)
    if comfort is not None:
        query = AcData.update(value=comfort).where(AcData.key == 'comfort')
        query.execute()

    print(get_config_json())
    return jsonify(get_config_json())

@app.route('/')
def hello():
    ac_on, _ = AcData.get_or_create(key='ac_on', defaults={'value': '0'})
    temp, _ = AcData.get_or_create(key='temperature', defaults={'value': '22'})
    mode, _ = AcData.get_or_create(key='mode', defaults={'value': 'auto'})
    swing, _ = AcData.get_or_create(key='swing', defaults={'value': '1'})
    fan_mode, _ = AcData.get_or_create(key='fan_mode', defaults={'value': 'auto'})
    eco, _ = AcData.get_or_create(key='is_eco', defaults={'value': '0'})
    powerful, _ = AcData.get_or_create(key='is_powerful', defaults={'value': '0'})
    comfort, _ = AcData.get_or_create(key='comfort', defaults={'value': '0'})
    return render_template("base.html")

if __name__ == '__main__':
    app.run()
