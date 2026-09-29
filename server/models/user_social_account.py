from extensions import db
from sqlalchemy.orm import validates
from enum import Enum

class Platform(Enum):
  X = "x"
  DISCORD = "discord"
  TWITCH_TV = "twitch_tv"
  XBOX = "xbox"
  STEAM = "steam"
  EPIC_GAMES = "epic_games"
  BATTLENET = "battle.net"
  RIOT_GAMES = "riot_games"

class UserSocialAccount(db.Model):
  __tablename__ = "user_social_accounts"
  
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  platform = db.Column(db.Enum(Platform), nullable=False)
  handle = db.Column(db.String(50), nullable=False)
  
  # user_social_acct belongs to a single user
  user = db.relationship("User", back_populates="social_accounts")
  
  # Validations
  @validates("user_id")
  def validates_ids(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
  @validates("handle")
  def validate_text(self, key, value):
    if not isinstance(value, str):
      raise ValueError(f"{key} must be a string")
    return value.lower().strip()
  
  @validates("platform")
  def validate_text(self, key, value):
    if not isinstance(value, str):
      raise ValueError(f"{key} must be a string")
    return value.upper().strip()
  
  def to_dict(self):
    return {
      "id": self.id,
      "user_id": self.user_id,
      "platform": self.platform.value,
      "handle": self.handle
    }