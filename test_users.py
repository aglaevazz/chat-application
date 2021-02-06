import os
import unittest
import users


class TestUsers(unittest.TestCase):

    # Test if database is created;
    def test_set_up_database(self):
        self.assertFalse(os.path.isfile('test.db'))

    def test_2(self):
        users.set_up_database('test')
        self.assertTrue(os.path.isfile('test.db'))
        # os.remove('test.db')
        # self.assertFalse(os.path.isfile('test.db'))


if __name__ == '__main__':
    unittest.main()
