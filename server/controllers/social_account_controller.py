from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from services import SocialAccountService
from utils.errors import AppError

# /me/social_accounts

class UserSocialAccount(Resource):
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()
    
    try:
      social_accounts = SocialAccountService.get_all(filters={"user_id": int(user_id)})
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return [social_account.to_dict() for social_account in social_accounts]
  
  @jwt_required()
  def post(self):
    data = request.get_json()
    user_id = get_jwt_identity()
    
    try:
      new_social = SocialAccountService.create_linked_account(user_id=int(user_id), data=data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return new_social.to_dict()
  
  @jwt_required()
  def delete(self):
    data = request.get_json()
    platform = data.get("platform")
    user_id = get_jwt_identity()
    
    try:
      SocialAccountService.unlink_social(user_id=int(user_id), platform=platform)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"message": "Account unlinked successfully"}, 200