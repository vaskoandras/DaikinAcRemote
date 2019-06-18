from flask_app import app
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()