
from flask_mqtt import Mqtt as FlaskMqtt

class PurePyHomeMqtt(FlaskMqtt):
    """ Custom MQTT class for PurePyHome

    This class is a custom Wrapper around the Flask MQTT class.
    It can be used to add custom functionality to the Flask MQTT class if needed.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

mqtt = PurePyHomeMqtt(connect_async=True)
