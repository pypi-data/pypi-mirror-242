
#### Requirements
- Python >= 3.6
- Django >= 2.1
- Django-Ninja >= 0.16.1
- Django-Ninja-Extra >= 0.11.0

These are the officially supported python and package versions. Other
versions will probably work. You 're free to modify the tox config and
see what is possible.

Installation
============
Ninja JWT can be installed with pip:

    pip install django-ninja-jwt

Also, you need to register `NinjaJWTDefaultController` controller to you Django-Ninja api.
The `NinjaJWTDefaultController` comes with three routes `obtain_token`, `refresh_token` and `verify_token`

```python
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

```

The `NinjaJWTDefaultController` comes with three routes `obtain_token`, `refresh_token` and `verify_token`. 
It is a combination of two subclass `TokenVerificationController` and `TokenObtainPairController`.
If you wish to customize these routes, you can inherit from these controllers and change its implementation

```python
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

@api_controller('token', tags=['Auth'])
class MyCustomController(TokenObtainPairController):
    """obtain_token and refresh_token only"
...
api.register_controllers(MyCustomController)
```

If you wish to use localizations/translations, simply add `ninja_jwt` to
`INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...
    'ninja_jwt',
    ...
]
```

Usage
=====

To verify that Ninja JWT is working, you can use curl to issue a couple
of test requests:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
  http://localhost:8000/api/token/pair

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```

You can use the returned access token to prove authentication for a
protected view:

``` {.sourceCode .bash}
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/some-protected-view/
```

When this short-lived access token expires, you can use the longer-lived
refresh token to obtain another access token:

``` {.sourceCode .bash}
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/api/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNTY3LCJqdGkiOiJjNzE4ZTVkNjgzZWQ0NTQyYTU0NWJkM2VmMGI0ZGQ0ZSJ9.ekxRxgb9OKmHkfy-zs1Ro_xs1eMLXiR17dIDBVxeT-w"}
```

Cryptographic Dependencies (Optional)
-------------------------------------

If you are planning on encoding or decoding tokens using certain digital
signature algorithms (i.e. RSA and ECDSA; visit PyJWT for other algorithms), you will need to install the
cryptography_ library. This can be installed explicitly, or as a required
extra in the `django-ninja-jwt` requirement:

    pip install django-ninja-jwt[crypto]


The `django-ninja-jwt[crypto]` format is recommended in requirements
files in projects using `Ninja JWT`, as a separate `cryptography` requirement
line may later be mistaken for an unused requirement and removed.
[cryptography](https://cryptography.io)
