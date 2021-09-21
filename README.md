# 🐣 piyo
esa API v1 client library, written in Python

**this project is work in progress.**

**currently,  available endpoint is partial.**

## Installation

install this library using pip
``` shell
pip install piyo
```

## Usage

``` python
from piyo import Client

client = Client(access_token='<access_token>', current_team='<team_name>')
# Client will look up environment variables  access token

client.user()
#=> GET /v1/user

client.teams()
#=> GET /v1/teams

client.team()
#=> GET /v1/teams/<team_name>

client.stats()
#=> GET /v1/teams/<team_name>/stats

client.members()
#=> GET /v1/teams/<team_name>/members

client.posts()
#=> GET /v1/teams/<team_name>/posts

client.post(1)
#=> GET /v1/teams/<team_name>/posts/1

client.comments()
#=> GET /v1/teams/<team_name>/comments

client.comments(1)
#=> GET /v1/teams/<team_name>/posts/1/comments

client.comment(1)
#=> GET /v1/teams/<team_name>/comments/1

client.stargazers(1)
#=> GET /v1/teams/<team_name>/posts/1/stargazers

...

```

## Development

issues and pull requests are always welcome!

run integration test

``` shell
python3 tests/integration_test.py
```

run unit test

``` shell
python3 tests/<test_file>.py -v
```