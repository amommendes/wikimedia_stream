import json
from sseclient import SSEClient as EventSource
from config.config import Configuration
from utils.logger import log
import re
from utils.utils import get_mseconds

class Consumer():
    """
        Consumer Class: request and return event messages
    """
    def __init__(self, filter="non-robot", mode="console", output=None, userFilter=None ):
        self.filter = filter
        self.conf = Configuration()
        self.url = self.conf.url + "?query%3Dsince%3D%3D{}".format(str(get_mseconds()))
        self.output = output
        self.mode = mode
        self.userFilter = userFilter

    def streamEvents(self):
        """
        Get events from api
        """
        for event in EventSource(self.url):
            if event.event == 'message':
                try:
                    message = json.loads(event.data)
                except ValueError:
                    pass
                else:
                    if self.setFilter(message):
                        self.outputStream(message)
                    else:
                       pass
    def outputStream(self, message):
        """
        Write output streams to user option mode
        """
        if self.mode == "file" and self.output:
            with open (self.output, "a+") as file:
                file.write(json.dumps(message, indent=4))
                file.write(",")

        else: 
            log.info("Message: \n{}".format(json.dumps (message, indent=4) ))
    
    def setFilter(self, message):
        """
        Set filter based on user input
        """
        if self.userFilter == None:
            return message["bot"] == False
        elif ( (self.userFilter is not None) and (re.match(str(self.userFilter), str(message))) ):
            return True
        else:
            return False
            
        
if __name__ == "__main__":
    consumer = Consumer()
    consumer.getEvents()
