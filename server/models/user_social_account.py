from extensions import db
from sqlalchemy.orm import validates

class UserSocialAccount(db.Model):
  __tablename__ = "user_social_accounts"
  
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  platform = db.Column(db.String(50), nullable=False)
  handle = db.Column(db.String(50), nullable=False)
  
  # user_social_acct belongs to a single user
  user = db.relationship("User", back_populates="social_accounts")
  
  # Validations
  @validates("user_id")
  def validates_ids(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
  @validates("platform", "handle")
  def validate_text(self, key, value):
    if not isinstance(value, str):
      raise ValueError(f"{key} must be a string")
    return value.lower().strip()
  
  def to_dict(self):
    return {
      "id": self.id,
      "user_id": self.user_id,
      "platform": self.platform,
      "handle": self.handle
    }