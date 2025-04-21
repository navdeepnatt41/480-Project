def handle_manager() -> None:
    """
    This function handles the manager menu. 
    """
    print("Welcome, Manager!")
    print("Please select one of the following")
    user_options: list[str] = ["1: Register", "2: Login"]
    print("\n".join(user_options)) 
    user_selection: str = input("Input Command: ")
    return None
