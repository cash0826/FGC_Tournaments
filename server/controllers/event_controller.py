from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import EventService
from utils.errors import AppError
from utils.require import require_admin_or_host, _current_user_id, require_event_ownership_or_admin

# /events
class EventController(Resource):
  def get(self):
    try:
      events = EventService.get_all()
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return [event.to_dict() for event in events], 200
  
  @jwt_required()
  @require_admin_or_host
  def post(self):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      new_event = EventService.create_event(int(_current_user_id()), data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return new_event.to_dict(), 201
  
# /events/<event_id>
class EventInstanceController(Resource):
  def get(self, event_id):
    try:
      event = EventService.get_by_id(event_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return event.to_dict(), 200
  
  @jwt_required()
  @require_admin_or_host
  def patch(self, event_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try:
      require_event_ownership_or_admin(event_id)
      updated_event = EventService.update_event(event_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return updated_event.to_dict(), 200
  
  @jwt_required()
  @require_admin_or_host
  def delete(self, event_id):
    try:
      require_event_ownership_or_admin(event_id)
      delete = EventService.delete(event_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "Event deleted successfully"}, 200