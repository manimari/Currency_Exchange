from functions.check_authentication import check_authentication  
from flask import Blueprint, jsonify, render_template 
import os  
from models.queries_rates import insert_one_currency, get_latest_id_currency, convert, get_exchange, get_specific_exchange, new_specific_exchange, get_exchange_all, get_exchange_all_dict
from dotenv import load_dotenv #pip install python-dotenv 

load_dotenv() 

current_working_directory=os.getcwd()+"\\" 
database_file_name=current_working_directory+f"data\\{os.getenv('DATABASE_NAME')}.db"   
  
route_rates=Blueprint("route_rates",__name__)  

secret_key = os.getenv("SECRET_KEY") 

@route_rates.route("/seed/",methods=["POST"]) 
def all_currencies() : 
    #athentication
    auth_dict=check_authentication(secret_key)
    if auth_dict["authentication"]==False:
        return jsonify(auth_dict),401  
    dict_to_send = {} 
    for base in ["CHF", "EUR", "GBP", "USD"] : 
        for target in ["CHF", "EUR", "GBP", "USD"] :
            insert_one_currency(get_latest_id_currency()+1, base, target, convert(base,target)) 
    dict_to_send["message"]=f'The exchange rates for all currencies with EUR, USD, CHF and GBP as base currency have been added.'
    return jsonify(dict_to_send)

@route_rates.route("/<base>/",methods=["GET"]) 
def all_exchange_base(base) : 
    #athentication
    auth_dict=check_authentication(secret_key)
    if auth_dict["authentication"]==False:
        return jsonify(auth_dict),401  
    dict_to_send = {} 
    dict_to_send["exchanges"] = get_exchange(base)
    dict_to_send["message"]=f'These are all the exchange rates from the database for {base}.'
    return jsonify(dict_to_send) 

@route_rates.route("/<base>/<target>/",methods=["GET"]) 
def exchange_base_target(base,target) : 
    #athentication
    auth_dict=check_authentication(secret_key)
    if auth_dict["authentication"]==False:
        return jsonify(auth_dict),401  
    dict_to_send = {} 
    dict_to_send["exchanges"] = get_specific_exchange(base,target)
    dict_to_send["message"]=f'This is the exchange rate from the database for the base {base} and the target {target}.'
    return jsonify(dict_to_send) 

@route_rates.route("/<base>/<target>/",methods=["POST"]) 
def exchange_base_target_new(base,target) : 
    #athentication
    auth_dict=check_authentication(secret_key)
    if auth_dict["authentication"]==False:
        return jsonify(auth_dict),401  
    dict_to_send = {} 
    dict_to_send["exchanges"] = new_specific_exchange(base,target)
    dict_to_send["message"]=f'This is the new/updated exchange rate for the base {base} and the target {target}.'
    return jsonify(dict_to_send) 

@route_rates.route("/",methods=["GET"]) 
def exchange_all() : 
    #athentication
    auth_dict=check_authentication(secret_key)
    if auth_dict["authentication"]==False:
        return jsonify(auth_dict),401  
    dict_to_send = {} 
    dict_to_send["exchanges"] = get_exchange_all()
    dict_to_send["message"]=f'These are all the exchange rates of the database.'
    return jsonify(dict_to_send) 

@route_rates.route("/all/") 
def get_all(): 
    all_rates=get_exchange_all_dict()
    print(all_rates)
    return render_template("currency.html", my_currency = all_rates)