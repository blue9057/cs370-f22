from gevent.pywsgi import WSGIServer
from CTFd import create_app

app = create_app()
http_server = WSGIServer(('127.0.0.1', 4000), app)
http_server.serve_forever()
