from models import TeamMember, TeamRole, User, Team
from .base_service import BaseService
from utils.errors import ConflictError, NotFoundError, ValidationError
from extensions import db

class TeamMemberService(BaseService):
  model = TeamMember
  
  @classmethod
  def get_teams_for_user(cls, user_id):
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id < 1:
      raise ValidationError("User id must be a positive integer.")

    teams = (
      db.session.query(Team.name)
      .join(TeamMember, TeamMember.team_id == Team.id)
      .filter(TeamMember.user_id == user_id)
      .all()
    )
    return [team[0] for team in teams]
  
  @classmethod
  def add_team_member(cls, team_id, data):
    if not isinstance(team_id, int) or isinstance(team_id, bool) or team_id < 1:
      raise ValidationError("Team id must be a positive integer.")
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object.")

    user_id = data.get("user_id")
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id < 1:
      raise ValidationError("User id must be a positive integer.")

    role = data.get("role_on_team", TeamRole.member.value)
    if isinstance(role, str):
      try:
        role = TeamRole(role.strip().lower())
      except ValueError as error:
        raise ValidationError("Role on team must be 'captain' or 'member'.") from error
    elif not isinstance(role, TeamRole):
      raise ValidationError("Role on team must be 'captain' or 'member'.")
    
    team = Team.query.filter_by(id=team_id).first()
    if not team:
      raise NotFoundError("Team not found.")
    user = User.query.filter_by(id=user_id).first()
    if not user:
      raise NotFoundError("User not found")
    existing = TeamMember.query.filter_by(user_id=user_id, team_id=team_id).first()
    if existing:
      raise ConflictError("User is already a member of this team")
    
    membership_data = dict(data)
    membership_data["team_id"] = team_id
    membership_data["role_on_team"] = role
    return super().create(membership_data)
  
  @classmethod
  def remove_team_member(cls, team_id, user_id):
    if not isinstance(team_id, int) or isinstance(team_id, bool) or team_id < 1:
      raise ValidationError("Team id must be a positive integer.")
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id < 1:
      raise ValidationError("User id must be a positive integer.")

    instance = TeamMember.query.filter_by(team_id=team_id, user_id=user_id).first()
    if not instance:
      raise NotFoundError("User is not a member of this team.")

    return super().delete(instance.id)