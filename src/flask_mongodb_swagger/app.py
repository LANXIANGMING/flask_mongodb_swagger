
import hashlib
import os
import ast 
import sys 
from dotenv import load_dotenv, find_dotenv

from flask import Flask, g,  request_started
from flask_cors import CORS
from flask_restful import  reqparse
from flask_restful_swagger_3 import Api, swagger, get_swagger_blueprint
from flask_json import FlaskJSON, json_response

from logging.config import dictConfig


from service.user import User 
from security import login_required
from security import set_user

from mongodb_client_wrapper import MongoDBClientWrapper
from response_utility import *
from api.api_resource_register import EntryPointResourceRegister


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',}, 
        'brief': {'format': '%(message)s'},
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
            },
        'console': { 
            'class' : 'logging.StreamHandler',
            'formatter': 'default',
            #'formatter': 'brief',
            'level': 'NOTSET',
            #'filters': ['allow_foo'],
            'stream': 'ext://sys.stdout'
            },
        'file': {
            'class' : 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': 'base.log',
            'maxBytes': 10485760,
            'backupCount': 20
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console','file']
    }
})


load_dotenv(find_dotenv())

app = Flask(__name__)

CORS(app)
#CORS(app, expose_headers='Authorization')
#CORS(app, supports_credentials=True)
FlaskJSON(app)


# Define parser and request args
parser = reqparse.RequestParser()


def env(key, default=None, required=True):
    """
    Retrieves environment variables and returns Python natives. The (optional)
    default will be returned if the environment variable does not exist.
    """
    try:
        value = os.environ[key]
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
    except KeyError:
        if default or not required:
            return default
        raise RuntimeError("Missing required environment variable '%s'" % key)

app.config['SECRET_KEY'] = env('SECRET_KEY')
 
app.config['USER_DATABASE_USER'] = env('USER_DATABASE_USER')
app.config['USER_DATABASE_PASSWORD'] = env('USER_DATABASE_PASSWORD')
app.config['USER_DATABASE_URL'] = env('USER_DATABASE_URL')
app.config['USER_DATABASE_PORT'] = env('USER_DATABASE_PORT')

mongodb_client_wrapper = MongoDBClientWrapper(app)
MongoDBClientWrapper.mongodb_client = mongodb_client_wrapper.get_mongodb_client()

@app.teardown_appcontext
def close_db(error): 
    if hasattr(g, 'mongodb_client'):
        g.mongodb_client.close()

def init_db():

    #init user 
    _user = User(mongodb_client_wrapper.mongodb_client)
    _user.init_user() 
    #init system parameters 

request_started.connect(set_user, app)

def hash_password(username, password):
    if sys.version[0] == 2:
        s = '{}:{}'.format(username, password)
    else:
        s = '{}:{}'.format(username, password).encode('utf-8')
    return hashlib.sha256(s).hexdigest()

init_db()


authorizations = {
    'APIKeyQueryParam': {
        'type': 'apiKey',
        'in': 'query',
        'name': 'api_key'
    },
}

#TODO: get server url and port instead of hard code
servers = [{"url": "http://localhost:5001"}]
api = Api(app, version='5', servers=servers, title="Backend service API", authorizations= authorizations, add_api_spec_resource=False)

def auth(api_key, endpoint, method):
    return True
    # # Space for your fancy authentication. Return True if access is granted, otherwise False
    # # api_key is extracted from the url parameters (?api_key=foo)
    # # endpoint is the full swagger url (e.g. /some/{value}/endpoint)
    # # method is the HTTP method
    # if api_key == None:
    #     return False

    # #TODO: configure the API key in database instead of hard code;test pipeline
    # if 'QasdJIEXesiBEZXZlbG9wZXI=' == api_key:
    #     return True
    # else: 
    #     return False

swagger.auth = auth

restful_api = EntryPointResourceRegister(api)

SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'swagger.json'  

swagger_ui_prefix = '/swagger-ui'
app.config.setdefault('SWAGGER_BLUEPRINT_URL_PREFIX', swagger_ui_prefix)
with app.app_context():
    swagger_blueprint = get_swagger_blueprint(
        api.open_api_object,
        swagger_prefix_url=SWAGGER_URL,
        swagger_url=API_URL,
        title='Backend Service Resource', description = 'Backend service resource', version='1.0.1')
app.register_blueprint(swagger_blueprint, url_prefix = swagger_ui_prefix)


#deserialize data to http response  
@api.representation('application/json')
def output_json(data, code, headers=None):
    return json_response(data_=data, headers_=headers, status_=code)
