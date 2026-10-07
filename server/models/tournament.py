from extensions import db
from sqlalchemy.orm import validates
from enum import Enum

class GamingPlatform(Enum):
  PS4 = "PS4"
  PS4_PRO = "PS4_PRO"
  PS5 = "PS5"
  MISTER_FPGA = "MiSTeR FPGA"
  OTHER = "OTHER"
  
class LineUpTypes(Enum):
  SINGLES = "SINGLES"
  TEAM = "TEAM"
  OTHER = "OTHER"

class Tournament(db.Model):
  __tablename__ = "tournaments"
  
  id = db.Column(db.Integer, primary_key=True)
  event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
  game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
  name = db.Column(db.String(50), nullable=False)
  start = db.Column(db.DateTime, nullable=False)
  registration_deadline = db.Column(db.DateTime, nullable=False)
  gaming_platform = db.Column(db.Enum(GamingPlatform))
  line_up_type = db.Column(db.Enum(LineUpTypes))
  
  # --------------
  # Relationships
  # --------------
  
  # tournament belongs (contains) to a single event
  event = db.relationship(
    "Event", back_populates="tournaments", foreign_keys=[event_id]
  )
  
  # tournament belongs (features) a single game
  game = db.relationship(
    "Game", back_populates="tournaments", foreign_keys=[game_id]
  )
  
  # tournament structures a bracket
  bracket = db.relationship(
    "Bracket", uselist=False, back_populates="tournament", cascade="all, delete-orphan"
    )
  
  # tournament schedules many matches
  matches = db.relationship(
    "Match", back_populates="tournament", cascade="all, delete-orphan"
  )
  
  # TODO: tournament ranks the standings
  # TODO: tournament is backed by sponsors
  
  # TODO: tournament registers a tournament_competitor / has (many) competitors
  competitors = db.relationship(
    "TournamentCompetitor", back_populates="tournament", cascade="all, delete-orphan"
  )
  
  # --------------
  # Validations
  # --------------
  @validates("event_id", "game_id")
  def validate_id(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
    
  @validates("gaming_platform", "line_up_type")
  def validate_enum(self, key, value):
    if not isinstance(value, str):
      raise ValueError(f"{key} must but a string")
    return value.upper().strip()
  
  def to_dict(self):
    return {
      "id": self.id,
      "event_id": self.event_id,
      "game_id": self.game_id,
      "name": self.name,
      "start": self.start.isoformat(),
      "registration_deadline": self.registration_deadline.isoformat(),
      "gaming_platform": self.gaming_platform.value,
      "line_up_type": self.line_up_type.value
    }