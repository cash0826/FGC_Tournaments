import pytest
from datetime import datetime
from flask import Flask

from extensions import db
from models import Bracket, Event, Game, Tournament, User
from services import BracketService, TournamentService
from utils.errors import NotFoundError, ValidationError


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
def tournament_context(app):
    user = User(email="bracket-service@example.com")
    user.password_hash = "correct horse battery staple"
    game = Game(name="Test Game", slug="test-game")
    event = Event(
        host=user,
        name="Test Event",
        start=datetime(2035, 1, 1),
    )
    db.session.add_all([user, game, event])
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
    return event, tournament


def test_bracket_operations_are_scoped_to_event_and_tournament(tournament_context):
    event, tournament = tournament_context
    bracket = BracketService.create_bracket(
        event.id,
        tournament.id,
        {"url": "https://example.test/bracket"},
    )

    assert BracketService.get_bracket(event.id, tournament.id).id == bracket.id
    assert BracketService.get_bracket_by_id(
        event.id, tournament.id, bracket.id
    ).url == "https://example.test/bracket"
    with pytest.raises(NotFoundError):
        BracketService.get_bracket_by_id(event.id, tournament.id + 1, bracket.id)
    with pytest.raises(ValidationError):
        BracketService.create_bracket(
            event.id, tournament.id, {"tournament_id": tournament.id + 1}
        )
    with pytest.raises(ValidationError):
        BracketService.update_bracket(
            event.id, tournament.id, bracket.id, {"tournament_id": tournament.id + 1}
        )

    BracketService.update_bracket(
        event.id, tournament.id, bracket.id, {"url": "https://example.test/updated"}
    )
    assert db.session.get(Bracket, bracket.id).url == "https://example.test/updated"
    BracketService.delete_bracket(event.id, tournament.id, bracket.id)
    assert db.session.get(Bracket, bracket.id) is None


def test_tournament_update_parses_iso_dates_and_rejects_invalid_dates(tournament_context):
    event, tournament = tournament_context
    updated = TournamentService.update_tournament(
        event.id,
        tournament.id,
        {"start": "2035-03-01T12:30:00"},
    )

    assert updated.start == datetime(2035, 3, 1, 12, 30)
    with pytest.raises(ValidationError):
        TournamentService.update_tournament(
            event.id, tournament.id, {"start": "not-a-date"}
        )
    with pytest.raises(ValidationError):
        TournamentService.update_tournament(event.id, tournament.id, None)
