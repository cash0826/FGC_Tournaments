from flask_restful import Resource
from utils.require_admin import require_admin

# Just POST/DELETE

class AddUserRoles(Resource):
  @require_admin
  def post(self):
    pass

class DeleteUserRoles(Resource): 
  @require_admin
  def delete(self):
    pass