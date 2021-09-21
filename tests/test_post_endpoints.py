import sys
import os
import time
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from piyo import Client
import unittest

from helper import StubServer, StubServerStatus, get_stub_json, load_env, TestClient

class TestPostEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient.get_instance()
        assert not self.client == None
        assert not self.client.api_endpoint == "https://api.esa.io"
    
    def test_posts(self):
        stub_name = "get_teams_{0}_posts".format(self.client.current_team)
        response = self.client.posts()
        expected = get_stub_json(stub_name)
        self.assertTrue("posts" in response)
        self.assertEqual(response, expected)

    def test_post(self):
        stub_name = "get_teams_{0}_posts_1".format(self.client.current_team)
        response = self.client.post(1)
        expected = get_stub_json(stub_name)
        self.assertTrue("name" in response)
        self.assertEqual(response, expected)

    def test_posts_comments(self):
        response = self.client.comments(post_number=2)
        stub_name = "get_teams_{0}_posts_2_comments".format(self.client.current_team)
        expected = get_stub_json(stub_name)
        self.assertTrue("comments" in response)
        self.assertEqual(response, expected)

    def test_comments(self):
        response = self.client.comments()
        stub_name = "get_teams_{0}_comments".format(self.client.current_team)
        expected = get_stub_json(stub_name)
        self.assertTrue("comments" in response)
        self.assertEqual(response, expected)

    def test_comment(self):
        stub_name = "get_teams_{0}_comments_13".format(self.client.current_team)
        response = self.client.comment(13)
        expected = get_stub_json(stub_name)
        self.assertTrue("id" in response)
        self.assertEqual(response, expected)

if __name__ == '__main__':
    port = 8800
    test_client = TestClient(port)

    if test_client.start_server():
        unittest.main(exit=False)
        test_client.stop_server()
    else:
        print("failed to start stub server")