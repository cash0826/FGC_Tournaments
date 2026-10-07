from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import BracketService
from utils.errors import AppError
from utils.require import require_admin_or_host, require_event_ownership_or_admin

# /events/<event_id>/tournaments/<tournament_id>/bracket
class BracketController(Resource):
  def get(self, event_id, tournament_id):
    try:
      bracket = BracketService.get_bracket(event_id, tournament_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return bracket.to_dict(), 200
  
  @jwt_required()
  @require_admin_or_host
  def post(self, event_id, tournament_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      require_event_ownership_or_admin(event_id)
      new_bracket = BracketService.create_bracket(event_id, tournament_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return new_bracket.to_dict(), 201

# /events/<event_id>/tournaments/<tournament_id>/bracket/<bracket_id>
class BracketInstanceController(Resource):
  def get(self, event_id, tournament_id, bracket_id):
    try:
      bracket = BracketService.get_bracket_by_id(event_id, tournament_id, bracket_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code

    return bracket.to_dict(), 200

  @jwt_required()
  @require_admin_or_host
  def patch(self, event_id, tournament_id, bracket_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      require_event_ownership_or_admin(event_id)
      updated_bracket = BracketService.update_bracket(
        event_id, tournament_id, bracket_id, data
      )
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return updated_bracket.to_dict(), 200
  
  @jwt_required()
  @require_admin_or_host
  def delete(self, event_id, tournament_id, bracket_id):
    try:
      require_event_ownership_or_admin(event_id)
      BracketService.delete_bracket(event_id, tournament_id, bracket_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "Bracket deleted successfully"}, 200
    