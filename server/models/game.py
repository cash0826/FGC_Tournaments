from extensions import db
from sqlalchemy.orm import validates

class Game(db.Model):
  __tablename__ = "games"
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False, index=True)
  publisher = db.Column(db.String(50), nullable=True)
  genre = db.Column(db.String(50), nullable=True)
  
  # TODO: Game is featured in a tournament
  
  @validates("name", "publisher", "genre")
  def validate_string(self, key, value):
    if not isinstance(value, str):
      raise ValueError(f"{key} must be a string")
    return value
  
  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "publisher": self.publisher,
      "genre": self.genre
    }