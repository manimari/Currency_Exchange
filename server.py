from flask import Flask, jsonify, request, render_template 
import os  
from models.queries_for_sql import create_db 
from functions.check_file_existence import check_file_existence 
from controls.rates import route_rates 
from controls.users import route_users 
from dotenv import load_dotenv #pip install python-dotenv

load_dotenv() 

current_working_directory=os.getcwd()+"\\" 
database_file_name=current_working_directory+f"data\\{os.getenv('DATABASE_NAME')}.db"   

  
if check_file_existence(database_file_name) == False : 
    create_db(database_file_name) 

app=Flask(__name__) 
app.secret_key=os.getenv("SECRET_KEY") #apokriptografei to session key automata
app.register_blueprint(route_rates,url_prefix="/rates")  
app.register_blueprint(route_users,url_prefix="/users") 



if __name__=="__main__":
    port=5000 
    app.run(port=port,debug=True)  

