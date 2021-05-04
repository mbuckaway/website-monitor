import unittest
from webmonlib.Config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_config(self):
        config = Config(".env.sample")
        self.assertEqual(config.DATABASE_HOST, "pg.aivencloud.com")
        self.assertEqual(config.DATABASE_PORT, 26654)
        self.assertEqual(config.DATABASE_DB, "webmonitor")
        self.assertEqual(config.DATABASE_USER, "webmonitor")
        self.assertEqual(config.KAFKA_HOST, "kafka.aivencloud.com:26656")
        self.assertEqual(config.KAFKA_TOPIC, "webmon-stats")
        self.assertEqual(config.KAFKA_USER, "avnadmin")
        self.assertEqual(config.KAFKA_CAFILE, "cert/ca.pem")
        self.assertEqual(config.KAFKA_CERTFILE, "cert/service.cert")
        self.assertEqual(config.KAFKA_KEYFILE, "cert/service.key")


if __name__ == '__main__':
    unittest.main()