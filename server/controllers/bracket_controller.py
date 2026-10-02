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
      bracket = BracketService.get_all(filters={"tournament_id": tournament_id})
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return bracket.to_dict()
  
  @jwt_required()
  @require_admin_or_host
  def post(self, event_id, tournament_id):
    data = request.get_json()
    
    try:
      require_event_ownership_or_admin(event_id)
      new_bracket = BracketService.create(data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return new_bracket.to_dict()
  
  @jwt_required()
  @require_admin_or_host
  def patch(self, event_id, tournament_id, bracket_id):
    data = request.get_json()
    
    try:
      require_event_ownership_or_admin(event_id)
      updated_bracket = BracketService.update(data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return updated_bracket.to_dict()
  
  @jwt_required()
  @require_admin_or_host
  def delete(self, event_id, tournament_id, bracket_id):
    try:
      require_admin_or_host(event_id)
      delete = BracketService.delete(bracket_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "Bracket deleted successfully"}, 200
    