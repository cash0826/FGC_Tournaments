from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import SponsorService
from utils.errors import AppError
from utils.require import require_admin_or_host

# /sponsors
class SponsorController(Resource):
  def get(self):
    try:
      sponsors = SponsorService.get_all()
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return [sponsor.to_dict() for sponsor in sponsors], 200
  
  @jwt_required()
  @require_admin_or_host
  def post(self):
    data = request.get_json()
    if not isinstance(data, dict):
      raise {"error": "Request body must be a JSON object."}
    
    try:
      new_sponsor = SponsorService.create(data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return new_sponsor.to_dict(), 201
  
  @jwt_required()
  @require_admin_or_host
  def patch(self):
    data = request.get_json()
    if not isinstance(data, dict):
      raise {"error": "Request body must be a JSON object."}
    
    try:
      updated_sponsor = SponsorService.update(data, data.get("sponsor_id"))
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return updated_sponsor.to_dict(), 200
  
  @jwt_required()
  @require_admin_or_host
  def delete(self):
    data = request.get_json()
    if not isinstance(data, dict):
      raise {"error": "Request body must be a JSON object."}
    
    try:
      SponsorService.delete(data.get("sponsor_id"))
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "Sponsor deleted successfully"}, 200