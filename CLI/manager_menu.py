def handle_manager() -> None:
    """
    This function handles the manager menu. 
    """
    print("Welcome, Manager!")
    print("Please select one of the following")
    user_options: list[str] = ["1: Register", "2: Login", "3: Exit to Main Menu"]
    print("\n".join(user_options)) 
    user_selection: str = input("Option Number: ")
    match user_selection:
        case "1":
            handle_registration()
        case "2":
            handle_login()
        case "3":
            return None
    return None

def handle_registration() -> None:
    """
    Manager inputs their name and it's entered to the database. 
    They need to enter their name, email, and ssn.
    """
    user_name: str = input("Please enter the following pieces of information: ")
    # To-Do: Pass the name to Backend Logic to insert into DB
    print("New User Registered. Returning to driver menu...")
    return 

def handle_login() -> None:
    """
    Manager merely logins with their ssn. 
    """
    user_name: str = input("Please enter your name, returning user: ")
    # To-Do: Pass the name to Backend Logic to check if they're in the DB.
    # If they exist, send them to Manager-Login Menu; else, back to Manager-Main
    # with a message saying they need to register first
    return None


def manager_main_menu() -> None:
    """
    Lists all of the manager's options 
    """
    print("Manager Main Menu: Please select an option")
    manager_options: list[str] = [
        "1. Available car models by date",
        "2. Book a rent",
        "3. View your rents",
        "4. Review a driver!",
        "5. Book a rent: best driver by model"
    ]
    print("\n".join(manager_options))
    pass