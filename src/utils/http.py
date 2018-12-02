import jwt
import json

from typing import List
from functools import wraps
from flask import Blueprint, request, make_response
from flask_restful import Api
from simplexml import dumps
from werkzeug.wrappers import Response, HTTP_STATUS_CODES

from config import get_secret_key, FLASK_APP
from config.flask_config import AuthenticationFailed, ForbiddenResourceException, ResourceException


def token_required(roles:List[str]=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                raise AuthenticationFailed('Token is missing')
                
            return func(token=token, *args, **kwargs)
        return wrapper
    return decorator