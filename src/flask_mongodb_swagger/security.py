import uuid
import re
from functools import wraps
from flask import  g, request, abort
from service.user import User

from mongodb_client_wrapper import MongoDBClientWrapper

def is_valid_uuid(val):
    try:
        uuid.UUID(val, version=4)
        return True
    except ValueError:
        return False

def set_user(sender, **extra):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        g.user = {'id': None}
        return
    match = re.match(r'^token-(\S+)', auth_header)
    if not match:
        abort(401, 'invalid authorization format. Follow `token-<uuid token>`')
        #abort(401, response_header({'invalid authorization format. Follow `token-<uuid token>`'},False,''))
        return
    token = match.group(1)

    if not is_valid_uuid(token):
        abort(401, 'invalid authorization format. Follow `token-<uuid token>`')
        #abort(401, response_header({'invalid authorization format. Follow `token-<uuid token>`'},False,''))
        return 
    
    _user = User(MongoDBClientWrapper.mongodb_client)
    user = _user.get_user(token =  uuid.UUID(token))
    if user == None:
        abort(401, 'invalid authorization key')
    try:
        user['str_id'] = str(user['_id'])
        g.user = user
    except (KeyError, TypeError):
        abort(401, 'invalid authorization key')
    return

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'no authorization provided'}, 401
        return f(*args, **kwargs)
    return wrapped

