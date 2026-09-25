from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services import UserRoleService, UserService
from utils.require import require_admin

# Just POST/DELETE
# /users/<user_id>/roles

class UserRoles(Resource):
  
  @jwt_required()
  @require_admin
  def post(self, user_id):   
    data = request.get_json()
    
    try: 
      instance = UserRoleService.assign_role(user_id, data.get("role"))
    except ValueError as error:
      return {"error": str(error)}, 400
    
    updated_roles = UserService.get_roles_for_user(user_id)
    return {"user_id": user_id, "roles": updated_roles}, 204

class UserRoles(Resource):
  
  @jwt_required()
  @require_admin
  def delete(self, user_id):
    
    try: 
      remove_role = UserRoleService.remove_role(user_id, data.get("role"))
    except ValueError as error:
      return {"error": str(error)}, 400
    if remove_role == "Failed to delete":
      return {"error": remove_role}, 400
    
    return {"msg": "Delete Successful"}, 204