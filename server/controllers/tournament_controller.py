from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import TournamentService, TournamentCompetitorService
from utils.errors import AppError
from utils.require import require_admin_or_host, require_event_ownership_or_admin

# /events/<event_id>/tournaments
class TournamentController(Resource):
  def get(self, event_id):
    try:
      tournaments = TournamentService.get_all(filters={"event_id": event_id})
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return [tournament.to_dict() for tournament in tournaments], 200
    
  @jwt_required()
  @require_admin_or_host
  def post(self, event_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      require_event_ownership_or_admin(event_id)
      new_tournament = TournamentService.create_tournament(event_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return new_tournament.to_dict(), 201
    
# /events/<event_id>/tournaments/<tournament_id>
class TournamentInstanceController(Resource):
  def get(self, event_id, tournament_id):
    try:
      tournament = TournamentService._get_tournament(event_id, tournament_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return tournament.to_dict(), 200
  
  @jwt_required()
  @require_admin_or_host
  def patch(self, event_id, tournament_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      require_event_ownership_or_admin(event_id)
      updated_tournament = TournamentService.update_tournament(event_id, tournament_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return updated_tournament.to_dict(), 200
  
  @jwt_required()
  @require_admin_or_host
  def delete(self, event_id, tournament_id):
    try:
      require_event_ownership_or_admin(event_id)
      delete = TournamentService.delete(event_id, tournament_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "Tournament deleted successfully"}, 200