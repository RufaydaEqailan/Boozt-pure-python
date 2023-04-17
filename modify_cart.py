import pymongo
from pymongo import MongoClient
import configration
import pprint
import modify_cart
from bson import ObjectId
import datetime
import re
import getpass
import manage_user

my_collection_carts = configration.getDBconnection("carts")
my_collection_products = configration.getDBconnection("product")


def update_cart_field():
    """Update Your Cart"""
    # Enter cart ID
    cart_ID = input("\n \n Enter the cart ID which you want to update : ")
    try:
        cart_ID = ObjectId(cart_ID)
    except:
        print("=" * 40 + "\n" + "=" * 40)
        print(f'{cart_ID} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
        return

    myquery = {"_id": cart_ID}
    cart = my_collection_carts.find_one(myquery)
    if len(cart) == 0:
        print("\nThis cart is not exist.. try again with another ID")
        return
    else:
        for pro in cart['cart_products']:
            print(f"\n {pro}")
        print('\n')

    pro_ID = input(
        "\n  Enter the product ID which you want to update the Quantity : ")
    try:
        pro_ID = ObjectId(pro_ID)
    except:
        print("=" * 40 + "\n" + "=" * 40)
        print(
            f'{pro_ID} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
        return

    documents = my_collection_carts.find_one(
        {"cart_products.pro_id": {"$in": [pro_ID]}})
    if len(documents) == 0:
        raise ValueError("Product not found in cart.")
    else:
        # print("Product not found in cart.")
        new_pro_Qua = input("\n what is the new quantity for this product : ")
        try:
            new_pro_Qua = int(new_pro_Qua)
        except:
            print("\nThe price you enter is not numerical data ... try again .\n")
        # make for loop 
        myquery = {"cart_products.pro_id": ObjectId(pro_ID)}
        update = {"$set": {"cart_products.$.pro_qua": new_pro_Qua}}
        # print(update)
        update_qua=my_collection_carts.update_one(myquery, update)
        if update_qua.matched_count>0:
             print("ok")
        #     myquery={"_id":ObjectId(pro_ID)}
        #     new_product_info = my_collection_products.find_one(myquery)
        #     # print(myquery)
        #     if len(new_product_info) == 0:
        #         print("\nThis product is not exist.. try again with another one")
        #         return
        #     else:
        #         pro_price = int(new_product_info['price'])
        #         all_pro_price = new_pro_Qua*pro_price
        #         new_product_data = {"pro_id": pro_ID,
        #                             "pro_qua": new_pro_Qua,
        #                             "prodcts_price": all_pro_price}
        #         edit_cart = my_collection_carts.update_one(
        #             {"_id": cart_ID}, {"$set": {"cart_products": new_product_data}})
        #         if edit_cart.matched_count > 0:
        #             cart_doc = my_collection_carts.find_one({"_id": cart_ID})
        #             total_price = 0
        #             for product in cart_doc["cart_products"]:
        #                 # product["prodcts_price"]=int(product["prodcts_price"])
        #                   print(product["prodcts_price"])
        #                 # total_price +=product["prodcts_price"] 

        # #             my_collection_carts.update_one(
        # #                 {"_id": cart_ID}, {"$set": {"cart_total_price": total_price}})
        # #             print(
        # #                 f"\nYour new product : {new_product_data }  is updated successfully")
        #         else:
        #             print("There is error during update..")
        else:
             print("There is error during update..")
# 1267296

def delete_cart():
    """Delete Your Cart"""
    # Enter cart ID
    cart_ID = input("\n \n Enter the cart ID which you want to update : ")
    try:
        cart_ID = ObjectId(cart_ID)
    except:
        print("=" * 40 + "\n" + "=" * 40)
        print(f'{cart_ID} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
        return

    myquery = {"_id": cart_ID}
    delete_cart = my_collection_carts.delete_one(myquery)
    if len(delete_cart) == 0:
        print("\nThis cart is not exist.. try again with another ID")
    else:
        print("\nThis cart is deleted successfully...")
