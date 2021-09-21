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
        post_number = 1
        stub_name = "get_teams_{0}_posts_{1}".format(self.client.current_team, post_number)
        response = self.client.post(post_number)
        expected = get_stub_json(stub_name)
        self.assertTrue("name" in response)
        self.assertEqual(response, expected)

    def test_posts_comments(self):
        post_number = 2
        response = self.client.comments(post_number=post_number)
        stub_name = "get_teams_{0}_posts_{1}_comments".format(self.client.current_team, post_number)
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
        comment_id = 13
        stub_name = "get_teams_{0}_comments_{1}".format(self.client.current_team, comment_id)
        response = self.client.comment(comment_id)
        expected = get_stub_json(stub_name)
        self.assertTrue("id" in response)
        self.assertEqual(response, expected)

    def test_post_stargazers(self):
        post_number = 2312
        stub_name = "get_teams_{0}_posts_{1}_stargazers".format(self.client.current_team, post_number)
        response = self.client.post_stargazers(post_number)
        expected = get_stub_json(stub_name)
        self.assertTrue("stargazers" in response)
        self.assertEqual(response, expected)

    def test_comment_stargazers(self):
        comment_id = 123
        stub_name = "get_teams_{0}_comments_{1}_stargazers".format(self.client.current_team, comment_id)
        response = self.client.comment_stargazers(comment_id)
        expected = get_stub_json(stub_name)
        self.assertTrue("stargazers" in response)
        self.assertEqual(response, expected)

    def test_watchers(self):
        post_number = 2312
        stub_name = "get_teams_{0}_posts_{1}_watchers".format(self.client.current_team, post_number)
        response = self.client.watchers(post_number)
        expected = get_stub_json(stub_name)
        self.assertTrue("watchers" in response)
        self.assertEqual(response, expected)

    def test_invitation(self):
        stub_name = "get_teams_{0}_invitation".format(self.client.current_team)
        response = self.client.invitation()
        expected = get_stub_json(stub_name)
        self.assertTrue("url" in response)
        self.assertEqual(response, expected)

    def test_invitations(self):
        stub_name = "get_teams_{0}_invitations".format(self.client.current_team)
        response = self.client.invitations()
        expected = get_stub_json(stub_name)
        self.assertTrue("invitations" in response)
        self.assertEqual(response, expected)

    def test_invitations(self):
        stub_name = "get_teams_{0}_emojis".format(self.client.current_team)
        response = self.client.emojis()
        expected = get_stub_json(stub_name)
        self.assertTrue("emojis" in response)
        self.assertEqual(response, expected)

    def test_user(self):
        stub_name = "get_user"
        response = self.client.user()
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