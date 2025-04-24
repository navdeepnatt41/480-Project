from Backend import manager_backend

def handle_manager() -> None:
    """
    Entry point for the Manager menu.
    Allows registration, login, and returning to the main menu.
    """
    while True:
        print("\n=== Manager Portal ===")
        print("1: Register")
        print("2: Login")
        print("3: Exit to Main Menu")
        user_selection: str = input("Select an option: ")
        match user_selection:
            case "1":
                handle_manager_registration()
            case "2":
                if handle_manager_login():
                    manager_main_menu()
            case "3":
                print("Returning to Main Menu...")
                return
            case _:
                print("Invalid option. Please try again.")

def handle_manager_registration() -> None:
    """
    Registers a new manager by collecting name, email, and SSN.
    """
    print("\n=== Manager Registration ===")
    name: str = input("Enter your name: ")
    email: str = input("Enter your email: ")
    ssn: str = input("Enter your SSN: ")
    success = manager_backend.register_manager(name, email, ssn)
    if success:
        print("Registration successful!")
    else:
        print("Registration failed. SSN may already be registered.")

def handle_manager_login() -> bool:
    """
    Logs in an existing manager using their SSN.
    Returns True if login is successful, False otherwise.
    """
    print("\n=== Manager Login ===")
    ssn: str = input("Enter your SSN to login: ")
    if manager_backend.manager_login(ssn):
        print("Login successful. Welcome back!")
        return True
    else:
        print("Login failed. Please register first.")
        return False

def manager_main_menu() -> None:
    """
    Main menu for logged-in managers, listing all available actions.
    """
    while True:
        print("\n=== Manager Main Menu ===")
        manager_options: list[str] = [
            "1. Insert/Remove Cars or Models",
            "2. Insert/Remove Drivers",
            "3. View Top-K Clients by Number of Rents",
            "4. View All Models and Rent Counts",
            "5. View All Driver Info (Total Rents & Avg. Rating)",
            "6. Query Clients by Client and Driver Cities",
            "7. Report Problematic Drivers (Chicago Rating Filter)",
            "8. Report Brand-wise Avg. Driver Rating and Rent Count",
            "9. Logout"
        ]
        print("\n".join(manager_options))
        selection = input("Select an option: ")
        match selection:
            case "1":
                handle_insert_remove_cars()
            case "2":
                handle_insert_remove_drivers()
            case "3":
                handle_top_k_clients()
            case "4":
                handle_models_rent_counts()
            case "5":
                handle_driver_info()
            case "6":
                handle_query_clients_by_cities()
            case "7":
                handle_problematic_drivers()
            case "8":
                handle_brand_avg_rating_rents()
            case "9":
                print("Logging out...")
                return
            case _:
                print("Invalid option. Please try again.")

# === Below are stubs for each requirement ===

def handle_insert_remove_cars() -> None:
    """
    Allows the manager to insert or remove car models.
    """
    print("\n=== Insert/Remove Cars ===")
    # Call relevant backend logic here (manager_backend.insert/remove_car())

def handle_insert_remove_drivers() -> None:
    """
    Allows the manager to insert or remove drivers and their information.
    """
    print("\n=== Insert/Remove Drivers ===")
    # Call relevant backend logic here (manager_backend.insert/remove_driver())

def handle_top_k_clients() -> None:
    """
    Prompts for a number k and displays the top-k clients by number of rents.
    """
    print("\n=== Top-K Clients ===")
    k = int(input("Enter the number k: "))
    manager_backend.get_top_k_clients(k)

def handle_models_rent_counts() -> None:
    """
    Lists every current car model and its corresponding number of rents.
    """
    print("\n=== Models and Rent Counts ===")
    manager_backend.list_models_and_rent_counts()

def handle_driver_info() -> None:
    """
    Lists each driver's name, total number of rents, and average rating.
    """
    print("\n=== Driver Info ===")
    manager_backend.list_driver_info()

def handle_query_clients_by_cities() -> None:
    """
    Retrieves clients who have at least one address in city C1 and have booked
    rents where the driver has an address in city C2.
    """
    print("\n=== Query Clients by Cities ===")
    city_c1 = input("Enter the client address city (C1): ")
    city_c2 = input("Enter the driver address city (C2): ")
    manager_backend.get_clients_by_client_and_driver_cities(city_c1, city_c2)

def handle_problematic_drivers() -> None:
    """
    Lists problematic local drivers (Chicago, avg. rating < 2.5, and meet other conditions).
    """
    print("\n=== Problematic Drivers ===")
    manager_backend.report_problematic_drivers()

def handle_brand_avg_rating_rents() -> None:
    """
    Lists car brands, average ratings of eligible drivers, and number of rents per brand.
    """
    print("\n=== Brand Avg. Driver Rating and Rent Count ===")
    manager_backend.report_brand_driver_stats()

