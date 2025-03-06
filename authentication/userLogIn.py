from services.services import UserService

def login_user(username, password):
    # Try to fetch user by username
    user = UserService().get(username=username).first()

    # If user not found, try to fetch by email
    if not user:
        user = UserService().get(email=username).first()

    # Check if the user exists and password is correct
    if user and user.check_password(password):
        return user
    return None