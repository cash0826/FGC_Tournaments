from extensions import db
from sqlalchemy.orm import validates

class Game(db.Model):
  __tablename__ = "games"
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False, index=True)
  slug = db.Column(db.String(10), unique=True, nullable=False, index=True)
  publisher = db.Column(db.String(50), nullable=True)
  genre = db.Column(db.String(50), nullable=True)
  picture = db.Column(db.String(500), nullable=True)
  
  # a game is featured in a tournament
  tournaments = db.relationship(
    "Tournament", back_populates="game", cascade='all, delete-orphan'
  )
  
  @validates("name", "slug", "publisher", "genre", "picture")
  def validate_string(self, key, value):
    if not isinstance(value, str):
      raise ValueError(f"{key} must be a string")
    return value
  
  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "slug": self.slug,
      "publisher": self.publisher,
      "genre": self.genre
    }