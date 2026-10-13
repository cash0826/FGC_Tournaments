from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import EventSponsorService, EventService
from utils.errors import AppError
from utils.require import require_admin_or_host, require_event_ownership_or_admin

# /events/<event_id>/sponsors
class EventSponsorController(Resource):
  def get(self, event_id):
    try:
      sponsors_for_event = EventService.get_event_sponsors(event_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"event_id": event_id, "sponsors": sponsors_for_event}, 201
  
  @jwt_required()
  @require_admin_or_host
  def post(self, event_id):
    data = request.get_json()   # sponsor, sponsorship_tier, amount
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400

    try:
      require_event_ownership_or_admin(event_id)
      EventSponsorService.assign_sponsor(event_id, data.get("sponsor"))
      sponsors_for_event = EventService.get_event_sponsors(event_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"event_id": event_id, "sponsors": sponsors_for_event}, 201
      
  @jwt_required()
  @require_admin_or_host
  def delete(self, event_id):
    data = request.get_json()   # sponsor
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      require_event_ownership_or_admin(event_id)
      EventSponsorService.remove_sponsor(event_id, data.get("sponsor"))
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "Sponsor removed from event successfully"}, 200
    
# get_json(silent=True)
# Returns None instead of raising an error if parsing fails