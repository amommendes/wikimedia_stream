import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.environment import Configuration
from db.connector import Connector

class Dao():
    def __init__(self, *args, **kwargs):
        self.db = Connector()
        self.conf = Configuration()

    @property
    def count(self):
        return self.db.es.count(index=self.conf.es_index)["count"]
    
    @property
    def sumLength(self):
        query={"aggs":{"sum_length":{"sum": {"field":"length.new"}}}}
        return int(self.db.es.search(index=self.conf.es_index, body=query)["aggregations"]["sum_length"]["value"])

    @property
    def countBySecond(self):
        query={"query":{"bool":{"filter":{"range":{"meta.dt":{"gte": "now-120s"}}}}},
               "aggs":{"edits_by_second":{"date_histogram":{
                                "field" : "meta.dt",
					           	"interval" : "1s",
                				"format" : "mm:ss"}}}}

        return (self.db.es.search(index=self.conf.es_index, body=query)["aggregations"]["edits_by_second"]["buckets"])

        