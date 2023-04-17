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
my_collection_user = configration.getDBconnection("users")


cart_ID = ""
new_product_data = {}


class Carts():
    def __init__(self, cart_created_at, cart_products, cart_status, cart_abandoned_date, cart_paid_date,
                 cart_total_price, cart_discount, cart_payment_methods, cart_location):
        self.qualites = {"cart_created_at": cart_created_at, "cart_products": cart_products,
                         "cart_status": cart_status, "cart_abandoned_date": cart_abandoned_date,
                         "cart_paid_date": cart_paid_date, "cart_total_price": cart_total_price,
                         "cart_discount": cart_discount, "cart_payment_methods": cart_payment_methods,
                         "cart_location": cart_location}


def show_cart_operation():
    """Main  Cart Operations"""
    print("=" * 40 + "\n" + "=" * 40)
    print(show_cart_operation.__doc__)
    print("=" * 40 + "\n" + "=" * 40)

    main_menu_list = {"s": show_user_carts,
                      "a": add_new_product,
                      "m": update_cart,
                      #   "c": delete_cart,
                      "q": "Quite"
                      }
    action = ""
    while action != "q":
        # if user:
        #     print("=" * 40 +"\n" +"=" * 40 )
        for key, value in main_menu_list.items():
            # check if the value is a function
            if callable(value):
                print(f"{key}) {value.__doc__}")
            else:
                # print the quit option in the desired syntax
                print(f"{key}) {value}")
        action = input("\nAction?")
        if action in main_menu_list:
            if action != "q":
                main_menu_list[action]()
            else:
                return


def show_user_carts():
    """User Carts List"""
    # Enter user ID
    user_ID = input("\n Enter the user ID : ")
    try:
        user_ID = ObjectId(user_ID)
    except:
        print("=" * 40 + "\n" + "=" * 40)
        print(f'{user_ID} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
        return
    myquery = {"_id": user_ID}

    user_carts = my_collection_user.find_one(myquery)
    if len(user_carts) == 0:
        print("\nThis user is not exist.. try again with another ID")
        return
    else:
        print(f'\n list of user carts : ')
        for cart in user_carts['users_carts']:
            # cart_detailes = my_collection_carts.find_one(
            #     {'_id': cart['_id']})
            # print(
            #     f"cart products :{cart_detailes['cart_products']} \n  cart status:{cart_detailes['cart_status']} \n total price :{cart_detailes['cart_total_price']} ")
            # print(f' \n{cart}')
            myquery = {"_id": ObjectId(cart)}
            cart = my_collection_carts.find_one(myquery)
            if len(cart) == 0:
                print("\nThis cart is not exist.. try again with another ID")
                return
            else:
                print(
                    f"\ncart status : {cart['cart_status']} \n cart total price : {cart['cart_total_price']}  \n")
                print("You cart's product : ")
                for pro in cart['cart_products']:
                    print(f"\n {pro}")
                print('\n')

        # update_cart()


def creat_new_cart(user_id):
    """Create new cart"""
    cart_created_at = datetime.datetime.now()
    cart_status = "pending"
    cart_paid_date = ""
    cart_discount = ""
    cart_location = []
    cart_products = [new_product_data]
    cart_abandoned_date = ""
    cart_total_price = new_product_data['prodcts_price']
    cart_payment_methods = []
    cart = Carts(cart_created_at, cart_products, cart_status, cart_abandoned_date, cart_paid_date,
                 cart_total_price, cart_discount, cart_payment_methods, cart_location)
    newCart = cart.qualites
    add_new_cart_result = my_collection_carts.insert_one(newCart)
    if add_new_cart_result.acknowledged:
        print('\n' + '=' * 40 + '\n')
        print(
            f'\nYour New cart \n: {new_product_data} is added succesfully ...')
        print("=" * 40 + "\n" + "=" * 40)
        new_cart_id = add_new_cart_result.inserted_id
        if user_id != "":
            user_id = ObjectId(user_id)
            add_cart_user = my_collection_user.update_one(
                {"_id": user_id}, {"$push": {"users_carts": new_cart_id}})
        show_cart_operation()


def add_to_existing_cart():
    """Add to existing cart"""
    user_ID = input("\n\nEnter user ID : ")
    try:
        user_ID = ObjectId(user_ID)
    except:
        print("=" * 40 + "\n" + "=" * 40)
        print(f'{user_ID} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
        return
    user_carts = my_collection_user.find_one({'_id': user_ID})
    if len(user_carts) == 0:
        print("\nThis user is not register ... try agin  ")
    else:
        for cart in user_carts['users_carts']:

            filter = {"cart_status": "pending", "_id": cart}
            sort = [("cart_created_at", pymongo.DESCENDING)]
            latest_cart = my_collection_carts.find_one(
                filter=filter, sort=sort)
            # filter=filter, sort=sort

            if len(latest_cart) != 0:
                global cart_ID
                cart_ID = latest_cart['_id']
            else:
                creat_new_cart(user_ID)

        if cart_ID != "":
            # print(cart_ID)
            add_pro = my_collection_carts.update_one(
                {"_id": cart_ID}, {"$push": {"cart_products": new_product_data}})
            if add_pro.matched_count > 0:
                cart_doc = my_collection_carts.find_one({"_id": cart_ID})
                total_price = 0
                for product in cart_doc["cart_products"]:
                    total_price += int(product["prodcts_price"])

                    my_collection_carts.update_one(
                        {"_id": cart_ID}, {"$set": {"cart_total_price": total_price}})
                    print(
                        f"\nYour new product : {new_product_data }  is added successfully")
        else:
            creat_new_cart(user_ID)


def add_new_product():
    """Add new product to the cart"""
    # Enter pro ID nad pro QUA from user
    new_product_ID = input("\n Enter the ID of product you like : ")
    try:
        new_product_ID = ObjectId(new_product_ID)
    except:
        print("=" * 40 + "\n" + "=" * 40)
        print(f'{new_product_ID} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
        return

    new_product_Qua = input("\n Enter the quantity of this product  : ")
    try:
        new_product_Qua = int(new_product_Qua)
    except:
        print("\nThis quantity is not digits.. try again")

    myquery = {"_id": new_product_ID}
    # check if this product is in the list of products
    new_product_info = my_collection_products.find_one(myquery)
    print(new_product_info)
    if len(new_product_info) == 0:
        print("\nThis product is not exist.. try again with another one")
        return
    else:
        pro_price = int(new_product_info['price'])
        all_pro_price = new_product_Qua*pro_price
        # Final question about which cart
        global new_product_data
        new_product_data = {"pro_id": new_product_ID,
                            "pro_qua": new_product_Qua,
                            "prodcts_price": all_pro_price}

        cart = input("\nAdd product to last cart : Yes/No ? ")
        if cart == "Yes":
            # get the id for catrs the latest cart added
            add_to_existing_cart()
        else:
            user_id = ""
            creat_new_cart(user_id)


def update_cart():
    """Modify your carts"""
    print("=" * 40 + "\n")
    print(update_cart.__doc__)
    print("=" * 40 + "\n")
    update_menu_list = {"u": modify_cart.update_cart_field,
                        "d": modify_cart.delete_cart,
                        "q": "Quite"
                        }
    action = ""
    while action != "q":
        # if user:
        #     print("=" * 40 +"\n" +"=" * 40 )
        for key, value in update_menu_list.items():
            # check if the value is a function
            if callable(value):
                print(f"{key}) {value.__doc__}")
            else:
                # print the quit option in the desired syntax
                print(f"{key}) {value}")
        action = input("\nAction?")
        if action in update_menu_list:
            if action != "q":
                update_menu_list[action]()
            else:
                return


def delete_cart():
    """Delete your carts"""
