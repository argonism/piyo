import sys
import os
import time
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from piyo import Client
import unittest

from helper import StubServer, StubServerStatus



class TestGetEndpoints(unittest.TestCase):
    def _load_env(self):
        with open(".env") as f:
            for line in f:
                field, value = line.strip().split("=")
                os.environ[field] = value

    def setUp(self):
        self._load_env()
        self.current_team = "docs"
        self.endpoint = "http://localhost:{0}".format(port)
        self.client = Client(current_team=self.current_team, api_endpoint=self.endpoint)
    
    def test_teams(self):
        response = self.client.teams()
        self.assertTrue("teams" in response)

    # def test_team(self):
    #     response = self.client.team()
    #     self.assertTrue("name" in response)

    # def test_stats(self):
    #     response = self.client.stats()
    #     self.assertTrue("members" in response)

    # def test_members(self):
    #     response = self.client.members()
    #     self.assertTrue("members" in response)

    # def test_posts(self):
    #     response = self.client.posts()
    #     self.assertTrue("posts" in response)

    # def test_post(self):
    #     post_number = 1
    #     response = self.client.post(post_number)
    #     self.assertTrue("posts" in response)

    # def test_comments_with_post_number(self):
    #     response = self.client.posts()
    #     self.assertTrue("posts" in response)

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