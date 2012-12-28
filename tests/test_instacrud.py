import unittest
from django.utils import simplejson
from gaetestbed.datastore import DataStoreTestCase
import CRUD
import weblib

class InstaCRUDTest(DataStoreTestCase, unittest.TestCase):

    def setUp(self):
        self.req = weblib.RequestBuilder().build()

    def test_new_grid(self):
        rawData = dict(
            name="people",
            meta=[
                ["str", "firstName"],
                ["str", "lastName"],
                ["int", "age"],
                ["email", "email"],
            ])

        self.req.content = simplejson.dumps(rawData)
        g = CRUD.create_grid(self.req, None)
        self.assertEqual(rawData['name'], g.keys()[0])
        self.assertEqual(rawData['meta'], g.values()[0])



if __name__=="__main__":
    unittest.main()
