"""
Creates the Client Menus
"""

import Backend.db_conn as db
import utils
import re

def available_car_models(email):
    pass

def book_rent(email):
    pass

def list_client_rents(email):
    pass

def review_driver(email):
    pass

def book_model_best_driver(email):
    pass

MENU_OPTIONS = {
    "1":available_car_models,
    "2":book_rent,
    "3":list_client_rents,
    "4":review_driver,
    "5":book_model_best_driver
}

def client_main_menu(email: str):
    while True:
        print("-------------------------------------")
        print("Welcome to the main menu. Please select an option!")
        options = [ 
            "0. Exit to Login",
            "1. List available car models",
            "2. Book a rent",
            "3. List your Rents",
            "4. Review a Driver",
            "5. Book the Best Driver for a specific Model"
        ]
        utils.print_menu_options(options)
        command = input("> ")
        valid_commands = ["0", "1", "2", "3", "4", "5"]
        if command not in valid_commands:
            print("Invalid Command, Try Again")
        elif command == "0":
            return
        else:
            MENU_OPTIONS[command](email)

def handle_register():
    """Handles registering a client"""
    name: str = input("Enter your name: ").strip()
    email: str = input("Enter your email: ").strip()

    addrs: list[tuple[str, int, str]] = []
    print("\nEnter home addresses in the format: city,number,roadname")
    print("When you're finished, press 'n'")
    while True:
        read = input("Address or 'n' -> ").strip()
        if read.lower() == "n":
            break
        parts = [p.strip() for p in read.split(",")]
        if len(parts) != 3:
            print(" ✗ Invalid format. Use: city, number, roadname\n")
            continue
        city, number_str, roadname = parts
        try:
            house_number = int(number_str)
        except ValueError:
            print("House number must be an integer.\n")
            continue
        addrs.append((city, house_number, roadname))

    ccn_addrs: list[tuple[str, int, str, str]] = []
    print("\nEnter credit-card + payment address as: card_number,city,number,roadname")
    print("When you're finished, press 'n'")
    while True:
        read = input("CCN+PaymentAddr or 'n' -> ").strip()
        if read.lower() == "n":
            break
        parts = [p.strip() for p in read.split(",")]
        if len(parts) != 4:
            print("Invalid format. Use: card_number, city, number, roadname\n")
            continue
        ccn, city, number_str, roadname = parts
        if len(ccn) != 16 or not ccn.isdigit():
            print("Card number must be exactly 16 digits.\n")
            continue
        try:
            house_number = int(number_str)
        except ValueError:
            print(" ✗ House number must be an integer.\n")
            continue
        ccn_addrs.append((ccn, city, house_number, roadname))

    # 3) Check for existing client
    exists = db.run_sql(
        sql="""
            SELECT 1
              FROM Client
             WHERE email = %s
        """,
        vals=[email],
        is_crud=False
    )
    if exists:
        print(f"\n✗ A client with email '{email}' already exists. Aborting.\n")
        return

    db.run_sql(
        sql="INSERT INTO Client (email, client_name) VALUES (%s, %s)",
        vals=[email, name],
        is_crud=True
    )

    for city, house_number, roadname in addrs:
        db.run_sql(
            sql="""
                INSERT INTO Address (city, house_number, road_name)
                 VALUES (%s, %s, %s)
                ON CONFLICT (city, house_number, road_name) DO NOTHING
            """,
            vals=[city, house_number, roadname],
            is_crud=True
        )
        db.run_sql(
            sql="""
                INSERT INTO ClientAddress (email, city, house_number, road_name)
                 VALUES (%s, %s, %s, %s)
            """,
            vals=[email, city, house_number, roadname],
            is_crud=True
        )

    for ccn, city, house_number, roadname in ccn_addrs:
        db.run_sql(
            sql="""
                INSERT INTO Address (city, house_number, road_name)
                 VALUES (%s, %s, %s)
                ON CONFLICT (city, house_number, road_name) DO NOTHING
            """,
            vals=[city, house_number, roadname],
            is_crud=True
        )
        db.run_sql(
            sql="""
                INSERT INTO CreditCard (card_number, city, house_number, road_name, email)
                 VALUES (%s, %s, %s, %s, %s)
            """,
            vals=[ccn, city, house_number, roadname, email],
            is_crud=True
        )

    print(f"\n Registration successful for {name} ({email})!")
    client_main_menu(email)

def handle_login():
    """Handles a client's login"""
    email: str = input("Please provide your email: ")
    exists = db.run_sql(
        sql = "SELECT 1 FROM Client WHERE client_name = $s",
        vals = [email],
        is_crud = False
    )
    if exists:
        client_main_menu(email)
    else:
        print("Invalid Client")

def client_start_menu():
    """Creates the client login menu"""
    while True:
        print("Welcome, Client! Please register or login")
        options = [
            "1. Login",
            "2. Register",
            "3. Exit" 
        ]
        match (input("> ")):
            case 1:
                handle_login()
            case 2:
                handle_register()
            case 3:
                return
            case _:
                print("Returning to main menu")