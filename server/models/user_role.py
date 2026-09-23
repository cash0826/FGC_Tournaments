from extensions import db
from sqlalchemy.orm import validates

# __tableargs__ : Attaching the same role to the same user twice does not create a duplicate row

class UserRole(db.Model):
  __tablename__ = "user_roles"
  __table_args__ = (
    db.UniqueConstraint("user_id", "role_id", name="uq_user_roles_user_role"),
  )
  
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
  added_at = db.Column(db.DateTime, default=db.func.now())
  
  # user_role belongs to a single User
  user = db.relationship("User", back_populates="user_roles")
  
  # user_role belongs to a single Role
  role = db.relationship("Role", back_populates="user_roles")
  
  # --------------
  # Validations
  # --------------
  @validates("user_id", "role_id")
  def validates_ids(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
  def to_dict(self):
    return {
      "user_id": self.user.id,
      "role": self.role.to_dict(),
      "added_at": self.added_at.isoformat()
    }