import sqlite3 
import requests 
import json 
from dotenv import load_dotenv #pip install python-dotenv
import os
load_dotenv()

api_key = os.getenv("API_KEY") 

def insert_one_currency(database_file_name, id, base, target, value) : 
    con = sqlite3.connect(database_file_name) 
    try : 
        query = f"""Insert Into Currency (id, base, target, value) values('{id}', '{base}', '{target}', '{value}')"""
        cursor = con.cursor() 
        cursor.execute(query)   
        con.commit() 
    except : 
        print("An exception occurred") 
    con.close()  

def get_exchange(database_file_name, base): 
    con = sqlite3.connect(database_file_name) 
    try : 
        query = f"Select * from Currency where base='{base}'" 
        #query = f"Select * from Currency where base='{base}' order by target" 
        #query = f"Select * from Currency where base='{base}' order by value" 
        cursor = con.cursor() 
        cursor.execute(query) 
        all_exchanges_base = cursor.fetchall() 
    except : 
        print("An exception occurred") 
    con.close() 
    return all_exchanges_base 

def get_specific_exchange(database_file_name, base,target): 
    con = sqlite3.connect(database_file_name) 
    try : 
        query = f"Select * from Currency where base='{base}' and target='{target}'" 
        cursor = con.cursor() 
        cursor.execute(query) 
        specific_exchange_base = cursor.fetchall() 
    except : 
        print("An exception occurred") 
    con.close() 
    return specific_exchange_base  

def get_latest_id_currency(database_file_name): 
    con = sqlite3.connect(database_file_name) 
    try : 
        query = f"Select max(id) from Currency" 
        cursor = con.cursor() 
        cursor.execute(query) 
        latest_id = cursor.fetchone() 
    except : 
        print("An exception occurred") 
    con.close() 
    return latest_id[0] 

def convert(base,currency):
    url=f"https://api.currencyapi.com/v3/latest?apikey={api_key}&currencies={currency}&base_currency={base}"
    site_html=json.loads(requests.get(url).text) #converts strings to dictionaries
    return site_html["data"][currency]["value"] 

def new_specific_exchange(database_file_name, base,target): 
    if len(get_specific_exchange(base,target)) == 0 : 
        new_specific_exchange_base = insert_one_currency(get_latest_id_currency()+1, base, target, convert(base,target)) 
    else : 
        con = sqlite3.connect(database_file_name) 
        try : 
            query = f"Update Currency set value='{convert(base,target)}' where base='{base}' and target='{target}'" 
            cursor = con.cursor() 
            cursor.execute(query) 
            new_specific_exchange_base = cursor.fetchall() 
        except : 
            print("An exception occurred") 
        con.close() 
    new_specific_exchange_base = get_specific_exchange(base,target)
    return new_specific_exchange_base  

def get_exchange_all(database_file_name): 
    con = sqlite3.connect(database_file_name) 
    try : 
        query = f"Select * from Currency" 
        cursor = con.cursor() 
        cursor.execute(query) 
        all_exchanges = cursor.fetchall() 
    except : 
        print("An exception occurred") 
    con.close() 
    return all_exchanges 

def get_exchange_all_dict(): 
    exchange_list_of_dict = [] 
    all_exchanges = get_exchange_all() 
    for exchange in all_exchanges: 
        exchange_dict = {} 
        exchange_dict["id"] = exchange[0] 
        exchange_dict["base"] = exchange[1] 
        exchange_dict["target"] = exchange[2] 
        exchange_dict["value"] = exchange[3] 
        exchange_list_of_dict.append(exchange_dict) 
    return exchange_list_of_dict 