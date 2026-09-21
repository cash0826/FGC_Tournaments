from extensions import db

class UserRole(db.Model):
  __tablename__ = "user_roles"
  __tableargs__ = (db.UniqueConstraint("user_id, role_id", name="uq_user_roles_user_role"),)
  
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
  added_at = db.Column(db.DateTime, default=db.func.now())
  
  user = db.relationship("User", back_populates="user_roles")
  role = db.relationship("Role", back_populates="user_roles")
  
  def to_dict(self):
    return {
      "user_id": self.user.user_id,
      "role": self.role.to_dict(),
      "added_at": self.added_at.isoformat()
    }