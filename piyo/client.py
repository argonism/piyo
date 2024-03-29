import warnings
import requests
import os
import mimetypes
from pathlib import Path
from enum import Enum
from .error import PiyoEmptyTeamException, PiyoNotImplementedException, PiyoHTTPException

class RequestMethod(Enum):
    GET = 1
    POST = 2
    PATCH = 3
    DELETE = 4

class Client(object):
    def __init__(self, access_token="", current_team="", api_endpoint="https://api.esa.io"):
        self._access_token = access_token
        self.current_team = current_team
        self.api_endpoint = api_endpoint
    
    def _credential_header(self, access_token):
        return {"Authorization": "Bearer {0}".format(access_token)}

    def _request(self, method, url, params={}, headers={}, data={}):
        response = None
        try:
            if method == RequestMethod.GET:
                response = requests.get(url, params=params, headers=headers)
            elif method == RequestMethod.POST:
                response = requests.post(url, params=params, headers=headers, json=data)
            elif method == RequestMethod.PATCH:
                response = requests.patch(url, params=params, headers=headers, json=data)
            elif method == RequestMethod.DELETE:
                response = requests.delete(url, params=params, headers=headers, json=data)
            else:
                raise PiyoNotImplementedException(method)

            response.raise_for_status()

            if len(response.text) <= 0:
                results = None
            else:
                results = response.json()

        except requests.exceptions.HTTPError as err:
            reason = err.response.reason
            status_code = err.response.status_code

            raise PiyoHTTPException(
                status_code,
                reason,
                -100,
            )

        return results

    def _request_to_esa(self, method, path, params={}, headers={}, data={}, with_auth=True):
        if with_auth: headers = dict(self._credential_header(self.access_token), **headers)
        url = "{0}{1}".format(self.api_endpoint, path)
        return self._request(method, url, params=params, headers=headers, data=data)
    
    def team_required(func):
        def wrapper(self, *args, **kwargs):
            if not self.current_team:
                assert PiyoEmptyTeamException(func.__name__)
            return func(self, *args, **kwargs)
        return wrapper
    
    @property
    def access_token(self):
        return self._access_token or os.environ["ESA_ACCESS_TOKEN"]

    def teams(self, params={}, headers={}):
        path = "/v1/teams"
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def team(self, params={}, headers={}):
        path = "/v1/teams/{0}".format(self.current_team)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def stats(self, params={}, headers={}):
        path = "/v1/teams/{0}/stats".format(self.current_team)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def members(self, params={}, headers={}):
        path = "/v1/teams/{0}/members".format(self.current_team)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def delete_member(self, screen_name, params={}, headers={}):
        path = "/v1/teams/{0}/members/{1}".format(self.current_team, screen_name)
        return self._request_to_esa(RequestMethod.DELETE, path, params, headers)

    @team_required
    def posts(self, keywords=[], search_options={}, params={}, headers={}):
        path = "/v1/teams/{0}/posts".format(self.current_team)
        if len(search_options) > 0:
            options = [f"{str(k)}: {str(v)}" for k, v in search_options.items()]
            q_param = " ".join([str(k) for k in keywords] + options)
            params["q"] = q_param
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def post(self, post_number, params={}, headers={}):
        path = "/v1/teams/{0}/posts/{1}".format(self.current_team, post_number)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)
    
    @team_required
    def create_post(self, data, params={}, headers={}):
        path = "/v1/teams/{0}/posts".format(self.current_team)
        return self._request_to_esa(RequestMethod.POST, path, params, headers, data=data)
    
    @team_required
    def update_post(self, post_number, data, params={}, headers={}):
        path = "/v1/teams/{0}/posts/{1}".format(self.current_team, post_number)
        return self._request_to_esa(RequestMethod.PATCH, path, params, headers, data=data)
    
    @team_required
    def delete_post(self, post_number, params={}, headers={}):
        path = "/v1/teams/{0}/posts/{1}".format(self.current_team, post_number)
        return self._request_to_esa(RequestMethod.DELETE, path, params, headers)

    @team_required
    def comments(self, post_number=None, params={}, headers={}):
        if post_number:
            path = "/v1/teams/{0}/posts/{1}/comments".format(self.current_team, post_number)
        else:
            path = "/v1/teams/{0}/comments".format(self.current_team)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def comment(self, comment_id, params={}, headers={}):
        path = "/v1/teams/{0}/comments/{1}".format(self.current_team, comment_id)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def create_comment(self, post_number, data, params={}, headers={}):
        path = "/v1/teams/{0}/posts/{1}/comments".format(self.current_team, post_number)
        return self._request_to_esa(RequestMethod.POST, path, params, headers, data=data)

    @team_required
    def update_comment(self, comment_id, data, params={}, headers={}):
        path = "/v1/teams/{0}/comments/{1}".format(self.current_team, comment_id)
        return self._request_to_esa(RequestMethod.PATCH, path, params, headers, data=data)

    @team_required
    def delete_comment(self, comment_id, params={}, headers={}):
        path = "/v1/teams/{0}/comments/{1}".format(self.current_team, comment_id)
        return self._request_to_esa(RequestMethod.DELETE, path, params, headers)

    @team_required
    def post_stargazers(self, post_number, params={}, headers={}):
        path = "/v1/teams/{0}/posts/{1}/stargazers".format(self.current_team, post_number)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def add_post_star(self, post_number, data={}, params={}, headers={}):
        path = "/v1/teams/{0}/posts/{1}/star".format(self.current_team, post_number)
        return self._request_to_esa(RequestMethod.POST, path, params, headers, data=data)

    @team_required
    def delete_post_star(self, post_number, params={}, headers={}):
        path = "/v1/teams/{0}/posts/{1}/star".format(self.current_team, post_number)
        return self._request_to_esa(RequestMethod.DELETE, path, params, headers)    

    @team_required
    def comment_stargazers(self, comment_id, params={}, headers={}):
        path = "/v1/teams/{0}/comments/{1}/stargazers".format(self.current_team, comment_id)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def add_comment_star(self, comment_id, data={}, params={}, headers={}):
        path = "/v1/teams/{0}/comments/{1}/star".format(self.current_team, comment_id)
        return self._request_to_esa(RequestMethod.POST, path, params, headers, data=data)

    @team_required
    def delete_comment_star(self, comment_id, params={}, headers={}):
        path = "/v1/teams/{0}/comments/{1}/star".format(self.current_team, comment_id)
        return self._request_to_esa(RequestMethod.DELETE, path, params, headers)

    @team_required
    def watchers(self, post_number, params={}, headers={}):
        path = "/v1/teams/{0}/posts/{1}/watchers".format(self.current_team, post_number)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def add_watch(self, post_number, params={}, headers={}):
        path = "/v1/teams/{0}/posts/{1}/watch".format(self.current_team, post_number)
        return self._request_to_esa(RequestMethod.POST, path, params, headers)

    @team_required
    def delete_watch(self, post_number, params={}, headers={}):
        path = "/v1/teams/{0}/posts/{1}/watch".format(self.current_team, post_number)
        return self._request_to_esa(RequestMethod.DELETE, path, params, headers)

    @team_required
    def batch_move(self, data, params={}, headers={}):
        path = "/v1/teams/{0}/categories/batch_move".format(self.current_team)
        return self._request_to_esa(RequestMethod.POST, path, params, headers)

    @team_required
    def invitation(self, params={}, headers={}):
        path = "/v1/teams/{0}/invitation".format(self.current_team)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def regenerate_invitation(self, params={}, headers={}):
        path = "/v1/teams/{0}/invitation_regenerator".format(self.current_team)
        return self._request_to_esa(RequestMethod.POST, path, params, headers)

    @team_required
    def send_invitation(self, data, params={}, headers={}):
        path = "/v1/teams/{0}/invitations".format(self.current_team)
        return self._request_to_esa(RequestMethod.POST, path, params, headers, data=data)

    @team_required
    def delete_invitation(self, code, params={}, headers={}):
        path = "/v1/teams/{0}/invitations/{1}".format(self.current_team, code)
        return self._request_to_esa(RequestMethod.DELETE, path, params, headers)

    @team_required
    def invitations(self, params={}, headers={}):
        path = "/v1/teams/{0}/invitations".format(self.current_team)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def emojis(self, params={}, headers={}):
        path = "/v1/teams/{0}/emojis".format(self.current_team)
        return self._request_to_esa(RequestMethod.GET, path, params, headers)

    @team_required
    def create_emoji(self, data, params={}, headers={}):
        path = "/v1/teams/{0}/emojis".format(self.current_team)
        return self._request_to_esa(RequestMethod.POST, path, params, headers)

    @team_required
    def delete_emoji(self, code, params={}, headers={}):
        path = "/v1/teams/{0}/emojis/{1}".format(self.current_team, code)
        return self._request_to_esa(RequestMethod.DELETE, path, params, headers)

    @team_required
    def upload_file(self, file_path, mine_type=None, params={}, headers={}):
        file_path = Path(file_path)
        mine_type = mine_type or mimetypes.guess_type(file_path)[0]
        if mine_type is None:
            warnings.warn("mine_type is None. use application/octet-stream")
            mine_type = "application/octet-stream"
        params = {
            "type": mine_type,
            "size": file_path.stat().st_size,
            "name": file_path.name,
        }
        path = f"/v1/teams/{self.current_team}/attachments/policies"
        response = self._request_to_esa(RequestMethod.POST, path, params, headers)

        s3_endpoint = response["attachment"]["endpoint"]
        attachment_url = response["attachment"]["url"]
        form_data = response["form"]
        _file = {'file': open(file_path, 'rb')}

        response = requests.post(s3_endpoint, data=form_data, files=_file)

        response.raise_for_status()

        return attachment_url

    def user(self, params={}, headers={}):
        path = "/v1/user"
        return self._request_to_esa(RequestMethod.GET, path, params, headers)


if __name__ == "__main__":
    client = Client(os.environ["ESA_TEST_TEAM"])
    res = client.stats()
    print(res)
