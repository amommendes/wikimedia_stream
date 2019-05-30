import os
from yaml import load
from utils.logger import log

class Configuration: 
    """
    Object with configuration properties read from app_config.yml file
    """
    def __init__(self, topic="WIKIMEDIA"):
        try:
            filePath = os.path.dirname(__file__) + '/app_config.yml'
            log.info('Loading configuration file in the path: %s' % filePath)
            with open(filePath) as cfg:
                config = load(cfg)
            list(map(lambda conf: self.__dict__.update(config.get(conf)), [topic]))
            log.info("Configuration file successfully loaded: %s" % self.__dict__)
        except IOError as err: 
            log.info('Config file not found: %s' % str(err))

    
    @property
    def confs(self):
        return self.__dict__