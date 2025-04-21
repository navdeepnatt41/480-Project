from manager_menu import handle_manager
from driver_menu import handle_driver
from client_menu import handle_client

def greeting_and_get_role() -> None:
    """
    This function presents the opening greeting and prompts the user to select a role.
    """
    print("Hello! Please select your role OR 'x' to exit:")
    print("1. Manager")
    print("2. Driver")
    print("3. Client")
    role = input("Enter the number corresponding to your role: ")
    match role:
        case "1":
            handle_manager()
        case "2":
            handle_driver()
        case "3":
            handle_client()
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