from config import Config
from flask import Flask
from extensions import db, migrate, jwt, bcrypt, api
from models import User, Role, UserRole
from controllers import Signup, Login, Me, UserRoles
from dotenv import load_dotenv

load_dotenv()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  
  # initialize extensions
  db.init_app(app)
  migrate.init_app(app, db)
  jwt.init_app(app)
  bcrypt.init_app(app)
  api.init_app(app)
  
  # import resources
  api.add_resource(Signup, "/api/signup")
  api.add_resource(Login, "/api/login")
  api.add_resource(Me, "/api/me")
  
  api.add_resource(UserRoles, "/api/users/<int:user_id>")
  
  return app
  
app = create_app()
  
if __name__ == "__main__":
  app = create_app()
  app.run(debug=True, port=5555)
