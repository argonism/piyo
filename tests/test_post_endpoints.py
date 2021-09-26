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

    def test_create_post(self):
        stub_name = "post_teams_{0}_posts".format(self.client.current_team)
        data = {
            "post":{
                "name": "hi!",
                "body_md": "# Getting Started\n",
                "tags": [
                        "api",
                        "dev"
                    ],
                "category": "dev/2015/05/10",
                "wip": False,
                "message": "Add Getting Started section"
            }
        }
        response = self.client.create_post(data)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_create_comment(self):
        post_id = 2
        data = {"comment":{"body_md":"LGTM!"}}
        stub_name = "post_teams_{0}_posts_{1}_comments".format(self.client.current_team, post_id)
        response = self.client.create_comment(post_id, data)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_add_post_star(self):
        post_id = 2312
        stub_name = "post_teams_{0}_posts_{1}_star".format(self.client.current_team, post_id)
        response = self.client.add_post_star(post_id)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_add_comment_star(self):
        comment_id = 123
        stub_name = "post_teams_{0}_comments_{1}_star".format(self.client.current_team, comment_id)
        response = self.client.add_comment_star(comment_id)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_add_watch(self):
        post_number = 2312
        stub_name = "post_teams_{0}_posts_{1}_watch".format(self.client.current_team, post_number)
        response = self.client.add_watch(post_number)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_batch_move(self):
        stub_name = "post_teams_{0}_categories_batch_move".format(self.client.current_team)
        data = {
            "from": "/foo/bar/",
            "to": "/baz/"
        }
        response = self.client.batch_move(data)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)


    def test_regenerate_invitation(self):
        stub_name = "post_teams_{0}_invitation_regenerator".format(self.client.current_team)
        response = self.client.regenerate_invitation()
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_send_invitation(self):
        stub_name = "post_teams_{0}_invitations".format(self.client.current_team)
        data = {
            "member": {
                "emails": ["foo@example.com", "bar@example.com"]
            }
        }
        response = self.client.send_invitation(data)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_create_emoji(self):
        stub_name = "post_teams_{0}_emojis".format(self.client.current_team)
        data = {
            "emoji": {
                "code": "team_emoji",
                "image": "..." # BASE64 String
            }
        }
        response = self.client.create_emoji(data)
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