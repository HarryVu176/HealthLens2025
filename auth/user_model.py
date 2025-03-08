# auth/user_model.py
from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, email, name=None, preferred_language="en", 
                 user_id=None, created_at=None, updated_at=None):
        self.user_id = user_id if user_id else ObjectId()
        self.email = email
        self.name = name
        self.preferred_language = preferred_language
        self.medication_history = []
        self.health_records = []
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()
    
    def to_dict(self):
        return {
            "_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "preferred_language": self.preferred_language,
            "medication_history": self.medication_history,
            "health_records": self.health_records,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        user = cls(
            email=data.get("email"),
            name=data.get("name"),
            preferred_language=data.get("preferred_language"),
            user_id=data.get("_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
        user.medication_history = data.get("medication_history", [])
        user.health_records = data.get("health_records", [])
        return user
    
    def add_medication(self, medication_data):
        """Add medication to user's history"""
        medication_data["added_at"] = datetime.now()
        self.medication_history.append(medication_data)
        self.updated_at = datetime.now()
    
    def add_health_record(self, record_data):
        """Add health record to user's profile"""
        record_data["added_at"] = datetime.now()
        self.health_records.append(record_data)
        self.updated_at = datetime.now()
