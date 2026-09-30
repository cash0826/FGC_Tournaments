from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import EventService
from utils.errors import AppError
from utils.require import require_admin_or_owner

# /events
class EventController(Resource):
  def get(self):
    try:
      events = EventService.get_all()
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return [event.to_dict() for event in events]
  
  @jwt_required()
  @require_admin_or_host
  def post(self):
    data = request.get_json()
    user_id = get_jwt_identity()
    
    try:
      new_event = EventService.create_event(user_id, data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return new_event.to_dict()
  
# /events/<event_id>
class EventInstanceController(Resource):
  def get(self, event_id):
    try:
      event = EventService.get_by_id(event_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return event.to_dict()
  
  @jwt_required()
  @require_admin_or_host
  def update(self, event_id):
    data = request.get_json()
    event = EventService.get_by_id(event_id)
    if event.host_id != user_id:
      return {"error": "Permission denied"}, 403
  
    try:
      updated_event = EventService.update_event(event_id, data)
      
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return updated_event.to_dict()
  
  @jwt_required()
  @require_admin_or_host
  def delete(self, event_id):
    event = EventService.get_by_id(event_id)
    if event.host_id != user_id:
      return {"error": "Permission denied"}, 403
    
    try:
      delete = EventService.delete(event_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "Event deleted successfully"}, 200