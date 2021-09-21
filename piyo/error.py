class PiyoException(Exception):
    def __init__(self, msg=""):
        self.msg = ""

class PiyoHTTPException(PiyoException):

    def __init__(self, http_code, reason, error_code):
        super().___init__()
        self.http_code = http_code
        self.msg = reason
        self.error_code = error_code

    def __str__(self):
        return "PiyoHTTPException(http status: {0}, reason: {1}, error_code: {2}".format(
            self.http_code, self.reason, self.error_code
        )

class PiyoEmptyTeamException(PiyoException):
    def __init__(self, func_name):
        self.msg = "team name required"
        self.func_name = func_name
    
    def __str__(self):
        return "PiyoTeamRequiredException: {0} at {1}".format(self.msg, self.func_name)