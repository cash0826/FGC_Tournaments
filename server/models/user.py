# import uuid (?)
import re
from datetime import datetime, timezone
from extensions import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

class User(db.Model):
  __tablename__ = "users"
  
  # For authentication
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False, index=True)
  _password_hash = db.Column(db.String(255), nullable=False)
  
  # Profile Information
  gamer_name = db.Column(db.String(50), unique=True, nullable=True, index=True)
  first_name = db.Column(db.String(50), nullable=True)
  last_name = db.Column(db.String(50), nullable=True)
  bio = db.Column(db.Text, nullable=True)
  profile_pic_url = db.Column(db.String(500), nullable=True)
  contact_number = db.Column(db.String(50), nullable=True)
  
  # Timestamps
  created_at = db.Column(db.DateTime, default=db.func.now())
  password_updated_at = db.Column(db.DateTime, default=db.func.now())
  
  # --------------
  # Relationships
  # --------------
  
  # User has user_roles
  user_roles = db.relationship(
    "UserRole", back_populates="user", cascade="all, delete-orphan"
  )
  
  # User links user_social_accounts
  social_accounts = db.relationship(
    "UserSocialAccount", back_populates="user", cascade="all, delete-orphan"
  )
  
  # User hosts events
  hosted_events = db.relationship(
    "Event", back_populates="host", cascade="all, delete-orphan"
  )
  
  # TODO: User plays as team member
  
  # TODO: User enters(solo) tournament competitor
  
  # --------------
  # Validations
  # --------------

  @validates("email")
  def validate_email(self, key, address):
    if not isinstance (address, str):
      raise ValueError("Email must be a string")
    address = address.lower().strip()
    if not address:
      raise ValueError("Email cannot be empty")
    if '@' not in address:
      raise ValueError('Email must have @ in the address')
    return address
  
  @validates("gamer_name", "first_name", "last_name", "bio")
  def validate_text(self, key, value):
    if not isinstance(value, str):
      raise ValueError(f"{key} must be a string")
    return value.lower().strip()
  
  @validates("contact_number")
  def validate_contact_number(self, key, number):
    if isinstance(number, int):
      phone_number = str(number)
    elif not isinstance(number, str):
      raise ValueError("Phone number must be in a string format")
    else:
      phone_number = number.strip()
    pattern = r"^\+?\d{7,15}$"
    if not re.fullmatch(pattern, phone_number):
      raise ValueError("Phone number must be 7–15 digits with no spaces or hyphens. Optional: leading +.")
    return phone_number
    
  # --------------
  # PW Methods
  # --------------
  
  @hybrid_property
  def password_hash(self):
    raise AttributeError("Password hashes may not be viewed")
  
  @password_hash.setter
  def password_hash(self, password):
    if not isinstance(password, str) or len(password.strip()) < 8:
      raise ValueError("Password must be a string of at least 8 characters.")
    password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
    self._password_hash = password_hash.decode("utf-8")
    self.password_updated_at = datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)
  
  def verify_password(self, password):
    return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))
    
  def to_dict(self):
    return {
      "id": self.id,
      "email": self.email,
      "first_name": self.first_name,
      "last_name": self.last_name,
      "gamer_name": self.gamer_name,
      "created_at": self.created_at.isoformat()
    }