from flask import Flask, g, request
from flask_restful import Resource, reqparse
from flask_restful_swagger_3 import Api, swagger, Schema
from flask_json import FlaskJSON, json_response
import uuid

from service.user import User

from mongodb_client_wrapper import MongoDBClientWrapper
from response_utility import response_header

class LoginInfo(Schema):
    type = 'object' 
    properties =  {  
                    'user_id': {
                        'type': 'string',
                    },
                    'user_email': {
                        'type': 'string',
                    },
                    'password': {
                        'type': 'string',
                    } 
                }

@swagger.tags('Users')
class Login(Resource): 
    @swagger.reorder_with(schema=None, response_code=200, description='Succesful login', summary='Login', example=None) 
    @swagger.response(response_code=400, description="Invalid credentials",summary='Login',  no_content=True) 
    @swagger.response(response_code=404, description="User does not exist",summary='Login',  no_content=True) 
    #@swagger.parameters([{'in': 'query', 'name': 'body', 'description': 'Request body', 'schema': schema, 'required': 'true'}]) 
    #RequestParser object if you want to pass its arguments to spec.
    @swagger.expected(schema= LoginInfo, required =  True)
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            user_email = data.get('user_email')
        password = data.get('password')
        
        if ((not user_id) and (not user_email)):
            return response_header({},False,'This field either user_id or user_email is required.'), 400
        if not password:
            return response_header({},False,'This field password is required.'), 400

        _user = User(MongoDBClientWrapper.mongodb_client)

        try:
            if user_id == None:
                user = _user.get_user(user_email =  user_email)
            else:
                user = _user.get_user(user_id =  user_id)

            if user == None:
                return response_header({},False,'user does not exist'), 404
            print(user) 

            #to do set token expire time
            if user['token'] == None or user['token'] == '':
                #generat a token 
                user['token'] = uuid.uuid4() 
                _user.update_user_token(user['user_id'], user['token'])
            
            login_result = {'token': user['token']}
            if 'role' in user:
                login_result['role'] = user['role']
            else:
                login_result['role'] = 'ge'

            return response_header(login_result,True,'')
        except KeyError:
            return response_header({},False,'user does not exist'), 404
