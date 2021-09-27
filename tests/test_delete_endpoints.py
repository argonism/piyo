import sys
import os
import time
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from piyo import Client
import unittest

from helper import StubServer, StubServerStatus, get_test_data, load_env, TestClient

class TestDeleteEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient.get_instance()
        assert not self.client == None
        assert not self.client.api_endpoint == "https://api.esa.io"

    def test_delete_member(self):
        screen_name = "alice"
        stub_name = "delete_teams_{0}_members_{1}".format(self.client.current_team, screen_name)
        response = self.client.delete_member(screen_name)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_delete_post(self):
        post_number = 5
        stub_name = "delete_teams_{0}_posts_{1}".format(self.client.current_team, post_number)
        response = self.client.delete_post(post_number)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_delete_comment(self):
        comment_id = 22767
        stub_name = "delete_teams_{0}_comments_{1}".format(self.client.current_team, comment_id)
        response = self.client.delete_comment(comment_id)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_delete_post_star(self):
        post_number = 2312
        stub_name = "delete_teams_{0}_posts_{1}_star".format(self.client.current_team, post_number)
        response = self.client.delete_post_star(post_number)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_delete_comment_star(self):
        comment_id = 123
        stub_name = "delete_teams_{0}_comments_{1}_star".format(self.client.current_team, comment_id)
        response = self.client.delete_comment_star(comment_id)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_delete_watch(self):
        post_number = 2312
        stub_name = "delete_teams_{0}_posts_{1}_watch".format(self.client.current_team, post_number)
        response = self.client.delete_watch(post_number)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_delete_invitation(self):
        inv_code = "mee93383edf699b525e01842d34078e28"
        stub_name = "delete_teams_{0}_invitations_{1}".format(self.client.current_team, inv_code)
        response = self.client.delete_invitation(inv_code)
        requestline = get_test_data(stub_name)
        self.assertEqual(response["requestline"], requestline)

    def test_delete_emoji(self):
        emj_code = "team_emoji"
        stub_name = "delete_teams_{0}_emojis_{1}".format(self.client.current_team, emj_code)
        response = self.client.delete_emoji(emj_code)
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