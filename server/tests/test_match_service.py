from datetime import datetime

import pytest
from flask import Flask

from extensions import db
from models import Event, Game, Match, Tournament, TournamentCompetitor, User
from services import MatchService
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
def match_context(app):
    host = User(email="match-host@example.com")
    host.password_hash = "correct horse battery staple"
    player_a = User(email="match-player-a@example.com")
    player_a.password_hash = "correct horse battery staple"
    player_b = User(email="match-player-b@example.com")
    player_b.password_hash = "correct horse battery staple"
    player_c = User(email="match-player-c@example.com")
    player_c.password_hash = "correct horse battery staple"
    game = Game(name="Match Test Game", slug="match-test-game")
    event = Event(
        host=host,
        name="Match Test Event",
        start=datetime(2035, 1, 1),
    )
    db.session.add_all([player_a, player_b, player_c, event, game])
    db.session.flush()

    tournament = Tournament(
        event=event,
        game=game,
        name="Match Tournament",
        start=datetime(2035, 2, 1),
        registration_deadline=datetime(2035, 1, 20),
        line_up_type="singles",
    )
    other_tournament = Tournament(
        event=event,
        game=game,
        name="Other Tournament",
        start=datetime(2035, 2, 1),
        registration_deadline=datetime(2035, 1, 20),
        line_up_type="singles",
    )
    db.session.add_all([tournament, other_tournament])
    db.session.flush()

    competitor_a = TournamentCompetitor(tournament=tournament, user=player_a)
    competitor_b = TournamentCompetitor(tournament=tournament, user=player_b)
    competitor_other = TournamentCompetitor(
        tournament=other_tournament, user=player_c
    )
    db.session.add_all([competitor_a, competitor_b, competitor_other])
    db.session.commit()
    return tournament, competitor_a, competitor_b, competitor_other


def test_create_rejects_winner_outside_match_competitors(match_context):
    tournament, competitor_a, competitor_b, competitor_other = match_context

    with pytest.raises(ValidationError, match="Winner must be one"):
        MatchService.create(
            tournament.event_id,
            tournament.id,
            {
                "round": "final",
                "competitor_a_id": competitor_a.id,
                "competitor_b_id": competitor_b.id,
                "winner_id": competitor_other.id,
            },
        )


def test_create_rejects_competitor_from_another_tournament(match_context):
    tournament, competitor_a, _, competitor_other = match_context

    with pytest.raises(ValidationError, match="must belong to the match tournament"):
        MatchService.create(
            tournament.event_id,
            tournament.id,
            {
                "round": "final",
                "competitor_a_id": competitor_a.id,
                "competitor_b_id": competitor_other.id,
            },
        )


def test_update_rejects_winner_outside_match_competitors(match_context):
    tournament, competitor_a, competitor_b, competitor_other = match_context
    match = MatchService.create(
        tournament.event_id,
        tournament.id,
        {
            "round": "final",
            "competitor_a_id": competitor_a.id,
            "competitor_b_id": competitor_b.id,
        },
    )

    with pytest.raises(ValidationError, match="Winner must be one"):
        MatchService.update(
            tournament.event_id,
            tournament.id,
            {"match_id": match.id, "winner_id": competitor_other.id},
        )


def test_update_rejects_competitor_from_another_tournament(match_context):
    tournament, competitor_a, competitor_b, competitor_other = match_context
    match = MatchService.create(
        tournament.event_id,
        tournament.id,
        {
            "round": "final",
            "competitor_a_id": competitor_a.id,
            "competitor_b_id": competitor_b.id,
        },
    )

    with pytest.raises(ValidationError, match="must belong to the match tournament"):
        MatchService.update(
            tournament.event_id,
            tournament.id,
            {"match_id": match.id, "competitor_b_id": competitor_other.id},
        )
