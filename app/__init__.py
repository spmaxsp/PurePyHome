import logging.config
import logging

from flask import Flask
import yaml



class App:
    def __init__(self) -> None:
        self.app = None
        self.socketio = None
        self.module_manager = None

    def create_app(self, debug: bool = False, config: str = "./config.yaml"):

        # Setup logging
        set_logger()

        # Initialize app
        self.app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/')
        self.app.logger.info('create_app::: Initializing app')

        # Setup app configs
        self.app.logger.info('create_app::: Loading config')
        load_config(self.app, debug, config)

        # Initialize entity handler
        self.app.logger.info('create_app::: Initializing entity handler')
        from app.entity_handler import entity_handler
        entity_handler.init_app(self.app)

        # Load entities
        self.app.logger.info('create_app::: Loading entities')
        for yaml_file in self.app.config['ENTITIES']:
            entity_handler.open_entity_yaml(yaml_file)

        # Initialize database
        self.app.logger.info('create_app::: Initializing database')
        from app.entity_db import db, entity_data_base
        db.init_app(self.app)
        entity_data_base.init_app(self.app)

        # Build database
        self.app.logger.info('create_app::: Building database')
        entity_data_base.init_db()
        entity_data_base.build_db(entity_handler.get_all_entities())

        # Initialize module manager
        self.app.logger.info('create_app::: Initializing module manager')
        
        from app.modules import ModuleManager
        self.module_manager = ModuleManager()
        self.module_manager.init_modules(self.app, entity_handler)

        # Initialize mqtt
        #app.logger.info('create_app::: Initializing mqtt')
        #from app.mqtt import mqtt, mqtt_data_subscriber, mqtt_data_publisher
        #mqtt.init_app(app)
        #mqtt_data_subscriber.init_app(app)
        #mqtt_data_publisher.init_app(app)

        # Build mqtt data subscriber map
        #app.logger.info('create_app::: Building mqtt data subscriber map')
        #mqtt_data_subscriber.build_map(entity_handler.get_all_entities())
        #app.logger.info('create_app::: Building mqtt data publisher map')
        #mqtt_data_publisher.build_map(entity_handler.get_all_entities())

        # Initialize socketio
        self.app.logger.info('create_app::: Initializing socketio')
        from app.ui_socketio import socketio, dashboard_data_publisher, dashboard_data_subscriber
        self.socketio = socketio
        self.socketio.init_app(self.app)
        dashboard_data_publisher.init_app(self.app)
        dashboard_data_subscriber.init_app(self.app)
        for ui_elem in self.app.config['UI_PAGES']:
            print(ui_elem)
            print(self.app.config['UI_PAGES'][ui_elem])
            if self.app.config['UI_PAGES'][ui_elem]['type'] == 'dashboard':
                dashboard_data_publisher.build_map_from_layout_yaml(self.app.config['UI_PAGES'][ui_elem]['layout'])
                dashboard_data_subscriber.build_map_from_layout_yaml(self.app.config['UI_PAGES'][ui_elem]['layout'])
        
        # Import and register blueprints
        self.app.logger.info('create_app::: Registering blueprints')
        from app.ui_blueprints import ui_blueprints
        self.app.register_blueprint(ui_blueprints)



LOG_LEVEL_COLORS = {
    logging.DEBUG: '\033[94m',    # Blue
    logging.INFO: '\033[92m',     # Green
    logging.WARNING: '\033[93m',  # Yellow
    logging.ERROR: '\033[91m',    # Red
    logging.CRITICAL: '\033[91m'   # Red
}

LOGGER_COLORS = {
    'app': '\033[32m',  # Green
    'eventlet.wsgi': '\033[36m',  # Cyan
    'eventlet.wsgi.http': '\033[33m',  # Yellow
    'flask_mqtt': '\033[35m',  # Magenta
    'flask_socketio': '\033[35m',  # Magenta
    'flask_sqlalchemy': '\033[35m'  # Magenta
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_level_color = LOG_LEVEL_COLORS.get(record.levelno, '\033[0m')
        logger_name_color = LOGGER_COLORS.get(record.name, '\033[0m')
        
        formatted_message = f"{logger_name_color}[{record.name}]{log_level_color}[{record.levelname}]\033[0m {record.msg}"
        return formatted_message


def set_logger() -> None:

    # Setup logging: create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(ColoredFormatter())

    # ROOT logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)

    # Flask logger
    app_logger = logging.getLogger('app')
    app_logger.setLevel(logging.DEBUG)
    app_logger.addHandler(console_handler)

    # Eventlet logger
    eventlet_wsgi_logger = logging.getLogger('eventlet.wsgi')
    eventlet_wsgi_logger.setLevel(logging.DEBUG)
    eventlet_wsgi_logger.addHandler(console_handler)

    eventlet_wsgi_http_logger = logging.getLogger('eventlet.wsgi.http')
    eventlet_wsgi_http_logger.setLevel(logging.DEBUG)
    eventlet_wsgi_http_logger.addHandler(console_handler)

    # Imported Flask modules
    mqtt_logger = logging.getLogger('flask_mqtt')
    mqtt_logger.setLevel(logging.DEBUG)
    mqtt_logger.addHandler(console_handler)

    socketio_logger = logging.getLogger('socketio')
    socketio_logger.setLevel(logging.DEBUG)
    socketio_logger.addHandler(console_handler)

    sqlalchemy_logger = logging.getLogger('sqlalchemy')
    sqlalchemy_logger.setLevel(logging.WARNING)
    sqlalchemy_logger.addHandler(console_handler)

    app_logger.propagate = False
    eventlet_wsgi_logger.propagate = False
    eventlet_wsgi_http_logger.propagate = False
    mqtt_logger.propagate = False
    socketio_logger.propagate = False
    sqlalchemy_logger.propagate = False


def load_config(app: Flask, debug: bool, config_path: str) -> None:
    # Load config file
    app.logger.info(f'load_config: Loading config from: {config_path}')
    try:
        with open(config_path, 'r') as f:
            config_raw = f.read()
            config = yaml.safe_load(config_raw)
    except Exception as e:
        error_message = f'Error reading file: {e}'
        app.logger.error(error_message) 

    # Parse config file
    try:
        app.config['DEBUG'] = debug
        app.config['SECRET'] = 'my secret key'

        app.config['MQTT_BROKER_URL']   = config['mqtt']['broker_url']
        app.config['MQTT_BROKER_PORT']  = config['mqtt']['broker_port']
        app.config['MQTT_USERNAME']     = config['mqtt']['username']
        app.config['MQTT_PASSWORD']     = config['mqtt']['password']
        app.config['MQTT_KEEPALIVE']    = config['mqtt']['keepalive']
        app.config['MQTT_TLS_ENABLED']  = config['mqtt']['tls_enabled']

        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        app.config['UI_PAGES']       = config['ui']

        app.config['ENTITIES']       = config['entities']
    except Exception as e:
        error_message = f'Error parsing config: {e}'
        app.logger.error(error_message)
