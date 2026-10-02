from random import choice as rc
from faker import Faker
from app import create_app
from extensions import db
from models import User, Role, UserRole, UserSocialAccount, Platform, Event, Game
import datetime as dt
fake = Faker()

app = create_app()

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
    description="Creates and manages their own events, including tournaments and user"
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
  
  print("Creating test admin account and two host accounts...")
  admin = User(email="admin@example.com", first_name="Admin")
  admin.password_hash = "adminpassword"
  
  host1 = User(email="host1@example.com", first_name="Host_1")
  host1.password_hash = "host1password"
  
  host2 = User(email="host2@example.com", first_name="Host_2")
  host2.password_hash = "host2password"
  
  db.session.add_all([admin, host1, host2])
  db.session.commit()
  
  print("Creating 20 test players...")
  players = []
  for i in range(20):
    first_name = fake.unique.first_name()
    email = first_name.lower() + "@example.com"
    random_int = fake.random_int(min=101, max=999)
    gamer_name = f"{first_name.lower()}{random_int}"
    password = first_name.lower() + 'pass123'
    player = User(
      email=email,
      gamer_name=gamer_name,
      first_name=first_name
    )
    player.password_hash = password
    players.append(player)
  db.session.add_all(players)
  db.session.commit()
  
  print("Assigning test admin, host and player roles...")
  admin_role_lookup = Role.query.filter_by(name="admin").first()
  admin_role = UserRole(user_id=admin.id, role_id=admin_role_lookup.id)   # Assigns admin role
  
  host_role_lookup = Role.query.filter_by(name="host").first()
  host1_role = UserRole(user_id=host1.id, role_id=host_role_lookup.id)
  host2_role = UserRole(user_id=host2.id, role_id=host_role_lookup.id)   # Assigns host role
  
  player_role_lookup = Role.query.filter_by(name="player").first()
  player_roles = []
  for player in players:
    player_role = UserRole(user_id=player.id, role_id=player_role_lookup.id)
    player_roles.append(player_role)
  
  db.session.add_all([admin_role, host1_role, host2_role])
  db.session.add_all(player_roles)
  db.session.commit()
  
  print("Assigning test social accounts to each user...")
  social_accounts = []
  for player in players:
    ran_platform = rc(["x", "discord", "twitch_tv", "xbox", "steam", "epic_games", "battle.net", "riot_games"])
    platform_enum = Platform(ran_platform)
    social_account = UserSocialAccount(user_id=player.id, platform=platform_enum.name, handle=player.gamer_name)
    social_accounts.append(social_account)
  db.session.add_all(social_accounts)
  db.session.commit()
  
  print("Creating 10 test events...")
  events = []
  for i in range(10):
    host = rc([host1, host2])
    name = f"Event{i+1}"
    start = fake.date_time_between_dates(datetime_start=dt.date(2026, 11, 7), datetime_end=dt.date(2026, 11, 28))
    end = start + dt.timedelta(days=1)
    in_person = rc([True, False])
    location = rc(["San Pedro", "Barreal, Heredia", "Coronado"])
    description = "Lorem ipsum dolor sit amet consectetur adipiscing elit."
    rules = "Consectetur adipiscing elit quisque faucibus ex sapien vitae."
    event = Event(
      host=host,
      name=name,
      start=start,
      end=end,
      in_person=in_person,
      location=location,
      description=description,
      rules=rules
    )
    events.append(event)
  db.session.add_all(events)
  db.session.commit()
  
  print("Creating games...")
  street_fighter_6 = Game(name="Street Fighter 6", slug="SF6")
  fatal_fury = Game(name="Fatal Fury: City of the Wolves", slug="FFCW")
  guilty_gear = Game(name="Guilty Gear Strive", slug="GGST")
  marvel_tokon = Game(name="Marvel Tōkon: Fighting Soul", slug="MTFS")
  king_of_fighters= Game(name="King of Fighters '98", slug="KOF")
  granblue_fantasy = Game(name="Granblue Fantasy Versus: Rising", slug="GBFV")
  
  db.session.add_all([
    street_fighter_6, fatal_fury, guilty_gear, marvel_tokon, king_of_fighters, granblue_fantasy
  ])
  db.session.commit()

  