import os
import unittest
from webmonlib.Config import Config
from webmonlib.URLItem import URLItem
from webmonlib.Consumer import Consumer
from webmonlib.Producer import Producer
import logging
import sys

class TestProducerConsumerMethods(unittest.TestCase):
    def setUp(self):
        self.config = Config(".env.test")

    def tearDown(self):
        pass

    @unittest.skip("Comment me out to enable")
    def test_producer(self):
        '''
        Setup a test to connect the remove server, send a message, and close the connection. We assume the topic has already been created.
        This is more a function test, but it tests the plumbing of sending the message.
        '''
        success = False
        producer = Producer(self.config)
        self.assertIsNotNone(producer)
        success = False
        try:
            producer.Connect()
            success = True
        except Exception as e:
            logging.error(F"Failed to send: {str(e)}")

        self.assertTrue(success)
        self.assertTrue(producer.IsConnected)

        item = URLItem("www.google.com", 0.0143234, True)
        success = False
        try:
            producer.SendData(item)
            success = True
        except Exception as e:
            logging.error(F"Failed to send: {str(e)}")
        
        self.assertTrue(success)

        del producer

    #@unittest.skip("Comment me out to enable")
    def test_consumer(self):
        '''
        Setup a test to connect the remove server, get messages, and close the connection. We assume the topic has already been created.
        This is more a function test, but it tests the plumbing of sending the message. No database connection is used, so any data received
        will not be stored.
        '''
        success = False
        consumer = Consumer(self.config)
        self.assertIsNotNone(consumer)
        success = False
        try:
            consumer.Connect()
            success = True
        except Exception as e:
            logging.error(F"Failed to send: {str(e)}")

        self.assertTrue(success)
        self.assertTrue(consumer.IsConnected)

        item = URLItem("www.google.com", 0.0143234, True)
        success = False
        try:
            consumer.GetData()
            success = True
        except Exception as e:
            logging.error(F"Failed to send: {str(e)}")
        
        self.assertTrue(success)

        del consumer


if __name__ == '__main__':
    root_logger = logging.getLogger('')
    # Setup logging to the screen
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] [%(name)-15.15s] [%(levelname)-7.7s] %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to logger
    root_logger.addHandler(ch)
    unittest.main()