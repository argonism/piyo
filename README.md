# piyo
esa API v1 client library, written in Python

### installation

install this library using pip
``` shell
pip install piyo
```

### Usage

``` python
from piyo import Client

client = Client(access_token="<access_token>", current_team='<team_name>')
# Client will look up environment variables  access token

client.user
#=> GET /v1/user

client.team
#=> GET /v1/teams

client.team("<team_name>")
#=> GET /v1/teams/team_name

client.stats
#=> GET /v1/teams/bar/stats

...

```