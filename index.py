from db import Database
from loguru import logger
import config

def reg():
    new_user_email = input("Enter Your Email: ")
    new_user_name = input("Enter Your username: ")
    new_user_password = input("Enter Your Password: ")
    db_instance = Database(config)
    db_instance.connect()
    #db.select_rows("""Select * from users""")
    rows = db_instance.run_query("""SELECT * from users""")
    new_user_id = len(rows) + 1
    db_instance.insert(new_user_id,new_user_name,new_user_password,new_user_email)

def login():
    print("login")

print(
"""
    Welcome user !
    Please authorize.
"""
)
new_user = input("Do you already have an account ? (y/n)")
entryVal_flag = False
while(entryVal_flag != True):
    if(new_user == "y"):
        entryVal_flag = True
        login()
    elif(new_user == "n"):
        entryVal_flag = True
        reg()
    else:
        print("Invalid entry. Please try again.")
        new_user = input("Do you already have an account ? (y/n)")
