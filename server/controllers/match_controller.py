from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import MatchService 
from utils.errors import AppError
from utils.require import require_admin_or_host, require_event_ownership_or_admin

# /events/<event_id>/tournaments/<tournament_id>/matches
class MatchController(Resource):
  def get(self, event_id, tournament_id):
    try:
      matches = MatchService.get_all(event_id, tournament_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return [match.to_dict() for match in matches], 200
  
  @jwt_required()
  @require_admin_or_host
  def post(self, event_id, tournament_id):
    data = request.get_json()
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object"}, 400
    
    try:
      require_event_ownership_or_admin(event_id)
      new_match = MatchService.create(event_id, tournament_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return new_match.to_dict(), 201
  
  @jwt_required()
  @require_admin_or_host
  def patch(self, event_id, tournament_id, match_id):
    data = request.get_json()
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object"}, 400
    
    try:
      require_event_ownership_or_admin(event_id)
      updated_match = MatchService.update(event_id, tournament_id, match_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return updated_match.to_dict(), 200
  
  @jwt_required()
  @require_admin_or_host
  def delete(self, event_id, tournament_id, match_id):
    try:
      require_event_ownership_or_admin(event_id)
      MatchService.delete(event_id, tournament_id, match_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return {"message": "Match deleted from tournament successfully"}, 200