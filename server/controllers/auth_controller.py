from flask_restful import Resource
from flask_jwt_extended import create_access_token
from services.auth_service import authenticate_user

def _issue_session(user, status_code):
  # create_access_token returns an encoded access token
  access_token = create_access_token(identity=user.id)   # expires_delta uses Config value: JWT_ACCESS_TOKEN_EXPIRES
  return {
    "token": access_token,
    "user": user.to_dict()
  }, status_code

class Signup(Resource):
  def post(self):
    pass
  
class Login(Resource):
  def post(self):
    data = request.get_json() or {}
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
      return { "error": "Email and Password are required"}, 400
    
    try: 
      user = authenticate_user(email, password)
    except ValueError as error:
      return {"error": str(error)}, 401
    
    return _issue_session(user, 200)
  
class Me(Resource):
  def get(self):
    pass
  
# No Logout Resource. Logout is controlled by the FE. Clear JWT token in the FE.
"""
An encoded JWT is made up of a header (Algorithm and Token Type), 
Payload (Data), 
and a Signature (Secret Key)
"""