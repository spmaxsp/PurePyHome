
from flask_socketio import SocketIO

class PurePyHomeSocketIO(SocketIO):
    """ Custom SocketIO class for PurePyHome

    This class is a custom Wrapper around the Flask SocketIO class.
    It can be used to add custom functionality to the Flask SocketIO class if needed.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

socketio = PurePyHomeSocketIO()