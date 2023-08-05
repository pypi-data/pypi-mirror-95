# MongoDB User Stores for Python

Frappy MongoDB Store Implementation for Users and UserTokens for Python

1. [Usage](#usage)
2. [Methods](#methods)

## Usage

```python
from frappymongouser import UserStore, UserTokenStore

MONGO_URL = "mongodb://localhost:27017"  # use your MongoDB url and add potential credentials

# this is how the stores are instantiated
user_store = UserStore(mongo_url=MONGO_URL, mongo_db="databaseName", collection_name="users")
token_store = UserTokenStore(mongo_url=MONGO_URL, mongo_db="databaseName", collection_name="userTokens")

# example usage: retrieve all documents
user_list = user_store.get_all() 
for user in user_list:
    # user is of type User and has attributes
    print(user.email, user.permissions)
```

## Methods

Base methods for both stores provided by [`pbu`](https://pypi.org/project/pbu/)

**`UserStore`**

- `create_local_user(username, password, permissions)` - will create a new local user. The password will be MD5 encoded.
 The same encoding mechanism used for the login check.
- `login_with_password(username, password)` - will attempt to perform a login with the provided credentials.
- `change_password(user_id, new_password)` - update the users password using MD5 to encode the password.
- `update_permissions(user_id, permissions)` - completely overwrites the permissions of a user with the provided.
- `update_profile(user_id, new_profile)` - completely overwrites the profile of a user with the provided value
- `get_by_username(username)` - fetches a user by it's `username` attribute.
-  `initial_local_user_check(initial_username, initial_password, initial_permissions)` - this function can be called
 when using local users only. It is already incorporated in the
  [`frappyflaskauth`](https://github.com/ilfrich/frappy-flask-authentication) package when using local logins. It will
  check if there are any existing users. If there are no users in the system yet, this will create an initial user with
  the provided credentials and permissions that can be used as initial administrator account. If no permissions are
  provided, the user will receive the `admin` permission, which is also the default to manage users using the package
  `frappyflaskauth` (and/or [`@frappy/react-authentication`](https://github.com/ilfrich/frappy-react-authentication)
- `create_api_key(user_id)` - the function will update a user's `apiKey` key in the database and return the new key. The
 key is something like this: `e31d7880-e968-4195-96ac-4be8798f1915` and a `str`.
- `get_users_with_api_key()` - retrieves a list of users that have an API key set (`apiKey` exists) - only used in
context of admin functions
- `revoke_api_key(user_id)` - removes an API key from a user leaving the user without an active API key.

**`UserTokenStore`**

- `create(user_id, token, lifetime)` - simple, just creates a new token. The `lifetime` is provided as
 `datetime.timedelta` (and defaults to 30 days)
- `get_by_token(token)` - searches for a specific token and returns a matching entry or `None`
- `clean_up_expired()` - checking the expired flag on each token and deleting entries that exceed their lifetime
- `update_token(token_id)` - just updates the `last_update` date of the token - _deprecated, because rather useless_
