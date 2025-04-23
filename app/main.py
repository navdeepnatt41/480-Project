from CLI import client_menu, driver_menu, manager_menu 

def greeting_and_get_role() -> None:
    """
    This function presents the opening greeting and prompts the user to select a role.
    """
    print("Hello! Please select your role OR 'x' to exit:")
    print("1. Manager")
    print("2. Driver")
    print("3. Client")
    role: str = input("Enter the number corresponding to your role: ")
    match role:
        case "1":
            manager_menu.handle_manager()
        case "2":
            driver_menu.handle_driver()
        case "3":
            client_menu.handle_client()
        case "x":
            return 
        case _:
            print("Invalid role selected. Please try again.")
            greeting_and_get_role()

def main():
    """
    Main function to execute the CLI application.
    """
    greeting_and_get_role()

if __name__ == "__main__":
    main()    