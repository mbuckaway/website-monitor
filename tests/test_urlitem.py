import unittest
from webmonlib.URLItem import URLItem

class TestURLItem(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_urlitem(self):
        '''
        Simple test to make sure we didn't make a typo
        '''
        urlitem = URLItem("http://www.google.com", 0.12323, True)
        self.assertEqual(urlitem.Url, "http://www.google.com")
        self.assertEqual(urlitem.ReactionTime, 0.12323)
        self.assertTrue(urlitem.Success)


if __name__ == '__main__':
    unittest.main()