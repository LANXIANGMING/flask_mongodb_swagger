import pymongo 
from datetime import datetime

class User:
    _COLLECTION_NAME = 'users'
    def __init__(self, user_db):
        self.mongodb = user_db

    #init and save users
    def init_user(self):
        
        collist = self.mongodb.list_collection_names()

        if self._COLLECTION_NAME in collist:
            return

        user_col =  self.mongodb[self._COLLECTION_NAME]

        users = [{ "user_id": "user1", "user_email": "user1@gmail.com","password":"","token":"", "role":"se"}]

        _now = datetime.now()
        for user in users:
            user['created_date'] = _now.strftime("%Y-%m-%d %H:%M:%S")
           
        x = user_col.insert_many(users)
    
    #create a new user
    def create_user(self, user_id,user_email, password,role):
        
        collist = self.mongodb.list_collection_names()

        if self._COLLECTION_NAME not in collist:
            return

        user_col =  self.mongodb[self._COLLECTION_NAME]
        user = { "user_id": user_id, "user_email": user_email,"password":password,"token":"", "role":role}

        _now = datetime.now()
        user['created_date'] = _now.strftime("%Y-%m-%d %H:%M:%S")

        x = user_col.insert_one(user)
        return str(x.inserted_id)

    #update user token
    def update_user_token(self, user_id, token):
        
        collist = self.mongodb.list_collection_names()

        if self._COLLECTION_NAME not in collist:
            return

        user_col =  self.mongodb[self._COLLECTION_NAME]

        filter = {'user_id':user_id}
        newvalues = { "$set": {'token':token}}

        user_col.update_one(filter,newvalues)
        x = self.get_user(user_id=user_id)
        print(x)
    
    #update user role
    def update_user_role(self, user_id, role):
        
        collist = self.mongodb.list_collection_names()

        if self._COLLECTION_NAME not in collist:
            return

        user_col =  self.mongodb[self._COLLECTION_NAME]

        filter = {'user_id':user_id}
        newvalues = { "$set": {'role':role}}

        user_col.update_one(filter,newvalues)
        x = self.get_user(user_id=user_id)

    
    _user_search_keys = ['user_id','user_email','token']
    def get_user(self, **kwds):
        collist = self.mongodb.list_collection_names()

        if self._COLLECTION_NAME in collist:
            for key, value in kwds.items():
                if key in self._user_search_keys:
                    return self.mongodb[self._COLLECTION_NAME].find_one({ key: value} )

    
    def get_users(self, **kwds):
        collist = self.mongodb.list_collection_names()

        query = {}
        if self._COLLECTION_NAME in collist:
            for key, value in kwds.items():
                query[key] = value

            return list(self.mongodb[self._COLLECTION_NAME].find(query))
