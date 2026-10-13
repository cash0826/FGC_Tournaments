from datetime import datetime

import pytest
from flask import Flask
from sqlalchemy.exc import IntegrityError

from extensions import db
from models import Event, Game, Standing, Team, Tournament, TournamentCompetitor, User
from services import StandingService, TournamentCompetitorService
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
    user = User(email="competitor-player@example.com", gamer_name="Test Player")
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
    singles_tournament = Tournament(
        event=event,
        game=game,
        name="Singles Tournament",
        start=datetime(2035, 2, 1),
        registration_deadline=datetime(2035, 1, 20),
        line_up_type="singles",
    )
    team_tournament = Tournament(
        event=event,
        game=game,
        name="Team Tournament",
        start=datetime(2035, 2, 1),
        registration_deadline=datetime(2035, 1, 20),
        line_up_type="teams",
    )
    unsupported_tournament = Tournament(
        event=event,
        game=game,
        name="Other Tournament",
        start=datetime(2035, 2, 1),
        registration_deadline=datetime(2035, 1, 20),
        line_up_type="other",
    )
    db.session.add_all([singles_tournament, team_tournament, unsupported_tournament])
    db.session.commit()
    return singles_tournament, team_tournament, unsupported_tournament, team, user


@pytest.mark.parametrize("entry_type", ["team", "user"])
def test_add_competitor_accepts_exactly_one_entry(competitor_context, entry_type):
    singles_tournament, team_tournament, _, team, user = competitor_context
    tournament = team_tournament if entry_type == "team" else singles_tournament
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
    tournament, _, _, _, _ = competitor_context

    with pytest.raises(ValidationError, match="Exactly one"):
        TournamentCompetitorService.add_competitor(
            tournament.event_id, tournament.id, data
        )


@pytest.mark.parametrize("data", [{"team_id": True}, {"user_id": 0}])
def test_add_competitor_rejects_invalid_entry_id(competitor_context, data):
    tournaments = competitor_context[:2]
    tournament = tournaments[1] if "team_id" in data else tournaments[0]

    with pytest.raises(ValidationError, match="positive integer"):
        TournamentCompetitorService.add_competitor(
            tournament.event_id, tournament.id, data
        )


@pytest.mark.parametrize(
    ("tournament_index", "data", "message"),
    [
        (0, {"team_id": 1}, "Singles tournaments require a user_id"),
        (1, {"user_id": 1}, "Team tournaments require a team_id"),
        (2, {"user_id": 1}, "does not support competitors"),
    ],
)
def test_add_competitor_rejects_entry_incompatible_with_lineup_type(
    competitor_context, tournament_index, data, message
):
    tournaments = competitor_context[:3]
    tournament = tournaments[tournament_index]

    with pytest.raises(ValidationError, match=message):
        TournamentCompetitorService.add_competitor(
            tournament.event_id, tournament.id, data
        )


def test_get_all_returns_team_names_and_standings(competitor_context):
    _, tournament, _, team, _ = competitor_context
    competitor = TournamentCompetitorService.add_competitor(
        tournament.event_id, tournament.id, {"team_id": team.id}
    )
    standing = competitor.standing
    standing.points = 3
    standing.rank = 1
    db.session.commit()

    competitors = StandingService.get_all(tournament.event_id, tournament.id)

    assert competitors == [
        {
            "tournament_id": tournament.id,
            "team_id": team.id,
            "user_id": None,
            "seed": None,
            "id": competitor.id,
            "team_name": team.name,
            "standing": standing.to_dict(),
        }
    ]


def test_get_all_returns_gamer_names_and_standings(competitor_context):
    tournament, _, _, _, user = competitor_context
    competitor = TournamentCompetitorService.add_competitor(
        tournament.event_id, tournament.id, {"user_id": user.id}
    )
    standing = competitor.standing
    standing.points = 5
    standing.rank = 2
    db.session.commit()

    competitors = StandingService.get_all(tournament.event_id, tournament.id)

    assert competitors == [
        {
            "tournament_id": tournament.id,
            "team_id": None,
            "user_id": user.id,
            "seed": None,
            "id": competitor.id,
            "gamer_name": user.gamer_name,
            "standing": standing.to_dict(),
        }
    ]


def test_get_all_rejects_unsupported_lineup_type(competitor_context):
    _, _, tournament, _, _ = competitor_context

    with pytest.raises(ValidationError, match="does not support competitors"):
        StandingService.get_all(tournament.event_id, tournament.id)


def test_add_competitor_creates_initial_standing(competitor_context):
    tournament, _, _, _, user = competitor_context
    competitor = TournamentCompetitorService.add_competitor(
        tournament.event_id, tournament.id, {"user_id": user.id}
    )

    competitors = StandingService.get_all(tournament.event_id, tournament.id)

    assert competitors[0]["gamer_name"] == user.gamer_name
    assert competitors[0]["standing"]["tournament_competitor_id"] == competitor.id
    assert competitors[0]["standing"]["points"] is None
    assert competitors[0]["standing"]["rank"] is None


def test_standing_is_unique_per_competitor(competitor_context):
    tournament, _, _, _, user = competitor_context
    competitor = TournamentCompetitorService.add_competitor(
        tournament.event_id, tournament.id, {"user_id": user.id}
    )
    duplicate_standing = Standing(tournament_competitor=competitor)
    db.session.add(duplicate_standing)

    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


@pytest.mark.parametrize(
    ("event_id", "tournament_id"),
    [(True, 1), (1, False), (0, 1), (1, 0)],
)
def test_get_all_validates_ids(competitor_context, event_id, tournament_id):
    with pytest.raises(ValidationError):
        StandingService.get_all(event_id, tournament_id)
