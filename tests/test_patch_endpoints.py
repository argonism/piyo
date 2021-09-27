import sys
import os
import time
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from piyo import Client
import unittest

from helper import StubServer, StubServerStatus, get_test_data, load_env, TestClient

class TestPostEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient.get_instance()
        assert not self.client == None
        assert not self.client.api_endpoint == "https://api.esa.io"

    def test_update_post(self):
        post_number = 5
        stub_name = "patch_teams_{0}_posts_{1}".format(self.client.current_team, post_number)
        data = {
            "post":{
                "name":"hi!",
                "body_md":"# Getting Started\n",
                "tags":[
                    "api",
                    "dev"
                ],
                "category":"dev/2015/05/10",
                "wip":False,
                "message":"Add Getting Started section",
                "original_revision": {
                    "body_md": "# Getting ...",
                    "number":1,
                    "user": "fukayatsu"
                }
            }
        }
        response = self.client.update_post(post_number, data)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_update_comment(self):
        comment_id = 22767
        data = {"comment":{"body_md":"LGTM!!!"}}
        stub_name = "patch_teams_{0}_comments_{1}".format(self.client.current_team, comment_id)
        response = self.client.update_comment(comment_id, data)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

if __name__ == '__main__':
    port = 8800
    test_client = TestClient(port)

    if test_client.start_server():
        unittest.main(exit=False)
        test_client.stop_server()
    else:
        print("failed to start stub server")