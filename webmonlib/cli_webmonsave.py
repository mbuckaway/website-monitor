import argparse
import sys
import logging
from webmonlib.Config import Config
from webmonlib.Consumer import Consumer
from webmonlib.Database import Database
import os

def webmonreader():
    '''
    webmonreader - parse the command line, connect to Kafka as a consumer, init the database connection,
    and wait for data. Any received data is stored in the database
    '''
    parser = argparse.ArgumentParser(description='Website Monitor Save (Consumer)')
    parser.add_argument('-e', '--envfile', default=".env", help='env file to load config')

    args = parser.parse_args()
    
    if not os.path.exists(args.envfile):
        raise FileNotFoundError(f"envfile does not exist: {args.envfile}")

    config = Config(args.envfile)

    consumer = Consumer(config)
    consumer.Connect()

    database = Database(config)
    database.Connect()
    database.CreateDatabase()

    logging.info("Connected and waiting for data...")
    while (1):
        consumer.GetData(database)

def main():
    try:
        root = logging.getLogger()
        root.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

        webmonreader()
    except KeyboardInterrupt as e:
        logging.error("User/System requested abort")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}")
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
