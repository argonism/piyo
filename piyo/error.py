class PiyoException(Exception):

    def __init__(self, http_code, reason, error_code):
        self.http_code = http_code
        self.reason = reason
        self.error_code = error_code

    def __str__(self):
        return "PiyoException(http status: {0}, reason: {1}, error_code: {2}".format(
            self.http_code, self.reason, self.error_code
        )