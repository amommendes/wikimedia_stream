from datetime import datetime
from elasticsearch import Elasticsearch
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.environment import Configuration
from utils.logger import log


class initElasticSearch():
    def __init__(self, *args, **kwargs):
        self.conf = Configuration()
        self.es = Elasticsearch(self.conf.es_host)
        
    def initIndex(self):
        """
        Init Elasticsearch index (database)
        """
        #TODO: Create Mappings to Recent Change Schema
        
        es_index=self.conf.es_index
        log.info("Initializing index: {}".format(es_index))
        try:
            self.es.indices.delete(index=es_index, ignore=[400, 404])
            log.info("Index {} deleted".format(es_index))
            log.info("Recreating index {}.".format(es_index))
            request_body={"settings" : {"number_of_shards" : self.conf.es_shards ,"number_of_replicas" : self.conf.es_replicas }}
            self.es.indices.create(index=es_index,body = request_body)
            log.info("Index {} recreated.".format(es_index))
        
        except Exception as error:
            log.error("Error while creating index {}.".format(es_index))
        

if __name__ == "__main__":
    initDb = initElasticSearch()
    initDb.initIndex()


    


