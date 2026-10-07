from extensions import db
from sqlalchemy.orm import validates
from enum import Enum

class TeamRole(Enum):
  captain = "captain"
  member = "member"

class TeamMember(db.Model):
  __tablename__ = "team_members"
  __table_args__ = (
    db.UniqueConstraint("team_id", "user_id", name="uq_team_members_team_member"),
  )
  
  id = db.Column(db.Integer, primary_key=True)
  team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  role_on_team = db.Column(db.Enum(TeamRole), default=TeamRole.member, nullable=False)
  joined_at = db.Column(db.DateTime, default=db.func.now())
  
  # members belongs to a team
  team = db.relationship("Team", back_populates="members")
  
  # team_member traces back to a user
  user = db.relationship("User", back_populates="user_teams")
  
  @validates("team_id", "user_id")
  def validate_ids(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
  def to_dict(self):
    return {
      "team_id": self.team_id,
      "user_id": self.user_id,
      "role_on_team": self.role_on_team.value,
      "joined_at": self.joined_at.isoformat()
    }