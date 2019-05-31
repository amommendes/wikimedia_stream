import sys
import os
from utils.logger import log
from service.consumer import Consumer
import argparse
import atexit

parser = argparse.ArgumentParser(prog="Wikimedia Stream Consumer", description="Simple wikimedia stream consumer")
parser.add_argument("--mode", 
help="""Output mode. Default is console, which prints messages to sysout. When file is desired it is necessary to pass
output path to file. Persist mode will write events to Elasticsearch.""", default="console", 
choices=["console", "file", "persist"], required=True)
parser.add_argument("-f", "--filter",default=None, help="""Filter to be executed on Wikimedia EventStream data based on regex. 
The regex pattern will be searched in all message, including all fields""")
parser.add_argument("-o","--output",default=None, help="Path to output file")

def finishMessage():
    """
    Message showed on app finishing
    """
    log.info ("Bye, bye")
    
atexit.register(finishMessage)

def main(parser):
    args = parser.parse_args()
    log.info(args)
    if (args.mode == "file") and (args.output == None):
       parser.error("--output should be specified with file mode")
    consumer = Consumer(mode=args.mode, output=args.output, userFilter=args.filter)
    consumer.streamEvents()

if __name__ == "__main__":
   main(parser)