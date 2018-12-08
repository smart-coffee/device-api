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
from core import WEB_API


CODE = 201


def token_required(roles:List[str]=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                raise AuthenticationFailed('Token is missing')
            
            # Verifies user token
            WEB_API.is_user(token)

            return func(token=token, *args, **kwargs)
        return wrapper
    return decorator


def get_post_response(body, content_type, api, obj_id):
    if content_type == 'application/json':
        body = json.dumps(body.__dict__)
    response = Response(body)
    response.status = HTTP_STATUS_CODES[CODE]
    response.status_code = CODE
    response.headers['location'] = '{api}/{new_id}'.format(api=api, new_id=obj_id)
    response.autocorrect_location_header = False
    response.content_type = content_type

    return response
