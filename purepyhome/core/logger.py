import logging

LOG_LEVEL_COLORS = {
    logging.DEBUG: '\033[94m',    # Blue
    logging.INFO: '\033[92m',     # Green
    logging.WARNING: '\033[93m',  # Yellow
    logging.ERROR: '\033[91m',    # Red
    logging.CRITICAL: '\033[91m'   # Red
}

LOGGER_COLORS = {
    'purepyhome': '\033[32m',  # Green
    'eventlet.wsgi': '\033[36m',  # Cyan
    'eventlet.wsgi.http': '\033[33m',  # Yellow
    'flask_mqtt': '\033[35m',  # Magenta
    'flask_socketio': '\033[35m',  # Magenta
    'flask_sqlalchemy': '\033[35m'  # Magenta
}


class PurePyHomeLoggerFormatter(logging.Formatter):
    """ Custom logging formatter for PurePyHome

    """

    def format(self, record):
        log_level_color = LOG_LEVEL_COLORS.get(record.levelno, '\033[0m')

        if record.name.startswith('purepyhome'):
            logger_name_color = LOGGER_COLORS['purepyhome']
        else:
            logger_name_color = LOGGER_COLORS.get(record.name, '\033[0m')
        
        formatted_message = f"{logger_name_color}[{record.name}]{log_level_color}[{record.levelname}]\033[0m {record.msg}"
        return formatted_message


def setup_logger():
    """Setup the logger for PurePyHome
    
    Args:
        None
    Returns:
        None
    """
    
    # Setup logging: create console handler
    console_handler = logging.StreamHandler()

    # Set global log level
    console_handler.setLevel(logging.DEBUG)

    # Set custom formatter
    console_handler.setFormatter(PurePyHomeLoggerFormatter())


    # ROOT logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)

    # Flask logger
    app_logger = logging.getLogger('app')
    app_logger.setLevel(logging.DEBUG)
    app_logger.addHandler(console_handler)

    # Application logger
    application_logger = logging.getLogger('purepyhome')
    application_logger.setLevel(logging.DEBUG)
    application_logger.addHandler(console_handler)

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
    application_logger.propagate = False
    eventlet_wsgi_logger.propagate = False
    eventlet_wsgi_http_logger.propagate = False
    mqtt_logger.propagate = False
    socketio_logger.propagate = False
    sqlalchemy_logger.propagate = False


def get_logger() -> logging.Logger:
    """Get the main logger for PurePyHome

    Args:
        None
    Returns:
        logging.Logger: The main logger for PurePyHome
    """

    logger = logging.getLogger('purepyhome')
    logger.setLevel(logging.DEBUG)
    return logger


def get_module_logger(module_name: str) -> logging.Logger:
    """Get a logger for a module in PurePyHome. A simple helper function to prepend "purepyhome." to the module name

    Args:
        module_name (str): The name of the module
    Returns:
        logging.Logger: The logger for the module
    """
    module_name = module_name.split('.')[-1]

    logger_name = f'purepyhome.module.{module_name}'

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    return logger