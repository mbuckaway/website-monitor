import unittest
from webmonlib.Config import Config
from webmonlib.URLItem import URLItem
from webmonlib.Database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.config = Config(".env.test")

    def tearDown(self):
        pass

    def test_connection(self):
        database = Database(self.config)
        database.Connect()
        self.assertTrue(database.Connected)
        del database

    @unittest.skip("Skipping destructive test")
    def test_createdb(self):
        '''
        Destructive test. This creates the DB tables and drops them. Should really use a test database to prevent dropping
        a set of tables in use.
        '''
        database = Database(self.config)
        success = False
        try:
            database.Connect()
            success = True
        except:
            success = False
        self.assertTrue(success)
        self.assertTrue(database.Connected)
        success = False
        try:
            database.CreateDatabase()
            success = True
        except Exception as e:
            print(f"DB Error: {str(e)}")
            success = False
        self.assertTrue(success, "DB Create failed")

        success = False
        try:
            database.DropDatabase()
            success = True
        except Exception as e:
            print(f"DB Error: {str(e)}")
            success = False
        self.assertTrue(success, "DB Drop failed")

        del database

    def test_insert(self):
        database = Database(self.config)
        success = False
        try:
            database.Connect()
            success = True
        except:
            success = False
        self.assertTrue(success)
        self.assertTrue(database.Connected)

        success = False
        try:
            database.CreateDatabase()
            success = True
        except Exception as e:
            print(f"DB Error: {str(e)}")
            success = False
        self.assertTrue(success, "DB Create failed")

        item = URLItem("http://testsite2.com", 1.0, True)
        database.InsertData(item)

        del database



if __name__ == '__main__':
    unittest.main()