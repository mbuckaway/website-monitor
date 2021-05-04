from webmonlib.Config import Config
from webmonlib.URLItem import URLItem
from kafka import KafkaProducer
from kafka.errors import KafkaError
import os
import jsonpickle
import logging

class Producer:
    '''
    Producer class. Setup and maintains the connection to the remote Kafka server. We assume
    the user has created the topic on the server already. Without a topic, SendData will fail.
    '''
    def __init__(self, config:Config):
        self.config = config
        self.producer = None
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
        self.producer = KafkaProducer(bootstrap_servers=[self.config.KAFKA_HOST],
                    security_protocol="SSL",
                    ssl_cafile=self.config.KAFKA_CAFILE,
                    ssl_certfile=self.config.KAFKA_CERTFILE,
                    ssl_keyfile=self.config.KAFKA_KEYFILE,
                    )
        self.connected = True

    def __del__(self):
        if self.connected:
            self.producer.close()
            self.connected = False

    @property
    def IsConnected(self):
        return self.connected

    def SendData(self, item: URLItem):
        '''
        Encode out data item and send it to Kafka
        '''
        if not self.connected:
            raise ConnectionError("Not connected: Use Connect to establish the connect prior to send")

        value_bytes = bytes(jsonpickle.encode(item), encoding='utf-8')
        self.producer.send(self.config.KAFKA_TOPIC, value=value_bytes)
        self.producer.flush()
        self.logging.info(f"Sent message to topic: {self.config.KAFKA_TOPIC}")
