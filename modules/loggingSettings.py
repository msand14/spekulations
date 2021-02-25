import logging
from datetime import datetime
import os

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}
os.path.abspath(os.getcwd())

now = datetime.now()  # datetime object containing current date and time
# dd/mm/YY H:M:S
dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILENAME = os.path.join(os.path.dirname(__file__), '..', 'loggs', 'logging_' + dt_string + '.out')
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
)

logging.debug('Starting Logger')
