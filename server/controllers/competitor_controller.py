from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import TournamentCompetitorService, StandingService
from utils.errors import AppError
from utils.require import require_admin_or_host

# /events/<event_id>/tournaments/<tournament_id>/competitors
class CompetitorController(Resource):
  def get(self, event_id, tournament_id):
    try:
      competitor_standings = StandingService.get_all(event_id, tournament_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return competitor_standings, 200
  
  @jwt_required()
  def post(self, event_id, tournament_id):
    data = request.get_json()
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      new_competitor = TournamentCompetitorService.add_competitor(event_id, tournament_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return new_competitor.to_dict(), 201
  
  @jwt_required()
  def delete(self, event_id, tournament_id):
    data = request.get_json()   # competitor to be deleted from tournament
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      TournamentCompetitorService.remove_competitor(event_id, tournament_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "Competitor removed from tournament successfully"}, 200

# /events/<event_id>/tournaments/<tournament_id>/competitors/<competitor_id>
class UpdateCompetitorStanding(Resource):
  
  @jwt_required()
  @require_admin_or_host
  def patch(self, event_id, tournament_id, competitor_id):
    data = request.get_json()
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      require_event_ownership_or_admin(event_id)
      updated_standing = StandingService.update(event_id, tournament_id, competitor_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return updated_standing.to_dict(), 200