"""Integration tests for the entities described in the project ERD.

These tests are intentionally written before the remaining ERD models exist.
They provide the executable contract for the model layer while the schema is
being implemented.
"""
import pytest
from datetime import datetime, timezone
from importlib import import_module

from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from extensions import db


ENTITY_SPECS = {
    "Role": ("models.role", "Role", "roles"),
    "User": ("models.user", "User", "users"),
    "UserRole": ("models.user_role", "UserRole", "user_roles"),
    "UserSocialAccount": (
        "models.user_social_account",
        "UserSocialAccount",
        "user_social_accounts",
    ),
    "Event": ("models.event", "Event", "events"),
    "Game": ("models.game", "Game", "games"),
    "Tournament": ("models.tournament", "Tournament", "tournaments"),
    "Bracket": ("models.bracket", "Bracket", "brackets"),
    "Team": ("models.team", "Team", "teams"),
    "TeamMember": ("models.team_member", "TeamMember", "team_members"),
    "TournamentCompetitor": (
        "models.tournament_competitor",
        "TournamentCompetitor",
        "tournament_competitors",
    ),
    "Match": ("models.match", "Match", "matches"),
    "Standing": ("models.standing", "Standing", "standings"),
    "Sponsor": ("models.sponsor", "Sponsor", "sponsors"),
    "TournamentSponsor": (
        "models.tournament_sponsor",
        "TournamentSponsor",
        "tournament_sponsors",
    ),
}


def model_class(entity_name):
    module_name, class_name, _ = ENTITY_SPECS[entity_name]
    module = import_module(module_name)
    return getattr(module, class_name)


def make_user(User, email):
    user = User(email=email)
    user.password_hash = "correct horse battery staple"
    return user


@pytest.fixture
def app():
    from flask import Flask

    application = Flask(__name__)
    application.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(application)
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def session(app):
    return db.session


@pytest.mark.parametrize("entity_name", list(ENTITY_SPECS))
def test_every_erd_entity_has_a_mapped_model(entity_name):
    model = model_class(entity_name)

    assert inspect(model).local_table.name == ENTITY_SPECS[entity_name][2]


def test_role_persists_and_serializes_all_public_fields(app, session):
    Role = model_class("Role")
    role = Role(name="Admin", description="Tournament administrator", is_system_role=True)
    session.add(role)
    session.commit()

    loaded = session.get(Role, role.id)
    assert loaded.to_dict() == {
        "id": role.id,
        "name": "admin",
        "description": "Tournament administrator",
        "is_system_role": True,
    }


def test_user_persists_and_to_dict_excludes_sensitive_fields(app, session):
    User = model_class("User")
    user = make_user(User, "Player@Example.com")
    user.gamer_name = "PlayerOne"
    user.first_name = "Jane"
    user.last_name = "Doe"
    user.contact_number = "+15551234567"
    session.add(user)
    session.commit()

    loaded = session.get(User, user.id)
    serialized = loaded.to_dict()
    assert serialized["email"] == "player@example.com"
    assert serialized["gamer_name"] == "playerone"
    assert "password_hash" not in serialized
    assert "_password_hash" not in serialized
    assert "contact_number" not in serialized


def test_user_role_relationships_persist_and_duplicate_assignment_is_rejected(app, session):
    User = model_class("User")
    Role = model_class("Role")
    UserRole = model_class("UserRole")
    user = make_user(User, "player@example.com")
    role = Role(name="player")
    session.add_all([user, role])
    session.flush()

    assignment = UserRole(user=user, role=role)
    session.add(assignment)
    session.commit()
    assert user.user_roles == [assignment]
    assert role.user_roles == [assignment]
    assert assignment.to_dict()["role"]["name"] == "player"

    session.add(UserRole(user=user, role=role))
    with pytest.raises(IntegrityError):
        session.commit()


def test_user_social_account_persists_through_user_relationship(app, session):
    User = model_class("User")
    SocialAccount = model_class("UserSocialAccount")
    user = make_user(User, "social@example.com")
    account = SocialAccount(platform="discord", handle="player#1234", user=user)
    session.add(user)
    session.commit()

    assert session.get(SocialAccount, account.id).user is user
    assert user.social_accounts[0].handle == "player#1234"
    assert user.social_accounts[0].to_dict()["platform"] == "discord"


def test_event_host_and_tournament_game_relationships_persist(app, session):
    User = model_class("User")
    Event = model_class("Event")
    Game = model_class("Game")
    Tournament = model_class("Tournament")
    host = make_user(User, "host@example.com")
    game = Game(name="Street Fighter 6", publisher="Capcom", genre="Fighting", slug="SF6")
    event = Event(
        name="Launch Event",
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        end=datetime(2028, 1, 2, tzinfo=timezone.utc),
        host=host,
    )
    tournament = Tournament(
        name="Singles", 
        event=event, 
        game=game, 
        line_up_type="singles", 
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        registration_deadline=datetime(2027, 12, 25, tzinfo=timezone.utc)
    )
    session.add(tournament)
    session.commit()

    assert tournament.event.host is host
    assert tournament.game.name == "Street Fighter 6"
    assert event.tournaments == [tournament]
    assert game.tournaments == [tournament]


def test_bracket_is_one_to_one_with_tournament_and_serializes_url(app, session):
    User = model_class("User")
    Event = model_class("Event")
    Game = model_class("Game")
    host = make_user(User, "host@example.com")
    game = Game(name="Street Fighter 6", publisher="Capcom", genre="Fighting", slug="SF6")
    event = Event(
        name="Launch Event",
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        end=datetime(2028, 1, 2, tzinfo=timezone.utc),
        host=host,
    )
    Tournament = model_class("Tournament")
    Bracket = model_class("Bracket")
    tournament = Tournament(
        name="Bracketed", 
        event=event,
        game=game,
        line_up_type="singles",
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        registration_deadline=datetime(2027, 12, 25, tzinfo=timezone.utc)
    )
    bracket = Bracket(tournament=tournament, url="https://example.test/bracket/1")
    session.add(bracket)
    session.commit()

    assert session.get(Bracket, bracket.id).tournament is tournament
    assert bracket.to_dict()["url"] == "https://example.test/bracket/1"
    session.add(Bracket(tournament_id=tournament.id, url="https://example.test/bracket/2"))
    with pytest.raises(IntegrityError):
        session.commit()


def test_team_membership_and_team_competitor_relationships_persist(app, session):
    User = model_class("User")
    Event = model_class("Event")
    Game = model_class("Game")
    Team = model_class("Team")
    TeamMember = model_class("TeamMember")
    Tournament = model_class("Tournament")
    Competitor = model_class("TournamentCompetitor")
    
    host = make_user(User, "host@example.com")
    user = make_user(User, "team@example.com")
    event = Event(
        name="Launch Event",
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        end=datetime(2028, 1, 2, tzinfo=timezone.utc),
        host=host,
    )
    game = Game(name="Street Fighter 6", publisher="Capcom", genre="Fighting", slug="SF6")
    team = Team(name="Arcade Squad")
    tournament = Tournament(
        name="Team Cup", 
        event=event,
        game=game, 
        line_up_type="team",
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        registration_deadline=datetime(2027, 12, 25, tzinfo=timezone.utc)
    )
    member = TeamMember(team=team, user=user, role_on_team="captain")
    competitor = Competitor(team=team, tournament=tournament, seed=1)
    session.add_all([member, competitor])
    session.commit()

    assert team.members[0].user is user
    assert tournament.competitors[0].team is team
    assert competitor.user is None


def test_solo_competitor_requires_user_and_team_competitor_requires_team(app, session):
    User = model_class("User")
    Event = model_class("Event")
    Game = model_class("Game")
    Tournament = model_class("Tournament")
    Competitor = model_class("TournamentCompetitor")
    
    host = make_user(User, "host@example.com")
    event = Event(
        name="Launch Event",
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        end=datetime(2028, 1, 2, tzinfo=timezone.utc),
        host=host,
    )
    game = Game(name="Street Fighter 6", publisher="Capcom", genre="Fighting", slug="SF6")
    singles = Tournament(
        name="Solo Cup",
        event=event,
        game=game, 
        line_up_type="singles",
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        registration_deadline=datetime(2027, 12, 25, tzinfo=timezone.utc)
    )
    team = Tournament(
        name="Team Cup", 
        event=event,
        game=game, 
        line_up_type="team",
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        registration_deadline=datetime(2027, 12, 25, tzinfo=timezone.utc)
    )
    session.add_all([singles, team])
    session.flush()

    session.add(Competitor(tournament=singles))
    with pytest.raises((IntegrityError, ValueError)):
        session.commit()
    session.rollback()

    session.add(Competitor(tournament=team))
    with pytest.raises((IntegrityError, ValueError)):
        session.commit()


def test_match_references_competitors_and_rejects_winner_outside_the_match(app, session):
    Tournament = model_class("Tournament")
    Competitor = model_class("TournamentCompetitor")
    Match = model_class("Match")
    tournament = Tournament(
        name="Match Cup", 
        line_up_type="singles",
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        registration_deadline=datetime(2027, 12, 25, tzinfo=timezone.utc)
    )
    other_tournament = Tournament(
        name="Other Cup", 
        line_up_type="singles",
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        registration_deadline=datetime(2027, 12, 25, tzinfo=timezone.utc)
    )
    a = Competitor(tournament=tournament, user_id=1)
    b = Competitor(tournament=tournament, user_id=2)
    outsider = Competitor(tournament=other_tournament, user_id=3)
    session.add_all([tournament, other_tournament, a, b, outsider])
    session.flush()

    match = Match(
        tournament=tournament,
        round="final",
        competitor_a=a,
        competitor_b=b,
        winner=outsider,
        status="completed",
    )
    session.add(match)
    with pytest.raises((IntegrityError, ValueError)):
        session.commit()


def test_standing_serializes_competitor_rank_and_points(app, session):
    Tournament = model_class("Tournament")
    Competitor = model_class("TournamentCompetitor")
    Standing = model_class("Standing")
    tournament = Tournament(
        name="Ranked Cup", 
        line_up_type="singles",
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        registration_deadline=datetime(2027, 12, 25, tzinfo=timezone.utc)
    )
    competitor = Competitor(tournament=tournament, user_id=1)
    standing = Standing(tournament_competitor=competitor, points=3, rank=1)
    session.add(standing)
    session.commit()

    assert standing.to_dict()["points"] == 3
    assert standing.to_dict()["rank"] == 1


def test_sponsor_many_to_many_relationship_preserves_sponsorship_attributes(app, session):
    Tournament = model_class("Tournament")
    Sponsor = model_class("Sponsor")
    TournamentSponsor = model_class("TournamentSponsor")
    tournament = Tournament(
        name="Sponsored Cup", 
        line_up_type="singles", 
        start=datetime(2028, 1, 1, tzinfo=timezone.utc),
        registration_deadline=datetime(2027, 12, 25, tzinfo=timezone.utc)
    )
    sponsor = Sponsor(name="Arcade Co.", contact_email="contact@arcade.test")
    sponsorship = TournamentSponsor(
        tournament=tournament,
        sponsor=sponsor,
        sponsorship_tier="gold",
        amount=2500,
    )
    session.add(sponsorship)
    session.commit()

    assert tournament.sponsors[0].sponsor is sponsor
    assert sponsor.tournaments[0].tournament is tournament
    assert sponsorship.to_dict()["sponsorship_tier"] == "gold"
