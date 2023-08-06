# Tamarin Utils


## Sentry
> settings.py
```python
from tamarin import sentry
...
SENTRY_KEY = '<your sentry key>'
SENTRY_ORGANIZATION = '<your sentry organization name>'
SENTRY_PROJECT = '<your sentry project name>'
SENTRY_ALLOWED_ALL = 'if true all status captured' # default False
SENTRY_ALLOWED_STATUS = 'list of status that should capture' # default []
sentry.init()
```
or
```python
from tamarin import sentry
...
SENTRY_URL = '<your sentry url>'
SENTRY_ALLOWED_ALL = 'if true all status captured' # default False
SENTRY_ALLOWED_STATUS = ['<allowed status or condition>'] # default []
sentry.init()
``` 
 

## Elastic search
> settings.py
```python
ELASTIC_PROTOCOL = '<http or https>' # default 'http'
ELASTIC_HOST = '<host that elastic run>' # default 'localhost'
ELASTIC_PORT = '<listen port>' # default 9200
ELASTIC_USE_SSL = '' # default False
TIME_ZONE = '<elastic timezone>' # default 'UTC'
ELASTIC_ALLOWED_STATUS = ['<allowed status or condition>'] # default []
ELASTIC_USER = '<elastic username>' # default ''
ELASTIC_PASSWORD = '<elastic secret>' # default ''
```

## Firebase
> settings.py
```python
FIREBASE_APP_OPTIONS = '<app dict options>' # default {}
FIREBASE_APP_NAME = 'your app name' # default 'FIRESTORE_DEFAULT'
```


## Log
> for use log, you must config elastic search and sentry before



## JWT Authentication
in your root urls.py file (or any other url config), 
include routes for Tamarin’s 
TokenObtainPairView and TokenRefreshView views:
```python
from django.urls import path
from tamarin.rest.authorization import (
    TamarinTokenObtainPairView,
    TamarinRefreshView
)
urlpatterns = [
    ...,
    path('apiv1/accounts/token/', TamarinTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('apiv1/accounts/refresh/', TamarinRefreshView.as_view(), name='token_refresh'),
    ...
]
```
### Settings
Some of Tamarin’s authentication behavior can be 
customized through settings variables in settings.py
```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('tamarin.rest.authorization.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
```

## Database ReplicaRouter

With `database.router.ReplicaRouter` all read queries will go to a replica
database;  all inserts, updates, and deletes will do to the ``default``
database.
First, define ``REPLICA_DATABASES`` in your settings.  It should be a list of
database aliases that can be found in ``DATABASES``:
```python
DATABASES = {
    'default': {...},
    'replica-1': {...},
    'replica-2': {...},
}
REPLICA_DATABASES = ['replica-1', 'replica-2']
```
Then put ``database.router.ReplicaRouter`` into DATABASE_ROUTERS:
```python
DATABASE_ROUTERS = ('tamarin.database.router.ReplicaRouter',)
```    
The replica databases will be chosen in round-robin fashion.
If you want to get a connection to a replica in your app, use `database.router.ReplicaRouter`
```python
from django.db import connections
from tamarin.database import router
connection = connections[router.get_replica()]
```

### Database PinningReplicaRouter
In some applications, the lag between the primary database receiving a
write and its replication to the replicas is enough to cause inconsistency
for the end user. For example, imagine a scenario with 1 second of replication lag.
If a user makes a forum post (to the primary) and then is redirected 
to a fully-rendered view of it (from a replica) 500ms later, the view will fail. 
If this is a problem in your application, consider using `multidb.PinningReplicaRouter`. 
This router works in combination with `multidb.middleware.PinningRouterMiddleware` 
to assure that, after writing to the `default` database, future reads from the same 
user agent are directed to the `default` database for a configurable length of time.

`PinningRouterMiddleware` identifies database writes primarily by request type, 
assuming that requests with HTTP methods that are not `GET`, `TRACE`, `HEAD`, or `OPTIONS` 
are writes. You can indicate that any view writes to the database by using the 
`tamarin.database.router.db_write` decorator. This will cause the same result 
as if the request were, e.g., a `POST`.

To use `PinningReplicaRouter`, put it into `DATABASE_ROUTERS` in your settings:
```python
DATABASE_ROUTERS = ('database.router.PinningReplicaRouter',)
```
Then, install the middleware. It must be listed before any other middleware 
which performs database writes:
```python
MIDDLEWARE_CLASSES = (
    'multidb.middleware.PinningRouterMiddleware',
    ...more middleware here...
)

```
`PinningRouterMiddleware` attaches a cookie to any user agent who has just written. 
The cookie should be set to expire at a time longer than your replication lag. 
By default, its value is a conservative 15 seconds, but it can be adjusted like so:
```python
TAMARIN_PINNING_SECONDS = 5
```
If you need to change the name of the cookie, use the `TAMARIN_PINNING_COOKIE` setting:
```python
TAMARIN_PINNING_COOKIE = 'tamarin_pin_writes'
```
