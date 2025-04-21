def handle_driver() -> None:
    """
    This function handles the driver menu.
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
        case "3":
            print("Leaving Driver Menu...") 
            return None 
        case _:
            print("Bad Option - Please try again ")
    return None

def handle_registration() -> None:
    """
    Driver inputs their name and it's entered to the database. 
    Note that they don't have to enter their address at this time. 
    """
    user_name: str = input("Please enter your name, new user: ")
    # To-Do: Pass the name to Backend Logic to insert into DB
    print("New User Registered. Returning to driver menu...")
    return 

def handle_login() -> None:
    """
    Driver merely logins with their name. No need to enter their address. 
    """
    user_name: str = input("Please enter your name, returning user: ")
    # To-Do: Pass the name to Backend Logic to check if they're in the DB.
    # If they exist, send them to Driver-Login Menu; else, back to Driver-Main
    # with a message saying they need to register first
    return
