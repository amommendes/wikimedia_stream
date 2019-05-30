import sys
import os
from utils.logger import log
from service.consumer import Consumer
import argparse
import atexit

parser = argparse.ArgumentParser(prog="Wikimedia Stream Consumer", description="Simple wikimedia stream consumer")
parser.add_argument("--mode", help="Output mode", default="console", choices=["console", "file", "persist"], required=True)
parser.add_argument("-f", "--filter",default=None, help="Filter to be executed on Wikimedia EventStream data (Regex)")
parser.add_argument("-o","--output",default=None, help="Path to output file")

def finishMessage():
    """
    Message showed on app finishing
    """
    log.info ("Application finished")
    
atexit.register(finishMessage)

if __name__ == "__main__":
    args = parser.parse_args()
    log.info(args)
    if (args.mode == "file") and (args.output == None):
       parser.error("--output should be specified with file mode")
    consumer = Consumer(mode=args.mode, output=args.output, userFilter=args.filter)
    consumer.streamEvents()
