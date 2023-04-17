import pymongo
from pymongo import MongoClient
import configration
import pprint
import modify_user
from bson import ObjectId
import datetime
import re
import getpass


my_collection=configration.getDBconnection("users")
user_ID=123456
class Users():
    def __init__(self,users_name,users_email,users_password,users_status,users_online,users_carts,users_payment_methods,users_regiterd_at,users_credit_card ):
        self.qualites={"users_name":users_name,"users_email":users_email,"users_password":users_password,"users_status":users_status,"users_online":users_online,"users_carts":users_carts,
                       "users_payment_methods":users_payment_methods,"users_regiterd_at":users_regiterd_at,"users_credit_card":users_credit_card}
def user_menu():
    """MY Users functions LIST"""
    print("=" * 40 +"\n" +"=" * 40 )
    print(user_menu.__doc__)
    print("=" * 40 +"\n" +"=" * 40 )
    global user_ID
    user_ID=ObjectId(user_ID)

    user = my_collection.find_one({"_id":user_ID })
    main_menu_list={
                    # "s":search_value_user_account,
                    "c":delete_user_account,
                    "mc":deactive_user_account,
                    "m":modify_user_account,
                    "s":show_user_account,
                    "q":"Logout"
                }
    action=""
    while action !="q":
        # if user:
        #     print("=" * 40 +"\n" +"=" * 40 )
        for key, value in main_menu_list.items():
            # check if the value is a function
            if callable(value):
                print(f"{key}) {value.__doc__}()")
            else:
            # print the quit option in the desired syntax
                print(f"{key}) {value}")
        action=input("\nAction?")
        if action in main_menu_list:
            if  action!="q":
                 main_menu_list[action]()
            else:
                return
            
def activation_user():
    """activation new user"""
    users_status="active"
    global user_ID
    user_ID=ObjectId(user_ID)
    myquery = { "_id":user_ID}
    newvalues = { "$set": { "users_status": "active" } }
    activation_result=my_collection.update_many(myquery, newvalues)
    if activation_result.matched_count>0:
        print(f"\nThe user is activated now ")
        user_menu()
    else:
        print("\nThere is something wrong  happend... Try again later")

def  user_register():
    """User Registeration"""
    print("=" * 40 +"\n" +"=" * 40 )
    print(user_register.__doc__)
    print("=" * 40 +"\n" +"=" * 40 )

    users_name = input("\nName of the user?:")

    #"validation email goes here"
    email_pattern="([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    email_value=input('\nEnter the new value of Email field in the right format test@test.com : ')
    if  re.search(email_pattern, email_value)==None:
        print("\nNot valid email formate , must be like this formate: name.surname@gmail.com")     
    users_email=email_value

    users_password= getpass.getpass("\Enter Password, password should be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character?:")

    users_status="pending"
    users_online=""
    users_carts=[]
    users_payment_methods=[]
    users_regiterd_at=datetime.datetime.now()
    users_credit_card=""
    
    user=Users(users_name,users_email,users_password,
               users_status,users_online,users_carts,
               users_payment_methods,users_regiterd_at,
               users_credit_card
               )
    new_user=user.qualites
    insert_result = my_collection.insert_one(new_user)
    inserted_id = insert_result.inserted_id
    
    if insert_result.acknowledged:
                print('\n' + '=' * 40 + '\n')
                active=input(f'\nUser {users_name} is registered succesfully ...\n please press Y to active your account : Y/N .')
                if(active=="Y"):
                     global user_ID
                     user_ID=inserted_id
                     activation_user()
                else:
                     print("Something wrong.. please try again")

                print("=" * 40 +"\n" +"=" * 40 )
                
def login_user():
    """Login User"""
    print("=" * 40 +"\n" +"=" * 40 )
    print(login_user.__doc__)
    print("=" * 40 +"\n" +"=" * 40 )

    user_email=input("\n Enter the email in the right  format  :  ")
    email_pattern="([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    if re.search(email_pattern, user_email)==None:
            print("Not valid email formate , must be like this formate: name.surname@gmail.com")
            return
    user_password=getpass.getpass("\n Enter  Password : ")

    query={"users_email":user_email, "users_password":user_password}
    user=my_collection.find_one(query)

    if user!=None:
        # print("you are login now")
        # print("=" * 40 +"\n"  )

        query={"_id":user["_id"],"users_status":"active"}
        user_status=my_collection.find_one(query)
        global user_ID
        user_ID=user["_id"]
        if user_status!=None:
            query={"_id":user["_id"]}
            newvalues = { "$set":{"users_online":datetime.datetime.now()}}
            user_update=my_collection.update_one(query,newvalues)
            if user_update.matched_count>0:
                print("you are login now")
                user_menu()
            else:
                print("\nThere is something wrong  happend... Try again later")
        else:
            print("\nThis user has terminated account")
            user_activation=input("\n Please active your account .. Press Yes for activation, No for Quite (Yes/No) ?")
            if user_activation=="Yes":
                activation_user()
            else:
                return 
    else:
        print("\nEmail or password is wrong.. try again ")
        print("=" * 40 +"\n"  )
        user_registeration=input("\n If tou don't have an account .. Press Yes for registeration, No for Quite (Yes/No) ?")
        if user_registeration=="Yes":
            user_register()
        else:
             return
        
def modify_user_account():
    """Modify Your Account"""
    global user_ID
    user_ID=ObjectId(user_ID)
    myquery={"_id":user_ID}
    user_information=my_collection.find_one(myquery)
    if len(user_information)==0:
        login_user()
    else:
        modify_user.modify_user_list(user_ID)

def delete_user_account():
    """Delete You Account"""
    global user_ID
    user_ID=ObjectId(user_ID)
    query={"_id":user_ID}
    delete_result=my_collection.delete_one(query)
    if delete_result.deleted_count == 1:
        print("User deleted successfully.")
        login_user()
    else:
        print("There was a problem.. Try again Later.")

def deactive_user_account():
    """Deactive Your Account"""
    users_status="terminated"
    global user_ID
    user_ID=ObjectId(user_ID)
    myquery = { "_id":user_ID}
    newvalues = { "$set": { "users_status": "terminated" } }
    activation_result=my_collection.update_many(myquery, newvalues)
    if activation_result.matched_count>0:
        print(f"\nThe user is Deactivated now ")
        login_user()
    else:
        print("\nThere is something wrong  happend... Try again later")

def show_user_account():
    """Show Detailes About Your Account"""   
    print("=" * 40 +"\n" +"=" * 40 )
    print(show_user_account.__doc__)
    print("=" * 40 +"\n" +"=" * 40 )

    global user_ID
    user_ID=ObjectId(user_ID)
    myquery={"_id":user_ID}
    account_result=my_collection.find_one(myquery)
    if len(account_result)==0:
        login_user()
    else:
        print(account_result)

