# Flask Data Sets

Flask Endpoints for Data Set Management and Retrieval

1. [Example Usage](#example-usage)
2. [Options](#options)

## Example Usage

```python
from frappyflaskdataset import register_endpoints
from frappyflaskauth import check_login_state
from flask import Flask

app = Flask(__name__)
# create store instances for data sets
data_store = ...
# register the endpoints
register_endpoints(app, data_store, options={
    "manage_permission": "manage",
    "login_check_function": check_login_state,
})
```

## Options

Options for the `register_endpoints` function are:

- `api_prefix` - default `/api/data-sets` - is the prefix under which the endpoints will be registered. This should
 match the prefix used in the front-end.
- `manage_permission` - default `None` - the permission required to manage data sets (upload, update, delete), if `None`
 is provided the user just needs to be logged in.
- `get_permission` - default `None` - the permission required to fetch data sets via the API. This can be different from
 the `manage_permission`.
- `data_folder` - default `_data` - the local directory where to store data files (images primarily). This is relative
 to your applications root directory (from where you execute the start command)
- `login_check_function` - default `None` - provide a function that performs authentication and uses Flask's `abort` in
 case the login / permission check fails. The function has 1 parameter for the required permission. You can use
 `check_login_state` from the `frappyflaskauth` package.
- `allow_public_binary_access` - default `False` - a boolean flag that, when set to `True` will allow even
 unauthenticated users to download the files from **all** `BINARY` data sets and `IMAGE` data sets. This allows to
 directly include `<img src="/api/data-sets/<id>/image">` without running into authentication issues (requires using
 `ImageView`)
