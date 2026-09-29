from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required 
from services import AuthService, UserService, UserRoleService
from utils.errors import AppError

def _issue_session(user, success_code):
  # create_access_token returns an encoded access token
  access_token = create_access_token(identity=str(user.id))   # expires_delta uses Config value: JWT_ACCESS_TOKEN_EXPIRES
  return {
    "token": access_token,
    "user": user.to_dict()
  }, success_code

# /signup
class Signup(Resource):
  def post(self):
    data = request.get_json(silent=True)
    
    try:
      new_user = AuthService.create_new_user(data)
      UserRoleService.assign_role(new_user.id, "viewer")
    except AppError as error:
      return {"error": error.message}, error.status_code
    return _issue_session(new_user, 201)

# /login   
class Login(Resource):
  def post(self):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
      return {"error": "Request body must be a JSON object."}, 400
    
    try: 
      user = AuthService.authenticate_user(data.get("email"), data.get("password"))
    except AppError as error:
      return {"error": error.message}, error.status_code
    
    return _issue_session(user, 200)
  
# /me
class Me(Resource):
  @jwt_required()
  def get(self):
    user_id = int(get_jwt_identity())
    try:
      user = UserService.get_user_by_id(user_id)
    except AppError as error:
      return {"error": error.message}, error.status_code
    
    return {"user": user.to_dict()}, 200
  
  @jwt_required()
  def patch(self):
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)
    
    try:
      updated_user = UserService.update_profile(user_id, data)
    except AppError as error:
      return {"error": error.message}, error.status_code
    
    return {"user": updated_user.to_dict()}, 200
  
  @jwt_required()
  def delete(self):
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)
    
    try: 
      user = UserService.get_user_by_id(user_id)
      AuthService.delete_profile(user, current_password=data.get("current_password"))
    except AppError as error:
      return {"error": error.message}, error.status_code
    
    return {"message": "Delete Successful"}, 200

# /me/password
class PasswordUpdate(Resource):
  @jwt_required()
  def patch(self):
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)
    
    try: 
      user = UserService.get_user_by_id(user_id)
      AuthService.change_password(user, current_password=data.get("current_password"), new_password=data.get("new_password"))
    except AppError as error:
      return {"error": error.message}, error.status_code
    
    return {"message": "Password updated successfully"}, 200
  

# No Logout Resource. Logout is controlled by the FE. Clear JWT token in the FE.
"""
An encoded JWT is made up of a header (Algorithm and Token Type), 
Payload (Data), 
and a Signature (Secret Key)
"""