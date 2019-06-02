import sys, os
import logging 

_LOG_LEVEL = 'INFO'

class Logging(object):
    """
    Class with logging utilities
    
    """
    def __init__(self, mode):
        log_level = getattr(logging, mode)
        logging.basicConfig(level=log_level, format='%(asctime)s: Wikimedia-StreamApp %(message)s')
        self.logger = logging.getLogger("")
        logging.getLogger().setLevel(log_level)

    def debug(self, msg):
        log_msg = ': [DEBUG] {}'.format(msg)
        self.logger.debug(log_msg)

    def info(self, msg):
        log_msg = ': [INFO] {}'.format(msg)
        self.logger.info(log_msg)

    def warn(self, msg):
        log_msg = ': [WARN] {}'.format(msg)
        self.logger.warn(log_msg)

    def error(self, msg):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        error_detail = "[DETAIL] filename: {} line: {}".format(fname, exc_tb.tb_lineno)
        log = ': [ERROR] {} {}'.format(msg, error_detail)
        self.logger.error(log)
  
log = Logging(_LOG_LEVEL)