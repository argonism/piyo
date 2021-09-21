
import sys
import os
import time
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest

from test_team_endpoints import TestTeamEndpoints
from test_post_endpoints import TestPostEndpoints
from helper import StubServer, StubServerStatus, get_stub_json, load_env, TestClient


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
    # TestClient.set_instance(current_team=current_team, api_endpoint=endpoint)


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