from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from services import TournamentService, EventService
from utils.errors import AppError
from utils.require import require_admin_or_host

# /events/<event_id>/tournaments
class TournamentController(Resource):
  def get(self, event_id):
    try:
      tournaments = TournamentService.get_all(filters={"event_id": event_id})
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return [tournament.to_dict() for tournament in tournaments]
    
  @jwt_required()
  @require_admin_or_host
  def post(self, event_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    
    try:
      event = EventService.get_by_id(event_id)
      if event.host_id != int(user_id):
        return {"error": "Permission denied"}, 403
      new_tournament = TournamentService.create_tournament(event_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return new_tournament.to_dict()  
    
# /events/<event_id>/tournaments/<tournament_id>
class TournamentInstanceController(Resource):
  def get(self, event_id, tournament_id):
    try:
      tournament = TournamentService.get_by_id(tournament_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return tournament.to_dict()
  
  @jwt_required()
  @require_admin_or_host
  def patch(self, event_id, tournament_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    
    try:
      event = EventService.get_by_id(event_id)
      if event.host_id != int(user_id):
        return {"error": "Permission denied"}, 403
      updated_tournament = TournamentService.update_tournament(tournament_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return updated_tournament.to_dict()
  
  @jwt_required()
  @require_admin_or_host
  def delete(self, event_id, tournament_id):
    user_id = get_jwt_identity()
    
    try:
      event = EventService.get_by_id(event_id)
      if event.host_id != int(user_id):
        return {"error": "Permission denied"}, 403
      delete = TournamentService.delete(tournament_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "Tournament deleted successfully"}, 200
