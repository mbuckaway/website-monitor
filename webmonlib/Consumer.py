from webmonlib.Config import Config
from webmonlib.URLItem import URLItem
from webmonlib.Database import Database
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import os
import logging
import jsonpickle

class Consumer:
    '''
    Consumer class. Setup and maintains the connection to the remote Kafka server.
    '''
    def __init__(self, config:Config):
        '''
        Initialize. cafile, certfile, and keyfile are required auth files.
        '''
        self.config = config
        self.consumer = None
        self.connected = False
        self.logging = logging.getLogger(__name__)

        if not os.path.exists(self.config.KAFKA_CAFILE):
            raise FileNotFoundError(f"CA file not found: {self.config.KAFKA_CAFILE}")
        if not os.path.exists(self.config.KAFKA_CERTFILE):
            raise FileNotFoundError(f"Cert file not found: {self.config.KAFKA_CERTFILE}")
        if not os.path.exists(self.config.KAFKA_KEYFILE):
            raise FileNotFoundError(f"Key file not found: {self.config.KAFKA_KEYFILE}")

    def Connect(self):
        '''
        Connect to remote Kafka server as a Consumer
        '''
        self.consumer = KafkaConsumer(self.config.KAFKA_TOPIC,
                    bootstrap_servers=[self.config.KAFKA_HOST],
                    security_protocol="SSL",
                    ssl_cafile=self.config.KAFKA_CAFILE,
                    ssl_certfile=self.config.KAFKA_CERTFILE,
                    ssl_keyfile=self.config.KAFKA_KEYFILE,
                    consumer_timeout_ms=3000,
                    )
        self.connected = True

    def __del__(self):
        if self.connected:
            self.consumer.close()
            self.connected = False

    @property
    def IsConnected(self):
        return self.connected

    def GetData(self, database:Database=None):
        '''
        Get data from the consume, and if we have something, we store it in the database
        '''
        if not self.connected:
            raise ConnectionError("Not connected to Kafka server")
        self.logging.debug("Getting data...")
        for msg in self.consumer:
            pickled = msg.value
            object = None
            try:
                object = jsonpickle.decode(pickled)
            except:
                self.logging.error(f"Unable to decode message: {pickled}")
            if object:
                # For testing, we allow the database object to be None
                if database:
                    database.InsertData(object)
                else:
                    self.warning("Database not defined: Data not stored")
                self.logging.info(f"Recieved and stored: {object.Url} {object.ReactionTime} {object.Success}")
