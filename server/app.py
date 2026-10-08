from config import Config
from flask import Flask
from extensions import db, migrate, jwt, bcrypt, api
from controllers import (
  Signup, Login, Me, PasswordUpdate, UserRoles, UserController, UserSocialAccount,
  EventController, EventInstanceController, GameController, GameInstanceController,
  TournamentController, TournamentInstanceController,
  CompetitorController, CompetitorStandingController
  BracketController, BracketInstanceController,
  TeamController, TeamMemberController, MyTeamsController,
  MatchController
)
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
  
  # ---- Auth / Profile ----
  api.add_resource(Signup, "/api/signup")   # POST
  api.add_resource(Login, "/api/login")   # POST
  api.add_resource(Me, "/api/me")   # GET / PATCH / DELETE
  api.add_resource(PasswordUpdate, "/api/me/password")    # PATCH
  api.add_resource(UserSocialAccount, "/api/me/social_accounts")    # GET / POST / DELETE
  
  # ---- User Management for Admins ----
  api.add_resource(UserController, "/api/users/<int:user_id>")   # DELETE user (admin resource)
  api.add_resource(UserRoles, "/api/users/<int:user_id>/roles")   # POST / DELETE roles (admin resource)
  
  # ---- Events ----
  api.add_resource(EventController, "/api/events")    # GET (ALL) / POST
  api.add_resource(EventInstanceController, "/api/events/<int:event_id>")   # GET / PATCH / DELETE
  
  # ---- Games ----
  api.add_resource(GameController, "/api/games")    # GET (ALL) / POST
  api.add_resource(GameInstanceController, "/api/games/<int:game_id>")    # GET / PATCH / DELETE
  
  # ---- Tournaments ----
  api.add_resource(TournamentController, "/api/events/<int:event_id>/tournaments")    # GET / POST
  api.add_resource(TournamentInstanceController, "/api/events/<int:event_id>/tournaments/<int:tournament_id>")    # GET / PATCH / DELETE
  
  # ---- Competitor ---- [can refer to team or user]
  api.add_resource(CompetitorController, "/api/events/<int:event_id>/tournaments/<int:tournament_id>/competitors")    # POST / DELETE
  
  # ---- Bracket ----
  api.add_resource(BracketController,"/api/events/<int:event_id>/tournaments/<int:tournament_id>/bracket")    # GET / POST
  api.add_resource(BracketInstanceController, "/api/events/<int:event_id>/tournaments/<int:tournament_id>/bracket/<int:bracket_id>")    # GET / PATCH / DELETE
  
  # ---- Teams ----
  api.add_resource(TeamController, "/api/teams")    # POST / DELETE
  api.add_resource(TeamMemberController, "/api/teams/<int:team_id>")    # POST / DELETE (members) 
  api.add_resource(MyTeamsController, "/api/me/teams")    # GET
  
  # ---- Matches ----
  api.add_resource(MatchController, "/api/events/<int:event_id>/tournaments/<int:tournament_id>/matches")   # Full CRUD
  
  return app
  
app = create_app()
  
if __name__ == "__main__":
  app = create_app()
  app.run(debug=True, port=5555)
