from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required 
from services import AuthService, UserService, UserRoleService

def _issue_session(user, status_code):
  # create_access_token returns an encoded access token
  access_token = create_access_token(identity=str(user.id))   # expires_delta uses Config value: JWT_ACCESS_TOKEN_EXPIRES
  return {
    "token": access_token,
    "user": user.to_dict()
  }, status_code

class Signup(Resource):
  def post(self):
    data = request.get_json() or {}
    
    try:
      new_user = AuthService.create_new_user(data)
      viewer_role = UserRoleService.assign_role(new_user.id, "viewer")
    except Exception as error:
      return {"error": str(error)}, 400
    return _issue_session(new_user, 201)
    
class Login(Resource):
  def post(self):
    data = request.get_json() or {}
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
      return { "error": "Email and Password are required"}, 400
    
    try: 
      user = UserService.authenticate_user(email, password)
    except ValueError as error:
      return {"error": str(error)}, 401
    
    return _issue_session(user, 200)
  
class Me(Resource):
  @jwt_required()
  def get(self):
    user_id = int(get_jwt_identity())
    user = UserService.get_user_by_id(user_id)
    if not user:
      return {"error": "User not found."}, 404
    
    return {"user": user.to_dict()}, 200
  
  @jwt_required()
  def patch(self):
    user_id = int(get_jwt_identity())
    user = UserService.get_user_by_id(user_id)
    data = request.get_json() or {}
    
    try: 
      updated_user = UserService.update_profile(user_id, data)
    except NotFoundError as error:
      return {"error": str(error)}, 404
  
# No Logout Resource. Logout is controlled by the FE. Clear JWT token in the FE.
"""
An encoded JWT is made up of a header (Algorithm and Token Type), 
Payload (Data), 
and a Signature (Secret Key)
"""