import manage_product
import manage_user
import manage_cart
import total_functions


def main_menu():

    while True:
        main_choice = input(
            "What collection do you want to work with? (Users / Carts / Products / Total / Quit): ")
        if main_choice == "Products":
            manage_product.show__products()
        elif main_choice == "Users":
            manage_user.login_user()
        elif main_choice == "Carts":
            manage_cart.show_cart_operation()
        elif main_choice == "Total":
            total_functions.show_total_options()
        elif main_choice == "Quit":
            break
        else:
            print("Invalid choice. Please try again.")


# block to allow the code to be imported without running the main_menu() function.
if __name__ == "__main__":
    main_menu()
