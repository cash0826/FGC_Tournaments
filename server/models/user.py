# import uuid (?)
from datetime import datetime, timezone
from extensions import db

class User(db.Model):
  __tablename__ = "users"
  
  # For authentication
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False, index=True)
  _password_hash = db.Column(db.String(255), nullable=False)
  
  # Profile Information
  gamer_username = db.Column(db.String(50), unique=True, nullable=True, index=True)
  first_name = db.Column(db.String(50), nullable=True)
  last_name = db.Column(db.String(50), nullable=True)
  bio = db.Column(db.Text, nullable=True)
  profile_pic_url = db.Column(db.String(500), nullable=True)
  contact_number = db.Column(db.String(50), nullable=True)
  
  # Timestamps
  created_at = db.Column(db.DateTime, default=db.func.now())
  password_updated_at = db.Column(db.DateTime, default=db.func.now())
  
  # TODO: relationships
  
  # TODO: email, username and name validations
  
  def to_dict(self):
    return {
      "id": self.id,
      "email": self.email,
      "first_name": self.first_name,
      "last_name": self.last_name,
      "created_at": self.created_at.isoformat()
    }