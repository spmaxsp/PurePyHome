import eventlet

#eventlet.monkey_patch()

from app import App
import logging

class WSGILog(object):

    def __init__(self):
        self.log = logging.getLogger("eventlet.wsgi")
        self.log_http = logging.getLogger("eventlet.wsgi.http")

    def write(self, string):
        if "GET" in string or "POST" in string:
            string = string.split("\"")[1]
            self.log_http.debug(string.rstrip("\n"))
        else:
            self.log.debug(string.rstrip("\n"))

app = App()

app.create_app(debug=True, config='./config.yaml')

if __name__ == '__main__':
    #socketio.run(app, use_reloader=False, debug=True, log_output=True)
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app.app, log_output=True, log=WSGILog())