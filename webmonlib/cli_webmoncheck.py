import argparse
import sys
import logging
import traceback
from webmonlib.Producer import Producer
import requests
import time
import json
import jsonpickle
import os
from webmonlib.Config import Config
from webmonlib.URLItem import URLItem
from kafka import KafkaProducer
from kafka.errors import KafkaError

def webmonitor():
    '''
    Connect to Kafka as a producer, and loop over the website we want to monitor checking every X seconds, and
    publishing the data.
    '''
    parser = argparse.ArgumentParser(description='Website Monitor Checker (Producer)')
    parser.add_argument('-u', '--url', required=True, help='Url to check')
    parser.add_argument('-t', '--timeout', default=2, type=int, help='Timeout for URL check (default 2 seconds)')
    parser.add_argument('-c', '--checktime', default=10, type=int, help='Check every xx seconds (default 10 seconds)')
    parser.add_argument('-e', '--envfile', default=".env", help='env file to load config')

    args = parser.parse_args()

    if not os.path.exists(args.envfile):
        raise FileNotFoundError(f"envfile does not exist: {args.envfile}")

    config = Config(args.envfile)

    producer = Producer(config)
    producer.Connect()

# Reference
# https://stackoverflow.com/questions/43252542/how-to-measure-server-response-time-for-python-requests-post-request#43260678

    # Run a check of the website. We make an assumption that status code 200 is a successful connect and anything else is an error
    # which may or may not be the case
    # Improvements:
    # - store the status code and error with the data
    # - check for a regex in the website to ensure we get back valid data
    checktime = int(args.checktime)
    timeout = int(args.timeout)
    while (1):
        success = False
        responsetime = 0.0
        error = ""
        try:
            response = requests.get(args.url, timeout=timeout)
            success = (response.status_code==200)
            responsetime = response.elapsed.total_seconds()
        except Exception as e:
            error = str(e)

        if success:
            logging.info(f"{args.url} response time: {responsetime}")
        else:
            logging.warning(f"{args.url} failed: {error}")
        item = URLItem(url=args.url, reactiontime=responsetime, success=success)
        producer.SendData(item)
        logging.info("Message sent")
        time.sleep(checktime)

def main():
    try:
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

        webmonitor()
    except KeyboardInterrupt as e:
        logging.error("User/System requested abort")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}")
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
