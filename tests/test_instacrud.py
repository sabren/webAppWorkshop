import unittest
from gaetestbed.datastore import DataStoreTestCase
from app.tangentcode import instacrud

class InstaCRUDTest(DataStoreTestCase, unittest.TestCase):

    def test_new_grid(self):
        g = instacrud.new_grid(dict(name="people"),None)
        self.assertEqual("people", g['name'])

if __name__=="__main__":
    unittest.main()
