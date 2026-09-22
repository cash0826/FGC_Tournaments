from random import choice as rc
from faker import Faker
from app import create_app
from extensions import db
from models import User, Role, UserRole
import datetime as dt
fake = Faker()

with app.app_context():
  db.drop_all()
  db.create_all()
  
  print("Creating admin, host, player and viewer roles...")
  role_admin = Role(
    name="admin",
    description="Full CRUD operations of site users, events, tournaments, and sponsors.",
    is_system_role=True
  )
  role_host = Role(
    name="host",
    description="Creates and manages their own events, including tournaments and user
  )
  role_player = Role(
    name="player",
    description="Registered to play in a tournament and participate in an event"
  )
  role_viewer = Role(
    name="viewer",
    description="User with read-only permission"
  )
  
  db.session.add_all([role_admin, role_host, role_player, role_viewer])
  db.session.commit()
  
  print("Creating test adming account and two host accounts...")
  admin = User(email="admin@example.com", first_name="Admin")
  # TODO: admin.set_password
  host1 = User(email="host1@example.com", first_name="Host_1")
  # TODO: host1.set_password
  host2 = User(email="host2@example.com", first_name="Host_2")
  # TODO: host2.set_password
  
  db.session.add_all([admin, host1, host2])
  db.session.commit()
  
  print("Creating 20 test players...")
  players = []
  for i in range(20):
    first_name = fake.unique.first_name()
    email = first_name.lower() + "example.com"
    random_int = fake.random_int(min=101, max=999)
    gamer_username = f"{name.lower()}{random_int}"
    password = name.lower() + '123'
    player = User(
      email=email,
      gamer_username=gamer_username,
      first_name=first_name
    )
    # TODO: player.set_password
    players.append(player)
  db.session.add_all(players)
  db.session.commit()
  
  print("Assigning admin, host and player rolles...")
  admin_role_lookup = Role.query.filter_by(name="admin").first()
  admin_role = UserRole(user_id=admin.id, role_id=admin_role_lookup.id)   # Assigns admin role
  
  host_role_lookup = Role.query.filter_by(name="host").first()
  host1_role = UserRole(user_id=host1.id, role_id=host_role_lookup)
  host2_role = UserRole(user_id=host2.id, role_id=host_role_lookup)   # Assigns host role
  
  player_role_lookup = Role.query.filter_by(name="player").first()
  player_roles = []
  for player in players:
    player_role = UserRole(user_id=player.id, role_id=player_role_lookup.id)
    player_roles.append(player_role)
  
  db.session.add_all([admin_role, host1_role, host2_role])
  db.session.add_all(player_roles)
  db.session.commit()
  
  