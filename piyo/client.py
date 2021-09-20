import requests, os
from enum import Enum, auto
from .error import PiyoException

class RequestMethod(Enum):
    GET = auto()
    POST = auto()
    PATHC = auto()
    DELETE = auto()

class Client(object):
    def __init__(self, access_token="", current_team="", api_endpoint="https://api.esa.io"):
        self._access_token = access_token
        self.current_team = current_team
        self.api_endpoint = api_endpoint
    
    def _credential_header(self, access_token):
        return {"Authorization": "Bearer {0}".format(access_token)}

    def _request(self, method, path, params={}, headers={}, with_auth=True):
        if with_auth: headers = dict(self._credential_header(self.access_token), **headers)
        url = "{0}{1}".format(self.api_endpoint, path)
        response = None
        try:
            if method == RequestMethod.GET:
                response = requests.get(url, params=params, headers=headers)
            if method == RequestMethod.POST:
                response = requests.post(url, params=params, headers=headers)

            response.raise_for_status()
            results = response.json()
        except requests.exceptions.HTTPError as err:
            reason = err.reason
            status_code = err.status

            raise PiyoException(
                status_code,
                reason,
                -1,
            )
        return results
    
    @property
    def access_token(self):
        return self._access_token or os.environ["ESA_ACCESS_TOKEN"]

    def teams(self, params={}, headers={}):
        path = "/v1/teams"
        return self._request(RequestMethod.GET, path, params, headers)

    def team(self, params={}, headers={}):
        path = "/v1/teams/{0}".format(self.current_team)
        return self._request(RequestMethod.GET, path, params, headers)
    
    def stats(self, params={}, headers={}):
        path = "/v1/teams/{0}/stats".format(self.current_team)
        return self._request(RequestMethod.GET, path, params, headers)
    
    def members(self, params={}, headers={}):
        path = "/v1/teams/{0}/members".format(self.current_team)
        return self._request(RequestMethod.GET, path, params, headers)
    
    def posts(self, params={}, headers={}):
        path = "/v1/teams/{0}/posts".format(self.current_team)
        return self._request(RequestMethod.GET, path, params, headers)

    def post(self, post_number, params={}, headers={}):
        path = "/v1/teams/{0}/posts/{1}".format(self.current_team, post_number)
        return self._request(RequestMethod.GET, path, params, headers)

    def comments(self, post_number=None, params={}, headers={}):
        if post_number:
            path = "/v1/teams/{0}/posts/{1}/comments".format(self.current_team, post_number)
        else:
            path = "/v1/teams/{0}/comments".format(self.current_team)
        return self._request(RequestMethod.GET, path, params, headers)
    
    def comment(self, comment_id, params={}, headers={}):
        path = "/v1/teams/{0}/comments/{1}".format(self.current_team, comment_id)
        return self._request(RequestMethod.GET, path, params, headers)



if __name__ == "__main__":
    client = Client(os.environ["ESA_TEST_TEAM"])
    res = client.teams()
    print(res)