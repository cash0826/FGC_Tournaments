# Gaming Tournament Management System — Redesigned ERD

This redesign keeps your existing `Role` / `User` / `Event` structure but introduces a **Team** and **Game** entity, unifies tournament entries under a single `TOURNAMENT_COMPETITOR` concept (so it works for both singles and team play), and adds **Sponsor** as a many-to-many relationship. It also normalizes the six nullable social-handle columns on `User` into a flexible `USER_SOCIAL_ACCOUNT` table. `Event` now only tracks its host — attendee tracking has been removed.

```mermaid
erDiagram
    ROLE ||--o{ USER_ROLE : "assigned to"
    USER ||--o{ USER_ROLE : "has"
    USER ||--o{ USER_SOCIAL_ACCOUNT : "links"
    USER ||--o{ EVENT : "hosts"
    EVENT ||--o{ TOURNAMENT : "contains"
    GAME ||--o{ TOURNAMENT : "featured in"
    TOURNAMENT ||--o{ MATCH : "schedules"
    TOURNAMENT ||--o{ TOURNAMENT_COMPETITOR : "registers"
    TOURNAMENT ||--o| BRACKET : "structured by"
    TOURNAMENT ||--o{ STANDING : "ranks"
    TOURNAMENT ||--o{ TOURNAMENT_SPONSOR : "backed by"
    SPONSOR ||--o{ TOURNAMENT_SPONSOR : "sponsors"
    TEAM ||--o{ TEAM_MEMBER : "composed of"
    USER ||--o{ TEAM_MEMBER : "plays as"
    TEAM ||--o{ TOURNAMENT_COMPETITOR : "enters (team)"
    USER ||--o{ TOURNAMENT_COMPETITOR : "enters (solo)"
    TOURNAMENT_COMPETITOR ||--o{ STANDING : "achieves"
    TOURNAMENT_COMPETITOR ||--o{ MATCH : "plays as side A"
    TOURNAMENT_COMPETITOR ||--o{ MATCH : "plays as side B"
    TOURNAMENT_COMPETITOR |o--o{ MATCH : "wins"
 
    ROLE {
        int id PK
        string name "admin, host, player, viewer"
        string description
        boolean is_system_role
    }
 
    USER {
        int id PK
        string email UK
        string first_name
        string last_name
        string username UK
        string password_hash
        text bio
        string profile_pic_url
        string contact_number
        datetime created_at
        datetime updated_at
    }
 
    USER_ROLE {
        int id PK
        int user_id FK
        int role_id FK
    }
 
    USER_SOCIAL_ACCOUNT {
        int id PK
        int user_id FK
        string platform "x, discord, twitch, xbox, steam, epic_games, battle_net, riot_games"
        string handle
    }
 
    EVENT {
        int id PK
        string name
        datetime start
        datetime end
        boolean in_person
        string location
        text description
        text tie_breaking_rule
        int host_id FK
    }
 
    GAME {
        int id PK
        string name
        string publisher
        string genre
        string supported_platforms "e.g. xbox, ps4, ps5, pc"
    }
 
    TOURNAMENT {
        int id PK
        int event_id FK
        int game_id FK
        string name
        datetime start_time
        datetime registration_deadline
        string platform "xbox, ps4, ps5"
        string line_up_type "singles, team"
    }
 
    BRACKET {
        int id PK
        int tournament_id FK
        text url
    }
 
    TEAM {
        int id PK
        string name
        string logo_url
        datetime created_at
    }
 
    TEAM_MEMBER {
        int id PK
        int team_id FK
        int user_id FK
        string role_on_team "captain, member"
        datetime joined_at
    }
 
    TOURNAMENT_COMPETITOR {
        int id PK
        int tournament_id FK
        int team_id FK "nullable"
        int user_id FK "nullable"
        int seed
        datetime registered_at
    }
 
    MATCH {
        int id PK
        int tournament_id FK
        string round
        datetime start_time
        string status "pending, in_progress, cancelled, completed"
        int competitor_a_id FK
        int competitor_b_id FK
        int winner_id FK "nullable"
    }
 
    STANDING {
        int id PK
        int tournament_competitor_id FK
        int points
        int rank
        datetime updated_at
    }
 
    SPONSOR {
        int id PK
        string name
        string logo_url
        string website
        string contact_email
    }
 
    TOURNAMENT_SPONSOR {
        int id PK
        int tournament_id FK
        int sponsor_id FK
        string sponsorship_tier
        decimal amount
    }
```

## Key design decisions

- **`TEAM` + `TEAM_MEMBER`** — a team can have many players, and a player (user) can belong to more than one team over time, since `TEAM_MEMBER` is a join table rather than a `team_id` column on `User`.
- **`GAME` as its own entity** — `Tournament.game_id` points at it, so one game can back many tournaments without duplicating game metadata each time.
- **`TOURNAMENT_COMPETITOR` unifies singles and team entries** — it has both a nullable `team_id` and a nullable `user_id`. Which one is populated is driven by `Tournament.line_up_type`. This is the entity that both `Standing` and `Match` hang off of, so ranking and match logic doesn't need to branch on singles-vs-team.
- **`MATCH` references `TOURNAMENT_COMPETITOR` three times** — `competitor_a_id` and `competitor_b_id` are the two sides (mandatory), and `winner_id` is a nullable reference to whichever of the two won. Enforce at the app/DB level that `winner_id` must equal `competitor_a_id` or `competitor_b_id`.
- **`STANDING` keys off `tournament_competitor_id`** (not `tournament_id` + `team_id` directly) — since a competitor row is already scoped to one tournament, this naturally gives you "the same team/player has different standings across different tournaments" without duplicate foreign keys.
- **`SPONSOR` + `TOURNAMENT_SPONSOR`** — a standard many-to-many join, so a tournament can have several sponsors and a sponsor can back several tournaments, with tier/amount stored per sponsorship rather than per sponsor.
- **`USER_SOCIAL_ACCOUNT`** — replaces the six nullable `*_user` columns on `User` with rows, so adding a new platform later doesn't require a schema migration.

## Business rules to enforce outside the ERD

These aren't expressible as plain foreign keys and should live in application logic or DB constraints:
- `TOURNAMENT_COMPETITOR`: exactly one of `team_id` / `user_id` must be set, matching `Tournament.line_up_type`.
- `MATCH.winner_id`, when set, must equal `competitor_a_id` or `competitor_b_id`.
- `MATCH.competitor_a_id` and `competitor_b_id` should belong to the same `tournament_id` as the match itself.