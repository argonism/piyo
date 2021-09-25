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

client.create_post({post: {name: "hi!"}})
#=> POST /v1/teams/<team_name>/posts

client.comments()
#=> GET /v1/teams/<team_name>/comments

client.comments(1)
#=> GET /v1/teams/<team_name>/posts/1/comments

client.create_comment(1, {"comment":{"body_md":"LGTM!"}})
#=> POST /v1/teams/<team_name>/posts/1/comments

client.comment(1)
#=> GET /v1/teams/<team_name>/comments/1

client.add_post_star(1)
#=> POST /v1/teams/<team_name>/posts/1/star

client.stargazers(1)
#=> GET /v1/teams/<team_name>/posts/1/stargazers

client.add_comment_star(1)
#=> POST /v1/teams/<team_name>/comment/1/star

client.watchers(1)
#=> POST /v1/teams/<team_name>/posts/1/watchers

client.add_watch(1)
#=> POST /v1/teams/<team_name>/posts/1/watch

client.batch_move({})
#=> POST /v1/teams/<team_name>/posts/1/watch

client.regenerate_invitation()
#=> POST /v1/teams/<team_name>/invitation_regenerator

client.send_invitation({"member": {"emails": ["foo@example.com"]})
#=> POST /v1/teams/<team_name>/invitations

client.invitations()
#=> GET /v1/teams/<team_name>/invitations

client.emojis()
#=> GET /v1/teams/<team_name>/emojis

client.create_emoji({"emoji": {"code": "funny", "image": base64}})
#=> POST /v1/teams/<team_name>/emojis

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