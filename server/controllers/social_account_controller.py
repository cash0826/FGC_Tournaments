from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import SocialAccountService
from utils.errors import AppError
from utils.require import _current_user_id

# /me/social_accounts

class UserSocialAccount(Resource):
  @jwt_required()
  def get(self):
    try:
      social_accounts = SocialAccountService.get_all(filters={"user_id": int(_current_user_id())})
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return [social_account.to_dict() for social_account in social_accounts]
  
  @jwt_required()
  def post(self):
    data = request.get_json()
    
    try:
      new_social = SocialAccountService.create_linked_account(user_id=int(_current_user_id()), data=data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return new_social.to_dict()
  
  @jwt_required()
  def delete(self):
    data = request.get_json()
    platform = data.get("platform")
    
    try:
      SocialAccountService.unlink_social(user_id=int(_current_user_id()), platform=platform)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "Account unlinked successfully"}, 200