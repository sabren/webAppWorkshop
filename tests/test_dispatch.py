import unittest
import app.tangentcode.tangentcode as tc
import weblib

class DispatchTest(unittest.TestCase):
    """
    This is currently testing tangentcode, but it's
    REALLY testing a new dispatch mechanism for weblib.
    """
    def setUp(self):
        self.req = weblib.RequestBuilder().build()
        self.res = weblib.Response()

    def tearDown(self):
        pass

    def test_pathArgs(self):
        self.req.path="/api/g/"
        tc.main(self.req, self.res)
        self.assertEqual({}, self.req.pathArgs)


if __name__ == "__main__":
    unittest.main()
