from CLI import client_menu, driver_menu, manager_menu 
from Backend import Postgres_DB_conn as db_conn

def get_db_cursor():
    """
    Connects to the application DB on postgres and returns a cursor 
    """
    _, cursor = db_conn.create_conn_cursor()
    return cursor


def greeting_and_get_role() -> None:
    """
    This function presents the opening greeting and prompts the user to select a role.
    """
    db_cursor = get_db_cursor()
    print("Hello! Please select your role OR 'x' to exit:")
    print("1. Manager")
    print("2. Driver")
    print("3. Client")
    role: str = input("Enter the number corresponding to your role: ")
    match role:
        case "1":
            manager_menu.handle_manager(cursor)
        case "2":
            driver_menu.handle_driver(cursor)
        case "3":
            client_menu.handle_client(cursor)
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