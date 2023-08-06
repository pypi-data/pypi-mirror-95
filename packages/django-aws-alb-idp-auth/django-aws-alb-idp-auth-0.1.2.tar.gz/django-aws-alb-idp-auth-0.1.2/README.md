# djang-aws-alb-idp-auth
![python test](https://github.com/opencollector/django-aws-alb-idp-auth/workflows/python%20test/badge.svg)
## features

- verify jwt
- extract user claims

## setup

### middleware

Put `django_aws_alb_idp_auth.middleware.alb_idp_auth_middleware` and `django.contrib.auth.middleware.RemoteUserMiddleware` after AuthenticationMiddleware.

```
MIDDLEWARE = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_aws_alb_idp_auth.middleware.alb_idp_auth_middleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    ...
]
```

## auth backend
You may use RemoteUserBackend as Authentication Backend to create accessing user model.

```
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
    # 'django_aws_alb_idp_auth.backends.CreateUsperUserBackend',
]
```

`django_aws_alb_idp_auth.backends.CreateUsperUserBackend` is very convenient RemoteUserBackend that creates superuser.

## accessing user claims

You can get user claims from `request.META["django_aws_alb_idp_auth.middleware.user_claims"]`.
