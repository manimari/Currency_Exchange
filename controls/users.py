from flask import Blueprint, jsonify, request 
import os  
from werkzeug.security import check_password_hash 
from models.queries_for_sql import insert_one_user, get_user_for_login
import jwt #module gia na dimiourgisoume kai na apokriptografisoume Json Web Token (JWT)  #pip install pyjwt 
from datetime import datetime,timedelta #datetime einai na ftiaxnoume antikeimena imerominiwn kai to timedelta einai gia diafores kai prostheseis imerominion kai wrwn kai hmerwn etc
from dotenv import load_dotenv #pip install python-dotenv 

load_dotenv() 

current_working_directory=os.getcwd()+"\\" 
database_file_name=current_working_directory+f"data\\{os.getenv('DATABASE_NAME')}.db"   
  
route_users=Blueprint("route_users",__name__)  


secret_key = os.getenv("SECRET_KEY") 

token_expire_time = os.getenv("TOKEN_EXPIRE_TIME") #in minutes 


@route_users.route("/register/",methods=["POST"])
def register(): 
    new_user = request.get_json() 
    dict_to_send = {} 
    insert_one_user(database_file_name, new_user["username"], new_user["password"]) 
    dict_to_send["message"]=f'The user with username {new_user["username"]} is registered.'
    return jsonify(dict_to_send) 

@route_users.route("/login/",methods=["POST"])
def login(): 
    user_data = request.get_json() 
    #Elegxos an yparxei sto post request username kai password
    if not "username" in user_data or not "password" in user_data : 
        return jsonify({"message":"You have to enter both username and password."}) 
    data_tuple = get_user_for_login(database_file_name, ["username"])
    #Elegxos an yparxei to username sto database mas 
    if data_tuple == None : 
        return jsonify({"message": "The username doesn't exist in the database."}) 
    #Elegxos an to password einai swsto 
    if not check_password_hash(data_tuple[1], user_data["password"]) : 
        return jsonify({"message": "The password is wrong."}) 
    if token_expire_time==0:#den ligei pote to token
        token = jwt.encode({"username":user_data["username"]},secret_key) 
    else:
        token = jwt.encode({"username":user_data["username"],"exp":(datetime.now()+timedelta(minutes=token_expire_time)).timestamp()},secret_key) 
    return jsonify({"message" : "Login successful.","token":token}) 