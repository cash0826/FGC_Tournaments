from extensions import db
from sqlalchemy.orm import validates

class Role(db.Model):
  __tablename__ = "roles"
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), default='viewer', nullable=False)
  description = db.Column(db.Text, nullable=True)
  is_system_role = db.Column(db.Boolean, nullable=True, default=False)
  
  # Roles are assigned to user_roles
  user_roles = db.relationship(
    "UserRole", back_populates="role", cascade="all, delete-orphan"
  )
  
  # TODO: name and is_system_role validations
  @validates("name")
  def validate_name(self, key, value):
    if not isinstance(value, str):
      raise ValueError(f"Role must be a string")
    cleaned = value.strip().lower()
    return cleaned

  @validates("is_system_role")
  def validate_system_role(self, key, value):
    if not isinstance(value, bool):
      raise ValueError("is_system_role must be a boolean")
    return value
  
  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "description": self.description,
      "is_system_role": self.is_system_role
    }