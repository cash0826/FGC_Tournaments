import pytest
from flask import Flask

from extensions import db
from models import Team, TeamMember, User
from services import TeamMemberService, TeamService
from utils.errors import ConflictError, NotFoundError, ValidationError


@pytest.fixture
def app():
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


def create_user(email):
    user = User(email=email)
    user.password_hash = "correct horse battery staple"
    db.session.add(user)
    db.session.commit()
    return user


def test_team_membership_services_access_and_update_database(app):
    user = create_user("team-service@example.com")
    team = Team(name="Arcade Squad")
    db.session.add(team)
    db.session.commit()

    membership = TeamMemberService.add_team_member(
        team.id,
        {"user_id": user.id, "role_on_team": "captain"},
    )

    assert membership.team_id == team.id
    assert membership.user_id == user.id
    assert membership.to_dict()["role_on_team"] == "captain"
    assert TeamMemberService.get_teams_for_user(user.id) == ["Arcade Squad"]
    with pytest.raises(ConflictError):
        TeamMemberService.add_team_member(team.id, {"user_id": user.id})

    TeamMemberService.remove_team_member(team.id, user.id)
    assert TeamMember.query.filter_by(team_id=team.id, user_id=user.id).first() is None
    assert TeamMemberService.get_teams_for_user(user.id) == []
    with pytest.raises(NotFoundError):
        TeamMemberService.remove_team_member(team.id, user.id)


def test_team_services_validate_references_and_delete_by_team_name(app):
    with pytest.raises(ValidationError):
        TeamMemberService.add_team_member(0, {"user_id": 1})
    with pytest.raises(ValidationError):
        TeamMemberService.add_team_member(1, {})
    with pytest.raises(NotFoundError):
        TeamMemberService.add_team_member(1, {"user_id": 1})

    team = Team(name="Delete Squad")
    db.session.add(team)
    db.session.commit()

    TeamService.delete("Delete Squad")
    assert Team.query.filter_by(name="Delete Squad").first() is None
    with pytest.raises(NotFoundError):
        TeamService.delete("Delete Squad")
