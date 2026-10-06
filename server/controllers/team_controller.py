from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import TeamService
from utils.errors import AppError

# /teams
class TeamController(Resource):
  def get(self):
    try:
      teams = TeamService.get_all()
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return [team.to_dict() for team in teams]

  @jwt_required()
  def post(self):
    data = request.get_json()
    
    try:
      new_team = TeamService.create(data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return new_team.to_dict()
  
  @jwt_required()
  def delete(self):
    data = request.get_json()

    try:
      delete = TeamService.delete(data.get("team"))
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return {"message": "Team deleted successfully"}, 200