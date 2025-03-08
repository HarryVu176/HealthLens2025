from datetime import datetime
import bcrypt
from database.db_connection import Database
from auth.user_model import User

class AuthHandler:
    def __init__(self):
        self.db = Database()
        self.users_collection = self.db.get_collection("users")
        self.create_indices()
    
    def create_indices(self):
        """Create necessary database indices for user collection"""
        self.users_collection.create_index("email", unique=True)
    
    def register_user(self, email, password, name=None, preferred_language="en"):
        """Register a new user"""
        # Check if user already exists
        if self.users_collection.find_one({"email": email}):
            return False, "User with this email already exists"
        
        # Create new user
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user = User(email=email, name=name, preferred_language=preferred_language)
        user_dict = user.to_dict()
        user_dict["password"] = hashed_password
        
        try:
            self.users_collection.insert_one(user_dict)
            return True, "User registered successfully"
        except Exception as e:
            return False, f"Error registering user: {str(e)}"
    
    def authenticate_user(self, email, password):
        """Authenticate user credentials"""
        user_data = self.users_collection.find_one({"email": email})
        
        if not user_data:
            return False, "Invalid email or password"
        
        stored_password = user_data.get("password")
        
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            user = User.from_dict(user_data)
            return True, user
        else:
            return False, "Invalid email or password"
    
    def get_user_by_email(self, email):
        """Retrieve user by email"""
        user_data = self.users_collection.find_one({"email": email})
        if user_data:
            return User.from_dict(user_data)
        return None
    
    def update_user(self, user):
        """Update user information"""
        user_dict = user.to_dict()
        user_dict["updated_at"] = datetime.now()
        
        try:
            self.users_collection.update_one(
                {"_id": user.user_id},
                {"$set": user_dict}
            )
            return True, "User updated successfully"
        except Exception as e:
            return False, f"Error updating user: {str(e)}"
    
    def change_password(self, email, current_password, new_password):
        """Change user password"""
        success, result = self.authenticate_user(email, current_password)
        
        if not success:
            return False, "Current password is incorrect"
        
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            self.users_collection.update_one(
                {"email": email},
                {"$set": {"password": hashed_password}}
            )
            return True, "Password updated successfully"
        except Exception as e:
            return False, f"Error updating password: {str(e)}"
