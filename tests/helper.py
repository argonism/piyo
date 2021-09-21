import os, sys, json
from http.server import SimpleHTTPRequestHandler
import socketserver
from threading import Thread
from enum import Enum, auto

def load_env(self):
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
            print("failed to start stub server")
            self.status = StubServerStatus.Failed

    def shutdown(self):
        self.httpd.shutdown()

if __name__ == "__main__":
    server = StubServer(8800)
    server.start()
