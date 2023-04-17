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
field_name=""
old_field_value=""
new_field_value=""
user_ID=123

def modify_user_list(user_id):
    """Modify User Account"""
    print("=" * 40 +"\n" +"=" * 40 )
    print("Modifications User Information List")
    print("=" * 40 +"\n" +"=" * 40 )
    sub_menu={
                "u":modify_users_name,
                "p":modify_users_payment_methods,
                "cc":modify_users_credit_card,
                "e":modify_users_email,
                "pw":modify_users_password,
                "s":modify_users_status,
                "q":"Back to Main menu"
                }
    next_action=""
    for key, value in sub_menu.items():
        # check if the value is a function
        if callable(value):
            print(f"{key}) {value.__doc__}")
        else:
        # print the quit option in the desired syntax
            print(f"{key}) {value}")
            
    next_action=input("\nAction?")
    if next_action in sub_menu:
        if  next_action!="q":
             global user_ID
             user_ID=user_id
             sub_menu[next_action]()
        else:
            return

def modify_user_account():
    """modify_user_account"""
    global user_ID
    user_ID=ObjectId(user_ID)
    myquery={"_id":user_ID}

    user_information=my_collection.find_one(myquery)
    if len(user_information)!=0:
            global old_field_value
            old_field_value=user_information[field_name]

            print(f"\nYour Old {field_name} : {old_field_value}")
            new_query = { "$set": { field_name: new_field_value } }

            modify_result=my_collection.update_one(myquery, new_query)
            if modify_result.matched_count>0:
                 print(f"\n Your {field_name} is updated successfully to : {new_field_value} ")
            else:
                 print("\nThere is something wrong  happend... Try again later")
    else:
        print("\nThis user is not exiest...")

    modify_user_list(user_ID)

def modify_users_name():
    """modify_users_name"""
    global field_name
    field_name="users_name"

    global new_field_value
    new_field_value=input("\n What is the new name :")
    
    modify_user_account()

def modify_users_payment_methods():
    """modify_users_payment_methods"""
    global field_name
    field_name="users_payment_methods"

    global new_field_value
    new_field_value=[]

    available_methods=["VISA","PayPal","Master"]
    alternative_methods=input("\n Enter the number of methods you want to add (MAX 3nr,) : ")
    for i in range(int(alternative_methods)):
        paymentmethod=input(f"\nFrom this list [VISA,PayPal,Master] Enter paymentmetod nr{i+1} : ")
        if paymentmethod in available_methods:
            new_field_value.append(paymentmethod)
        else:
            print(f"The paymentmethod {paymentmethod} is not in the available payment method list [VISA,PayPal,Master] .")

    modify_user_account()

def modify_users_credit_card():
    """modify_users_credit_card"""
    global field_name
    field_name="users_credit_card"

    global new_field_value
    new_field_value=input('\nEnter the new value of Cridet card  field in the right format 16 Digits : ')
    if  len(new_field_value)==16:
        #print(len(field_value)) 
        part_one=new_field_value[0:4]
        part_two=new_field_value[4:8]
        part_three=new_field_value[8:12]
        part_four=new_field_value[12:16]
        new_field_value=part_one+" "+part_two+" "+part_three+" "+part_four
        modify_user_account()
    else:
        print("\nThe cridet card is wrong (Less\More) 16 Digit ..  ")
        modify_user_list(user_ID)

def modify_users_email():
    """modify_users_email"""
    global field_name
    field_name="users_email"

    global new_field_value
    new_field_value=input('\nEnter the new value of Email field in the right format test@test.com : ')

    #"validation email goes here"
    email_pattern="([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    
    if  re.search(email_pattern, new_field_value)==None:
        print("\nNot valid email formate , must be like this formate: name.surname@gmail.com")
        modify_user_list(user_ID)
    else:
        modify_user_account()

def modify_users_password():
    """modify_users_password"""
    global field_name
    field_name="users_password"

    global new_field_value
    new_field_value=input("\n What is the new password :")

    modify_user_account()

def modify_users_status():
    """modify_users_status"""
    global field_name
    field_name="users_status"

    global new_field_value
    new_field_value=input("\n What is the new status :")

    modify_user_account()
