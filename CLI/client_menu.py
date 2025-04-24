def handle_client(cursor) -> None:
    """
    This function handles the client login menu. After-wards, control is passed
    to the actual client menu
    """
    print("Welcome, Driver!")
    print("Please select one of the following")
    user_options: list[str] = ["1: Register", "2: Login", "3: Return to Main Menu"]
    print("\n".join(user_options))
    user_opt: str = input("Option Number: ")
    match user_opt:
        case "1":
            handle_registration()
        case "2":
            handle_login()
            handle_client()
        case "3":
            print("Leaving Driver Menu...") 
            return None 
        case _:
            print("Bad Option - Please try again ")
    return None


def handle_registration() -> None:
    """
    Client inputs their name, email, address(s), and credit card(s) 
    and it's entered to the database. 
    """
    user_name: str = input("Please enter the following pieces of information: ")
    # To-Do: Pass the name to Backend Logic to insert into DB
    print("New User Registered. Returning to driver menu...")
    return 

def handle_login() -> None:
    """
    Manager merely logins with their email. 
    """
    user_name: str = input("Please enter your email, returning client: ")
    # To-Do: Pass the email to Backend Logic to check if they're in the DB.
    # If they exist, send them to Client-Login Menu; else, back to Client-Main
    # with a message saying they need to register first
    return

def client_main_menu() -> None:
    """
    This menu lists all of the possible client menu options 
    """
    print("Client Main Menu: Please select an option")
    client_options: list[str] = [
        "1. Available car models by date",
        "2. Book a rent",
        "3. View your rents",
        "4. Review a driver!",
        "5. Book a rent: best driver by model"
    ]
    print("\n".join(client_options))
    match input(">"):
        case "1":
            handle_date_car_models()
        case "2":
            handle_rent_booking()
        case "3":
            handle_rent_viewing()
        case "4":
            handle_driver_review()
        case "5":
            handle_best_driver_rent()
       
def handle_date_car_models():
    pass

def handle_rent_booking():
    pass

def handle_rent_viewing():
    pass

def handle_driver_review():
    pass

def handle_best_driver_rent():
    pass
