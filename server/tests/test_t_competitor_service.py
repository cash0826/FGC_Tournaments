from datetime import datetime

import pytest
from flask import Flask

from extensions import db
from models import Event, Game, Team, Tournament, User
from services import TournamentCompetitorService
from utils.errors import ValidationError


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


@pytest.fixture
def competitor_context(app):
    host = User(email="competitor-host@example.com")
    host.password_hash = "correct horse battery staple"
    user = User(email="competitor-player@example.com")
    user.password_hash = "correct horse battery staple"
    game = Game(name="Test Game", slug="competitor-test-game")
    event = Event(
        host=host,
        name="Test Event",
        start=datetime(2035, 1, 1),
    )
    team = Team(name="Test Team")
    db.session.add_all([host, user, game, event, team])
    db.session.flush()
    tournament = Tournament(
        event=event,
        game=game,
        name="Test Tournament",
        start=datetime(2035, 2, 1),
        registration_deadline=datetime(2035, 1, 20),
    )
    db.session.add(tournament)
    db.session.commit()
    return tournament, team, user


@pytest.mark.parametrize("entry_type", ["team", "user"])
def test_add_competitor_accepts_exactly_one_entry(competitor_context, entry_type):
    tournament, team, user = competitor_context
    data = {"team_id": team.id} if entry_type == "team" else {"user_id": user.id}

    competitor = TournamentCompetitorService.add_competitor(
        tournament.event_id, tournament.id, data
    )

    assert competitor.tournament_id == tournament.id
    assert competitor.team_id == (team.id if entry_type == "team" else None)
    assert competitor.user_id == (user.id if entry_type == "user" else None)


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"team_id": None, "user_id": None},
        {"team_id": 1, "user_id": 2},
    ],
)
def test_add_competitor_rejects_zero_or_two_entries(competitor_context, data):
    tournament, _, _ = competitor_context

    with pytest.raises(ValidationError, match="Exactly one"):
        TournamentCompetitorService.add_competitor(
            tournament.event_id, tournament.id, data
        )


@pytest.mark.parametrize("data", [{"team_id": True}, {"user_id": 0}])
def test_add_competitor_rejects_invalid_entry_id(competitor_context, data):
    tournament, _, _ = competitor_context

    with pytest.raises(ValidationError, match="positive integer"):
        TournamentCompetitorService.add_competitor(
            tournament.event_id, tournament.id, data
        )
