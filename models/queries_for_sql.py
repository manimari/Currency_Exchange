import sqlite3
from werkzeug.security import generate_password_hash 

def create_db(database_file_name) : 
    con = sqlite3.connect(database_file_name)
    try : 
        query = """Create Table User
            (username varchar(100) not NULL primary key, 
            password varchar(100) 
            );"""  
        cursor = con.cursor() 
        cursor.execute(query) 
        query = """Create Table Currency
            (id int not NULL primary key, 
            base char(3), 
            target char(3), 
            value real  
            );"""  
        cursor = con.cursor() 
        cursor.execute(query)   
    except : 
        print("An exception occurred") 
    con.close() 

def insert_one_user(database_file_name, username, password) : 
    con = sqlite3.connect(database_file_name) 
    try : 
        hashed_password = generate_password_hash(password,method='sha256') 
        query = f"""Insert Into User (username, password) values('{username}', '{hashed_password}')"""
        cursor = con.cursor() 
        cursor.execute(query)   
        con.commit() 
    except : 
        print("An exception occurred") 
    con.close()  

def get_user_for_login(database_file_name, username):  
    con = sqlite3.connect(database_file_name) 
    try : 
        query = f"Select * from User where username='{username}'" 
        cursor = con.cursor() 
        cursor.execute(query) 
        all_users_user = cursor.fetchone() #epistrefei mono to tuple, oxi pinaka me tuples 
    except : 
        print("An exception occurred") 
    con.close() 
    return all_users_user 