import unittest

from api.database import base


class TestDB(unittest.TestCase):
    def setUp(self):
        self.db = base.DBConnection()
        self.conn = self.db.create_session()


    def test_dbconnect(self):
        self.db.create_session()


    def test_table(self):
        from api.database.models.test import Tests
        n_t = Tests(1, "test")
        self.conn.add(n_t)
        print('?')
        self.conn.commit()