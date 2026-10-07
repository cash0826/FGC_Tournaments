from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import UserRoleService, UserService
from utils.errors import AppError
from utils.require import require_admin

# Just POST/DELETE
# /users/<user_id>/roles

class UserRoles(Resource):
  @jwt_required()
  @require_admin
  def post(self, user_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400

    try:
      UserRoleService.assign_role(user_id, data.get("role"))
      updated_roles = UserService.get_roles_for_user(user_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return {"user_id": user_id, "roles": updated_roles}, 201

  @jwt_required()
  @require_admin
  def delete(self, user_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400

    try:
      UserRoleService.remove_role(user_id, data.get("role"))
    except AppError as error:
      return {"error": str(error)}, error.status_code

    return {"message": "Role removed from user successfully"}, 200