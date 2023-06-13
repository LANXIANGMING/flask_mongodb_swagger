def response_header(data,state,msg): 
    return {
        'success': state,
        'msg':msg,
		'data': data
    }
 
def serialize_str(value):
    return value