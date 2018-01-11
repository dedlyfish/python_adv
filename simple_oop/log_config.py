import logging
import logging.handlers
import sys
import inspect

def log(foo):
    def wrapper(*args, **kwargs):
            server_log.info('Called function {} from {}'.format(foo.__name__, inspect.stack()[1][3]))
            return foo(*args, **kwargs)
    return wrapper


format = logging.Formatter('%(asctime)s:%(levelname)s:%(module)s:%(message)s')

crit_handler = logging.StreamHandler(sys.stderr)
crit_handler.setLevel(logging.CRITICAL)
crit_handler.setFormatter(format)

info_handler = logging.handlers.TimedRotatingFileHandler('messanger.log', when='D')
info_handler.setFormatter(format)

server_log = logging.getLogger('server')
server_log.setLevel(logging.INFO)
server_log.addHandler(crit_handler)
server_log.addHandler(info_handler)
