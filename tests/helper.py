import os, sys, json, time
from http.server import SimpleHTTPRequestHandler
import socketserver
from threading import Thread
from enum import Enum, auto
from piyo import Client

def load_env():
    with open(".env") as f:
        for line in f:
            field, value = line.strip().split("=")
            os.environ[field] = value


def get_script_dir():
    script_path = __file__ if "__file__" in globals() \
                            else os.path.abspath(sys.argv[0])
    return os.path.dirname(script_path)


def get_stub_json(stub_name):
    path = os.path.join(get_script_dir(), "stubs", stub_name + ".json")
    with open(path) as f:
        return json.load(f)

class TestClient():
    def __init__(self, port, team="docs", api_endpoint="http://localhost"):
        load_env()
        self.port = port
        self.current_team = team
        self.api_endpoint = "{0}:{1}".format(api_endpoint, port)
        TestClient._instance = Client(current_team=self.current_team, api_endpoint=self.api_endpoint)

    @classmethod
    def get_instance(cls, *args, **kwargs):
        return cls._instance if hasattr(cls, "_instance") else None
    
    # @classmethod
    # def set_instance(cls, *args, **kwargs):
    #     cls._instance = Client(*args, **kwargs)
    
    def start_server(self, timeout=3):
        self.server_thd = StubServer(self.port)
        self.server_thd.start()
        timeout = 3
        elasped = 0
        wait_time = 0.1
        while self.server_thd.status == StubServerStatus.NotBind:
            if elasped >= timeout:
                print("set up server timed out.")
                return False
            time.sleep(wait_time)
            elasped += wait_time
        return self.server_thd.status == StubServerStatus.Established

    def stop_server(self):
        self.server_thd.shutdown()



class StubHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        tests_dir = get_script_dir()

        stubs_path = os.path.join(tests_dir, "stubs")
        super().__init__(*args, directory=stubs_path, **kwargs)
    
    def path_to_filename(self):
        dirs = self.path.split("/")[2:]
        stub_suffix = "_".join(dirs)
        stub_name = "{0}_{1}.json".format(self.command.lower(), stub_suffix)
        return stub_name

    def do_GET(self):
        self.path = self.path_to_filename()
        # print("self.path:", self.path)
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()

    def do_POST(self):
        pass
    
    def do_PATCH(self):
        pass
    
    def do_DELETE(self):
        pass


class StubServerStatus(Enum):
    NotBind = auto()
    Established = auto()
    Failed = auto()

class StubServer(Thread):
    def __init__(self, port):
        super(StubServer, self).__init__()
        self.port = port
        self.httpd = None
        self.status = StubServerStatus.NotBind
    
    def run(self):
        Handler = StubHTTPRequestHandler
        try:
            with socketserver.TCPServer(("", self.port), Handler) as httpd:
                self.httpd = httpd
                self.status = StubServerStatus.Established
                httpd.serve_forever()
        except OSError as err:
            print("failed to start stub server:", err)
            self.status = StubServerStatus.Failed

    def shutdown(self):
        self.httpd.shutdown()

if __name__ == "__main__":
    server = StubServer(8800)
    server.start()
