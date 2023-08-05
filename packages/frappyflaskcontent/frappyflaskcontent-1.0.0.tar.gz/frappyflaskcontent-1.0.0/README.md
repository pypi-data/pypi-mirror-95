# Flask Content

Flask Endpoints for Content Management and Retrieval

1. [Example Usage](#example-usage)
2. [Options](#options)

## Example Usage

```python
from frappyflaskcontent import register_endpoints
from frappyflaskauth import check_login_state
from flask import Flask

app = Flask(__name__)
# create store instances for content
content_store = ...
# register the endpoints
register_endpoints(app, content_store, options={
    "manage_permission": "manage",
    "login_check_function": check_login_state,
})
```

## Options

Options for the `register_endpoints` function are:

- `api_prefix` - default `/api/content` - is the prefix under which the endpoints will be registered. This should
 match the prefix used in the front-end.
- `manage_permission` - default `None` - the permission required to manage content (create, update, delete), if `None`
 is provided the user just needs to be logged in.
- `get_permission` - default `None` - the permission required to fetch content via the API. This can be different from
 the `manage_permission`.
- `login_check_function` - default `None` - provide a function that performs authentication and uses Flask's `abort` in
 case the login / permission check fails. The function has 1 parameter for the required permission. You can use
 `check_login_state` from the `frappyflaskauth` package.
