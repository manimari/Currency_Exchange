from flask import request 
import jwt #module gia na dimiourgisoume kai na apokriptografisoume Json Web Token (JWT)  #pip install pyjwt 

def check_authentication(secret_key) : 
    token = None 
    if "token_auth" in request.headers : 
        token = request.headers["token_auth"]

    # an de iparxei token( token=None)
    if not token:
        return {"message": "Prepei na steilete token.", "authentication" : False} 
    try:
        jwt_data=jwt.decode(token, secret_key, algorithms=["HS256"])
        return {"message": "Ola kala.", "authentication" : True} 
    except jwt.exceptions.ExpiredSignatureError:
        return  {"message": "Elixe to token, prepei na kaneis login.", "authentication" : False} 
    except:
        return  {"message": "Lathos token, steile to swsto....", "authentication" : False} 
