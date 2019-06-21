from config import Config
from flask import Flask
from flask import jsonify, request
from flask import render_template
from peewee import *
import set_ac

app = Flask(__name__)
app.config.from_object(Config)

db = MySQLDatabase(
    app.config.get('DB_DB'),
    host=app.config.get('DB_HOST'),
    port=3306,
    user=app.config.get('DB_USERNAME'),
    passwd=app.config.get('DB_PASSWORD')
)
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
    temperature, _ = AcData.get_or_create(key='temperature', defaults={'value': '22'})
    mode, _ = AcData.get_or_create(key='mode', defaults={'value': 'auto'})
    swing, _ = AcData.get_or_create(key='swing', defaults={'value': '1'})
    fan_mode, _ = AcData.get_or_create(key='fan_mode', defaults={'value': 'auto'})
    eco, _ = AcData.get_or_create(key='eco', defaults={'value': '0'})
    powerful, _ = AcData.get_or_create(key='powerful', defaults={'value': '0'})
    comfort, _ = AcData.get_or_create(key='comfort', defaults={'value': '0'})
    return {
        'ac_on':ac_on.value,
        'temperature': temperature.value,
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

    # Parse json
    ac_on = json.get("ac_on", None)
    if ac_on is not None:
        query = AcData.update(value=ac_on).where(AcData.key == 'ac_on')
        query.execute()
    temperature = json.get("temperature", None)
    if temperature is not None:
        query = AcData.update(value=temperature).where(AcData.key == 'temperature')
        query.execute()
    mode = json.get("mode", None)
    if mode is not None:
        query = AcData.update(value=mode).where(AcData.key == 'mode')
        query.execute()
    fan_mode = json.get("fan_mode", None)
    if fan_mode is not None:
        query = AcData.update(value=fan_mode).where(AcData.key == 'fan_mode')
        query.execute()
    swing = json.get("swing", None)
    if swing is not None:
        query = AcData.update(value=swing).where(AcData.key == 'swing')
        query.execute()
    eco = json.get("eco", None)
    if eco is not None:
        query = AcData.update(value=eco).where(AcData.key == 'eco')
        query.execute()
    powerful = json.get("powerful", None)
    if powerful is not None:
        if powerful:
            query = AcData.update(value='auto').where(AcData.key == 'fan_mode')
            query.execute()
            query = AcData.update(value=0).where(AcData.key == 'comfort')
            query.execute()
        query = AcData.update(value=powerful).where(AcData.key == 'powerful')
        query.execute()
    comfort = json.get("comfort", None)
    if comfort is not None:
        if comfort:
            query = AcData.update(value=0).where(AcData.key == 'swing')
            query.execute()
            query = AcData.update(value=0).where(AcData.key == 'powerful')
            query.execute()
            query = AcData.update(value='auto').where(AcData.key == 'fan_mode')
            query.execute()
        query = AcData.update(value=comfort).where(AcData.key == 'comfort')
        query.execute()

    # Set AC
    ac_config = get_config_json()
    set_ac.set_ac(
        ac_config['ac_on'],
        ac_config['temperature'],
        ac_config['mode'],
        ac_config['fan_mode'],
        ac_config['swing'],
        ac_config['eco'],
        ac_config['powerful'],
        ac_config['comfort'],
        0,
        0,
    )

    return jsonify(ac_config)


@app.route('/')
def hello():
    return render_template("base.html")


if __name__ == '__main__':
    app.run(debug=True)
