from flask_restful import Resource
from flask_jwt_extended import jwt_required
from utils.require import require_admin

# Just POST/DELETE

class AddUserRoles(Resource):
  
  @jwt_required
  @require_admin
  def post(self):
    pass

class DeleteUserRoles(Resource):
  
  @jwt_required
  @require_admin
  def delete(self):
    pass