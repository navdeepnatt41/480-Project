from Backend import client_backend

def handle_client() -> None:
    """
    Entry point for the Client menu.
    Allows registration, login, and returning to the main menu.
    After successful login, directs to the client main menu.
    """
    while True:
        print("\n=== Client Portal ===")
        print("1: Register")
        print("2: Login")
        print("3: Return to Main Menu")
        user_opt: str = input("Select an option: ")
        match user_opt:
            case "1":
                handle_client_registration()
            case "2":
                if handle_client_login():
                    client_main_menu()
            case "3":
                print("Leaving Client Menu...")
                return
            case _:
                print("Invalid option. Please try again.")

def handle_client_registration() -> None:
    """
    Registers a new client by collecting their name, email, addresses, and credit cards.
    Clients may have multiple addresses and credit cards (payment addresses may differ).
    """
    print("\n=== Client Registration ===")
    name: str = input("Enter your name: ")
    email: str = input("Enter your email: ")

    addresses = []
    print("Enter your addresses (type 'done' to finish):")
    while True:
        addr = input("Address: ")
        if addr.lower() == "done":
            break
        addresses.append(addr)

    credit_cards = []
    print("Enter your credit cards with billing address (type 'done' to finish):")
    while True:
        card_number = input("Card Number: ")
        if card_number.lower() == "done":
            break
        billing_address = input("Billing Address for this card: ")
        credit_cards.append((card_number, billing_address))

    success = client_backend.register_client(name, email, addresses, credit_cards)
    if success:
        print("Registration successful!")
    else:
        print("Registration failed. Email may already be registered.")

def handle_client_login() -> bool:
    """
    Logs in an existing client using their email.
    Returns True if login is successful, False otherwise.
    """
    print("\n=== Client Login ===")
    email: str = input("Enter your email to login: ")
    if client_backend.client_login(email):
        print("Login successful. Welcome back!")
        return True
    else:
        print("Login failed. Please register first.")
        return False

def client_main_menu() -> None:
    """
    Lists all client options after login and handles user selection.
    """
    while True:
        print("\n=== Client Main Menu ===")
        client_options: list[str] = [
            "1. View Available Car Models by Date",
            "2. Book a Rent (Assign Any Available Driver)",
            "3. View Your Booked Rents",
            "4. Review a Driver",
            "5. Book a Rent with the Best Driver for a Model",
            "6. Logout"
        ]
        print("\n".join(client_options))
        selection = input("Select an option: ")
        match selection:
            case "1":
                handle_view_available_car_models()
            case "2":
                handle_book_rent()
            case "3":
                handle_view_booked_rents()
            case "4":
                handle_review_driver()
            case "5":
                handle_book_best_driver_rent()
            case "6":
                print("Logging out...")
                return
            case _:
                print("Invalid option. Please try again.")

def handle_view_available_car_models() -> None:
    """
    Prompts the client for a date D and displays available car models on that date.
    """
    print("\n=== Available Car Models by Date ===")
    date: str = input("Enter the date (YYYY-MM-DD): ")
    client_backend.view_available_car_models_by_date(date)

def handle_book_rent() -> None:
    """
    Allows the client to book a rent by selecting an available car model on a specific date.
    Assigns any arbitrary available driver who can drive the selected model.
    """
    print("\n=== Book a Rent ===")
    date: str = input("Enter the date for the rent (YYYY-MM-DD): ")
    model: str = input("Enter the car model you'd like to book: ")
    client_backend.book_rent_any_driver(date, model)

def handle_view_booked_rents() -> None:
    """
    Allows the client to view all their booked rents, including car model and assigned driver.
    """
    print("\n=== Your Booked Rents ===")
    email: str = input("Confirm your email to view rents: ")
    client_backend.view_client_rents(email)

def handle_review_driver() -> None:
    """
    Allows the client to review a driver if they were assigned to a rent booked by the client.
    """
    print("\n=== Review a Driver ===")
    email: str = input("Confirm your email: ")
    driver_name: str = input("Enter the driver's name you want to review: ")
    rating: float = float(input("Enter your rating for the driver (1-5): "))
    review: str = input("Enter your review comment: ")
    client_backend.review_driver(email, driver_name, rating, review)

def handle_book_best_driver_rent() -> None:
    """
    Allows the client to book a rent with the best available driver (highest avg. rating)
    who can drive the requested car model on the given date.
    """
    print("\n=== Book a Rent with the Best Driver ===")
    date: str = input("Enter the date for the rent (YYYY-MM-DD): ")
    model: str = input("Enter the car model you'd like to book: ")
    client_backend.book_rent_best_driver(date, model)

