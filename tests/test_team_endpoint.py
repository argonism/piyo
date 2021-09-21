import sys
import os
import time
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from piyo import Client
import unittest

from helper import StubServer, StubServerStatus, get_stub_json, load_env

class TestGetEndpoints(unittest.TestCase):
    def setUp(self):
        load_env()
        self.current_team = "docs"
        self.endpoint = "http://localhost:{0}".format(port)
        self.client = Client(current_team=self.current_team, api_endpoint=self.endpoint)
    
    def test_teams(self):
        stub_name = "get_teams"
        response = self.client.teams()
        expected = get_stub_json(stub_name)
        self.assertTrue("teams" in response)
        self.assertEqual(response, expected)

    def test_team(self):
        stub_name = "get_teams_{0}".format(self.current_team)
        response = self.client.team()
        expected = get_stub_json(stub_name)
        self.assertTrue("name" in response)
        self.assertEqual(response, expected)

    def test_stats(self):
        response = self.client.stats()
        stub_name = "get_teams_{0}_stats".format(self.current_team)
        expected = get_stub_json(stub_name)
        self.assertTrue("members" in response)
        self.assertEqual(response, expected)

    def test_members(self):
        stub_name = "get_teams_{0}_members".format(self.current_team)
        response = self.client.members()
        expected = get_stub_json(stub_name)
        self.assertTrue("members" in response)
        self.assertEqual(response, expected)

if __name__ == '__main__':
    port = 8800
    server_thd = StubServer(port)
    server_thd.start()

    timeout = 3
    elasped = 0
    wait_time = 0.1
    while server_thd.status == StubServerStatus.NotBind:
        if elasped >= timeout:
            print("set up server timed out.")
            sys.exit(1)
        time.sleep(wait_time)
        elasped += wait_time

    if server_thd.status == StubServerStatus.Established:
        unittest.main(exit=False)
        server_thd.shutdown()

    elif server_thd.status == StubServerStatus.Failed:
        print("failed to start stub server")