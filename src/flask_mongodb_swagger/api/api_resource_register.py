from api.user_resource import * 
 
#json_data = request.get_json(force=True)
#define get, post, put, delete methods in Class Resource
 
class EntryPointResourceRegister:
    def __init__(self, api):
        if api is not None:
            self.init_restful_api(api)
            
    def init_restful_api(self,api):
        api_version = 'v0'  
        api.add_resource(Login, '/api/' + api_version + '/login') 
 
         