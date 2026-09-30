from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import UserService
from utils.errors import AppError
from utils.require import require_admin

# For admin use: Delete user

class UserController(Resource):
  
  @jwt_required()
  @require_admin
  def delete(self, user_id):
    try:
      UserService.delete_user(user_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code

    return {"msg": "Delete Successful"}, 200
    