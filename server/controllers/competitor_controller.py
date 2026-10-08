from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import TournamentCompetitorService, StandingService
from utils.errors import AppError

# /events/<event_id>/tournaments/<tournament_id>/competitors
class CompetitorController(Resource):
  def get(self, event_id, tournament_id):
    try:
      competitors_w_standings = StandingService.get_all(event_id, tournament_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return [competitor.to_dict() for competitor in competitors_w_standings]
  
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
  
class CompetitorStandingController(Resource):
  pass