from db import Database
from loguru import logger
from getpass import getpass
import config
import re

def validateEmail(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    # for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if(re.search(regex,email)):
        return True
    else:
        logger.error("Invalid Email")
        return False

def validatePass(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if mat:
        return True
    else:
        logger.error("Invalid password")
        return False

def reg():
    validEmail, validPass = False, False
    while(not validEmail or not validPass):
        new_user_email = input("Enter Your Email: ")
        validEmail = validateEmail(new_user_email)
        if not validEmail:
            continue
        new_user_name = input("Enter Your username: ")
        new_user_password = getpass()
        validPass = validatePass(new_user_password)
        print(validPass)

    db_instance = Database(config)
    db_instance.connect()
    #db.select_rows("""Select * from users""")
    rows = db_instance.select_rows("""SELECT * from users""")
    new_user_id = len(rows) + 1
    db_instance.insert(new_user_id,new_user_name,new_user_password,new_user_email)
    db_instance.close_Connection()
    startApp()


def mainApp(user):
    print(
        """
            Welcome to your user portal, %s !

            Your details,
            NAME: %s
            EMAIL: %s
        """
    % (user[1],user[1],user[3]))
    print(
    """
        press p to update any of your details
        press d to delete your account
        press l to logout
    """
    )
    inp = input("  Enter Your option:  ")
    while(True):
        if inp == "p":
            db_instance = Database(config)
            db_instance.connect()
            print(
                """
                    1. Username
                    2. Password
                    3. Email
                """
            )
            option = int(input("choose an option from above"))
            if(option == 1):
                detail = input("Enter new username: ")
            elif(option == 2):
                oldpass = getpass("Enter old password: ")
                if(oldpass == user[2]):
                    detail = getpass("Enter new password: ")

            else:
                detail = input("Enter new email: ")
            db_instance.update(user[0],detail,option)
            db_instance.close_Connection()
            mainApp(user)

        elif inp == "d":
            db_instance = Database(config)
            db_instance.connect()
            db_instance.delete(user[0])
            db_instance.close_Connection()
            mainApp(user)

        elif inp == "l":
            startApp()
            break

def login():
    print("login")
    login_name = input("Enter your username: ")
    login_pass = getpass()
    db_instance = Database(config)
    db_instance.connect()
    data = (login_name, login_pass)
    find = db_instance.run_query("""SELECT * from users WHERE user_name = %s AND password = %s""",data)
    if len(find) > 0:
        logger.success("Logged In successfully")
    mainApp(find[0])

def startApp():
    print(
    """
        Welcome user !
        Please authorize.
    """
    )
    new_user = input("Do you already have an account ? (y/n): ")

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

startApp()
