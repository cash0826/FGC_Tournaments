from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import TeamService, TeamMemberService
from utils.errors import AppError
from utils.require import _current_user_id

# /teams
class TeamController(Resource):
  @jwt_required()
  def post(self):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      new_team = TeamService.create(data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return new_team.to_dict(), 201
  
  @jwt_required()
  def delete(self):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400

    try:
      TeamService.delete(data.get("team"))
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return {"message": "Team deleted successfully"}, 200
  
# /teams/<team_id>
class TeamMemberController(Resource):
  @jwt_required()
  def post(self, team_id):
    data = request.get_json(silent=True)   # user_id, role_on_team
    
    try:
      new_team_member = TeamMemberService.add_team_member(team_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return new_team_member.to_dict(), 200
  
  @jwt_required()
  def delete(self, team_id):
    data = request.get_json(silent=True)   # user_id
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      TeamMemberService.remove_team_member(team_id, data.get("user_id"))
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "User removed from team successfully"}, 200
  
# /me/teams
class MyTeamsController(Resource):
  @jwt_required()
  def get(self):
    try:
      teams = TeamMemberService.get_teams_for_user(int(_current_user_id()))
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"teams": teams}, 200