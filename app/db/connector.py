from elasticsearch import Elasticsearch
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.environment import Configuration
from utils.logger import log


class Connector:
    """
    This class is the interface with Elasticsearch
    """
    def __init__(self, *args, **kwargs):
        self.conf = Configuration()
        self.es = Elasticsearch(self.conf.es_host)
        self.index = self.conf.es_index

    def writeDocument(self, document):
        """
        Write data to Elasticsearch
        """
        self.es.index(index=self.conf.es_index, body=document)
