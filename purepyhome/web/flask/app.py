

from purepyhome.core.db.sqlalchemy import db
from purepyhome.core.db.entity_db import entity_db
from purepyhome.core.mqtt import mqtt
from purepyhome.core.socketio import socketio
from purepyhome.core.logger import setup_logger, get_logger

from purepyhome.core.core import create_entity
from purepyhome.core.data_types.creation_info import EntityCreationInfo, EntityDataSinkInfo, EntityDataSourceInfo

from purepyhome.modules.mqtt.mqtt_subscriber import mqtt_subscriber
from purepyhome.modules.mqtt.mqtt_publisher import mqtt_publisher
from purepyhome.modules.ui.io_emitter import ui_io_emitter
from purepyhome.modules.ui.io_receiver import ui_io_receiver
from purepyhome.modules.actions.actions_manager import actions_manager

from purepyhome.web.flask.ui_blueprints import ui_blueprints

from flask import Flask

import yaml

logger = get_logger()

def configure_app(app, config_path='./config.yaml'):
    """ Configure the app: Loads the configuration file and loads it into the app config

    Args:
        app (Flask): The Flask app object
    Returns:
        None
    """

    # Load config file
    logger.info(f'load_config: Loading config from: {config_path}')

    try:
        with open(config_path, 'r') as f:
            config_raw = f.read()
            config = yaml.safe_load(config_raw)
    except Exception as e:
        app.logger.error("Error reading file: {e}")

    # Parse config file
    try:
        app.config['DEBUG'] = True
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
        logger.error(f'Error reading values from config: {e}')


def setup_blueprints(app):
    """ Setup the templates

    Args:
        app (Flask): The Flask app object
    Returns:
        None
    """

    app.register_blueprint(ui_blueprints)


def setup_db(app):
    """ Setup the database

    Args:
        app (Flask): The Flask app object
    Returns:
        None
    """

    # Drop all tables and create new ones
    with app.app_context():
        db.drop_all()
        db.create_all()  


def setup_entities(app):
    """ Setup the entities reads all entity yaml files and registers the entities via the signal

    Args:
        app (Flask): The Flask app object
    Returns:
        None
    """

    for yaml_file in app.config['ENTITIES']:
        with open(yaml_file, 'r') as file:
            entities = yaml.safe_load(file)
            for entity_id in entities:
                entity = entities[entity_id]

                creation_info = EntityCreationInfo(
                    entity_id=entity_id,
                    device_type=entity['device_type'],
                    data_type=entity['data_type'],
                    history_depth=0,
                    data_sink=None,
                    data_source=None,
                    node_red_mqtt_link=False,
                    actions={}
                )

                if 'history_depth' in entity:
                    creation_info.history_depth = entity['history_depth']
                
                if 'data_sink' in entity and len(entity['data_sink'].keys()) > 0:
                    data_sink_type = next(iter(entity['data_sink']))
                    creation_info.data_sink = EntityDataSinkInfo(
                        sink_type=data_sink_type,
                        sink_info=entity['data_sink'][data_sink_type],
                        conversion_type="",
                        conversion_str=""
                    )
                    if 'conversion_type' in entity['data_sink'][data_sink_type]:
                        creation_info.data_sink.conversion_type = entity['data_sink'][data_sink_type]['conversion_type']
                    if 'conversion_str' in entity['data_sink'][data_sink_type]:
                        creation_info.data_sink.conversion_str = entity['data_sink'][data_sink_type]['conversion_str']
                else:
                    creation_info.data_sink = EntityDataSinkInfo(
                        sink_type='none',
                        sink_info=None,
                        conversion_type="",
                        conversion_str=""
                    )

                if 'data_source' in entity and len(entity['data_source'].keys()) > 0:
                    data_source_type = next(iter(entity['data_source']))
                    creation_info.data_source = EntityDataSourceInfo(
                        source_type=data_source_type,
                        source_info=entity['data_source'][data_source_type],
                        conversion_type="",
                        conversion_str=""
                    )
                    if 'conversion_type' in entity['data_source'][data_source_type]:
                        creation_info.data_source.conversion_type = entity['data_source'][data_source_type]['conversion_type']
                    if 'conversion_str' in entity['data_source'][data_source_type]:
                        creation_info.data_source.conversion_str = entity['data_source'][data_source_type]['conversion_str']
                else:
                    creation_info.data_source = EntityDataSourceInfo(
                        source_type='none',
                        source_info=None,
                        conversion_type="",
                        conversion_str=""
                    )

                if 'node_red_mqtt_link' in entity:
                    creation_info.node_red_mqtt_link = entity['node_red_mqtt_link']

                if 'actions' in entity:
                    creation_info.actions = entity['actions']

                create_entity(creation_info)


def init_app(debug=False):
    """ Initialize the app

    Args:
        debug (bool): Debug flag
    Returns:
        Flask: The Flask app object
    """

    setup_logger()

    app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/')

    configure_app(app)

    db.init_app(app)
    mqtt.init_app(app)
    socketio.init_app(app)

    entity_db.init_app(app)

    setup_db(app)

    setup_entities(app)

    entity_db.dbg_printout_db()

    setup_blueprints(app)
    
    return app

    