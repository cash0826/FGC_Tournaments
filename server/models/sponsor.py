from extensions import db
from sqlalchemy.orm import validates

class Sponsor(db.Model):
  __tablename__ = "sponsors"
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False, index=True)
  logo_url = db.Column(db.Text)
  website = db.Column(db.Text)
  contact_email = db.Column(db.String(120))
  
  # sponsors back sponsored_events (has many)
  # Opted to keep children if parent is deleted (no cascade)
  sponsored_events = db.relationship("EventSponsor", back_populates="sponsor")
  
  @validates("name", "logo_url", "website")
  def validates_text(self, key, value):
    if not isinstance(value, str):
      raise ValueError(f"{key} must be a string")
    return value.lower().strip()
  
  @validates("contact_email")
  def validates_email(self, key, address):
    if not isinstance(address, str):
      raise ValueError("Email must be a string")
    address = address.lower().strip()
    if not address:
      raise ValueError("Email cannot be empty")
    if '@' not in address:
      raise ValueError('Email must be a valid format with @ in the address')
    return address
  
  def to_dict(self):
    return {
      "name": self.name,
      "logo_url": self.logo_url,
      "website": self.website,
      "contact_email": self.contact_email
    }
  
  