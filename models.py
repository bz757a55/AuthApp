import hashlib

# Mock database for storing user information
users_db = {}

def get_user(username):
    """Retrieve a user by username."""
    return users_db.get(username)

def verify_password(stored_password, provided_password):
    """Verify if the provided password matches the stored password."""
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

def create_user(username, password, email):
    """Create a new user in the database."""
    if username in users_db:
        return False  # User already exists
    users_db[username] = {
        'username': username,
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'email': email
    }
    return True
