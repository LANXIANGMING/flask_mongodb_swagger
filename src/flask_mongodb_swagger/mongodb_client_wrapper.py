from flask import Flask, g
import pymongo


class MongoDBClientWrapper:
    def __init__(self, app,uri=None, *args, **kwargs):
        if app is not None:
            self.init_wrapper(app, uri, *args, **kwargs)

    def init_wrapper(self, app, uri=None, *args, **kwargs):
        self.USER_DATABASE_USER = app.config.get("USER_DATABASE_USER", None)
        self.USER_DATABASE_PASSWORD = app.config.get("USER_DATABASE_PASSWORD", None)
        self.USER_DATABASE_URL = app.config.get("USER_DATABASE_URL", None)
        self.USER_DATABASE_PORT = str(app.config.get("USER_DATABASE_PORT", '27017'))

        _mongodb_client = pymongo.MongoClient('mongodb://' + self.USER_DATABASE_URL + ':' + self.USER_DATABASE_PORT + '/')
        #_mongodb_client.admin.authenticate( self.USER_DATABASE_USER , self.USER_DATABASE_PASSWORD )
        
        with app.app_context():
            if not hasattr(g, 'mongodb_client'):
                g.mongodb_client = _mongodb_client
        
        self.mongodb_client = _mongodb_client["bd"]
    
    def get_mongodb_client(self):
        return self.mongodb_client

    mongodb_client = None
    