import os
import logging
import traceback
import json

import structlog
from google.cloud import logging as cloudlogging
from google.cloud.logging.handlers import CloudLoggingHandler


def add_traceback(logger, method_name, event_dict):
    # Extract the traceback information
    trace = traceback.format_exc()
    # Add the traceback information to the log event dictionary
    event_dict['traceback'] = trace
    return event_dict


def configure_struct_log_prod():
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.render_to_log_kwargs,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def configure_struct_log_dev():
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(
                fmt="%Y-%m-%d %H:%M:%S", utc=True),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
    )


def configure_struct_log(is_prod: bool):
    if is_prod:
        configure_struct_log_prod()
    else:
        configure_struct_log_dev()


def setup(log_name=None):
    env_setup = os.getenv('SETUP', 'prod')
    is_prod_env = env_setup.lower() == "prod"
    configure_struct_log(is_prod_env)

    if not is_prod_env:
        return

    if log_name is None:
        try:
            import __main__
            log_name = __main__.__loader__.name.split('.')[0]
        except:
            pass

    # Set up the Cloud Logging client
    client = cloudlogging.Client()

    # Set up the Python logging handler
    handler = client.get_default_handler()

    # Add handler to the root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
