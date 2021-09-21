import sys
import os
import time
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from piyo import Client
import unittest

from helper import StubServer, StubServerStatus, get_stub_json, load_env, TestClient

class TestTeamEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient.get_instance()
        assert not self.client == None
        assert not self.client.api_endpoint == "https://api.esa.io"

    def test_teams(self):
        stub_name = "get_teams"
        response = self.client.teams()
        expected = get_stub_json(stub_name)
        self.assertTrue("teams" in response)
        self.assertEqual(response, expected)

    def test_team(self):
        stub_name = "get_teams_{0}".format(self.client.current_team)
        response = self.client.team()
        expected = get_stub_json(stub_name)
        self.assertTrue("name" in response)
        self.assertEqual(response, expected)

    def test_stats(self):
        stub_name = "get_teams_{0}_stats".format(self.client.current_team)
        response = self.client.stats()
        expected = get_stub_json(stub_name)
        self.assertTrue("members" in response)
        self.assertEqual(response, expected)

    def test_members(self):
        stub_name = "get_teams_{0}_members".format(self.client.current_team)
        response = self.client.members()
        expected = get_stub_json(stub_name)
        self.assertTrue("members" in response)
        self.assertEqual(response, expected)

if __name__ == '__main__':
    port = 8800
    test_client = TestClient(port)

    if test_client.start_server():
        unittest.main(exit=False)
        test_client.stop_server()
    else:
        print("failed to start stub server")
    # port = 8800
    # current_team = "docs"
    # endpoint = "http://localhost:{0}".format(port)
    # TestClient(current_team=current_team, api_endpoint=endpoint)

    # server_thd = StubServer(port)
    # server_thd.start()

    # timeout = 3
    # elasped = 0
    # wait_time = 0.1
    # while server_thd.status == StubServerStatus.NotBind:
    #     if elasped >= timeout:
    #         print("set up server timed out.")
    #         sys.exit(1)
    #     time.sleep(wait_time)
    #     elasped += wait_time

    # if server_thd.status == StubServerStatus.Established:
    #     unittest.main(exit=False)
    #     server_thd.shutdown()

    # elif server_thd.status == StubServerStatus.Failed:
    #     print("failed to start stub server")