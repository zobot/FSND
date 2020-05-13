import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'zoe-coffeeshop.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


"""UDACITY REVIEWER:  most of this code is copied with small modification from the lessons preceding the project."""


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if auth is None:
        raise AuthError(error={
            'code': "missing_authorization_header",
            'description': "No authorization header",
        }, status_code=401)

    header_parts = auth.split(" ")
    if len(header_parts) != 2:
        raise AuthError(error={
            'code': "invalid_authorization_header",
            'description': "Authorization header is not length 2",
        }, status_code=401)

    if header_parts[0].lower() != "bearer":
        raise AuthError(error={
            'code': "invalid_authorization_header",
            'description': "Authorization header does not contain bearer",
        }, status_code=401)

    token = header_parts[1]
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError(error={
            'code': "invalid_payload",
            'description': "JWT payload does not include permissions.",
        }, status_code=400)

    if permission not in payload['permissions']:
        raise AuthError(error={
            'code': "permission_not_allowed",
            'description': "Permission is not allowed for this action.",
        }, status_code=401)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': "invalid_authorization_header",
            'description': "Authorization does not contain kid",
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token has expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_authorization_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    else:
        raise AuthError({
            'code': 'invalid_authorization_header',
            'description': 'Unable to find the rsa key.'
        }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator