## API Reference

Accessibility of resources listed in the following order:  

No login required: [Public Resources](#public-resources)

Requires an authenticated user: [Authenticated Resources](#authenticated-resources)

Requires admin role or event ownership: [Event_Owner](#event-owner-resources-you-must-be-hosting-the-event)

Requires host role: [Host](#host-resources)

Requires admin role: [Admin](#admin-resources)

### Public Resources

#### Get all games

```http
  GET /api/games
```

#### Get a game by id

```http
  GET /api/games/{id}
```
| Path Param | Type      | Description                        |
| :--------- | :-------- | :--------------------------------- |
| `id`       | `integer` | **Required**. Id of game to fetch  |

#### Get all sponsors

```http
  GET /api/sponsors
```

#### Get all events

```http
  GET /api/events
```

#### Get an event by id

```http
  GET /api/events/{id}
```
| Path Param | Type     | Description                        |
| :--------- | :------- | :--------------------------------- |
| `id`       | `integer`| **Required**. Id of event to fetch |

#### Get all sponsors backing an event

```http
  GET /api/events/{id}/sponsors
```
| Path Param | Type     | Description                       |
| :--------- | :------- | :-------------------------------- |
| `id`       | `integer`| **Required**. Id of event to fetch |

#### Get all tournaments in an event

```http
  GET /api/events/{id}/tournaments
```
| Path Param | Type     | Description                        |
| :--------- | :------- | :--------------------------------- |
| `id`       | `integer`| **Required**. Id of event to fetch |

#### Get a single tournament within an event

```http
  GET /api/events/{event_id}/tournaments/{tournament_id}
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of event to fetch |
| `tournament_id` | `integer` | **Required**. Id of tournament to fetch |

#### Get all registered competitors in a single tournament within an event

```http
  GET /api/events/{event_id}/tournaments/{tournament_id}/competitors
```
| Path Param      | Type      | Description                       |
| :-------------- | :-------- | :-------------------------------- |
| `event_id`      | `integer` | **Required**. Id of event to fetch |
| `tournament_id` | `integer` | **Required**. Id of tournament to fetch |

#### Get associated bracket url in a single tournament within an event

```http
  GET /api/events/{event_id}/tournaments/{tournament_id}/bracket
```
| Path Param | Type      | Description                       |
| :--------- | :-------- | :-------------------------------- |
| `id`       | `integer` | **Required**. Id of event to fetch |
| `id`       | `integer` | **Required**. Id of tournament to fetch |

#### Get all matches in a single tournament within an event

```http
  GET /api/events/{event_id}/tournaments/{tournament_id}/matches
```
| Path Param | Type     | Description                       |
| :--------- | :------- | :-------------------------------- |
| `id`       | `integer` | **Required**. Id of event to fetch |
| `id`       | `integer` | **Required**. Id of tournament to fetch |

#### Post a signup request. Returns a JSON Web Token and created authenticated user

```http
  POST /api/signup
```
| Keys supported   | Value Type  | Considerations                    |
| :--------------- | :---------- | :-------------------------------- |
| `email`          | `string`    | **Required**. Must contain @ within the string |
| `password`       | `string`    | **Required**. Must be at least 8 characters |
| `gamer_name`     | `string`    |  Must be unique |
| `first_name`     | `string`    |   |
| `last_name`      | `string`    |   |
| `bio`            | `text`      |   |
| `profile_pic_url`| `string`    |   |
| `contact_number` | `string`    |  Must be 7 to 15 digits with no spaces or hyphens. Optional: leading +. |

#### Post a login request. Returns a JSON Web Token and your public data

```http
  POST /api/login
```
| Keys supported   | Value Type  | Considerations                    |
| :--------------- | :---------- | :-------------------------------- |
| `email`          | `string`    | **Required**. Must contain @ within the string |
| `password`       | `string`    | **Required**. Must be at least 8 characters |

### Authenticated Resources

#### Get your public data

```http
  GET /api/me
```

#### Update your profile information

```http
  PATCH /api/me
```
| Keys supported   | Value Type  | Considerations                    |
| :--------------- | :---------- | :-------------------------------- |
| `gamer_name`     | `string`    |  Must be unique |
| `first_name`     | `string`    |   |
| `last_name`      | `string`    |   |
| `bio`            | `text`      |   |
| `profile_pic_url`| `string`    |   |
| `contact_number` | `string`    |  Must be 7 to 15 digits with no spaces or hyphens. |

#### Update your password

```http
  PATCH /api/me/password
```
| Keys supported    | Value Type  | Considerations                    |
| :---------------- | :---------- | :-------------------------------- |
| `current_password`| `string`    | **Required**. Must coincide with the existing password | 
| `new_password`    | `string`    | **Required**. Must be at least 8 characters | 


#### Get your linked social accounts

```http
  GET /api/me/social_accounts
```

#### Link a new social account to your user profile

```http
  POST /api/me/social_accounts
```
| Keys supported   | Value Type  | Considerations                    |
| :--------------- | :---------- | :-------------------------------- |
| `platform`       | `string`    | **Required**.  |
| `handle`         | `string`    | **Required**  | 

#### Unlink a social account from your user profile

```http
  DELETE /api/me/social_accounts
```
| Keys supported   | Value Type  | Considerations                    |
| :--------------- | :---------- | :-------------------------------- |
| `platform`       | `string`    | **Required**. Accepts x, twitch_tv, discord, xbox, steam, epic_games, battle.net and riot_games. |

#### Get your teams. Returns an object with an array of teams names that you are registered to

```http
  GET /api/me/teams
```

#### Create a new team. This team object can be registered as tournament_competitor IF the tournament is a teams-type tournament.

```http
  POST /api/teams
```
| Keys supported   | Value Type  | Considerations                    |
| :--------------- | :---------- | :-------------------------------- |
| `name`           | `string`    | **Required**. |
| `logo_url`       | `string`    | | 

#### Update an existing team

```http
  PATCH /api/teams/{id}
```
| Path Param | Type      | Description                        |
| :--------- | :-------- | :--------------------------------- |
| `id`       | `integer` | **Required**. Id of team to update |

| Keys supported   | Value Type  |
| :--------------- | :---------- |
| `name`           | `string`    |
| `logo_url`       | `string`    | 

#### Delete an existing team

```http
  DELETE /api/teams/{team_id}
```
| Path Param | Type      | Description                        |
| :--------- | :-------- | :--------------------------------- |
| `team_id`  | `integer` | **Required**. Id of team to update |

#### Add an existing user to an existing team

```http
  POST /api/teams/{team_id}/members
```
| Path Param | Type      | Description                        |
| :--------- | :-------- | :--------------------------------- |
| `team_id`  | `integer` | **Required**. Id of team to update |

| Keys supported   | Value Type  | Considerations                    |
| :--------------- | :---------- | :-------------------------------- |
| `user_id`        | `integer`   | **Required**. Id of existing user |
| `role_on_team`   | `string`    | **Required**. Accepts "captain" or "member" |

#### Remove an existing user from an existing team

```http
  DELETE /api/teams/{team_id}/members
```
| Path Param | Type      | Description                        |
| :--------- | :-------- | :--------------------------------- |
| `team_id`  | `integer` | **Required**. Id of team to update |

| Keys supported   | Value Type  | Considerations                    |
| :--------------- | :---------- | :-------------------------------- |
| `user_id`        | `integer`   | **Required**. Id of existing user |

#### Register team or user as a tournament_competitor. Also creates the standing for that competitor

```http
  POST /api/events/{event_id}/tournaments/{tournament_id}/competitors
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |
| `tournament_id` | `integer` | **Required**. Id of existing tournament |

| Keys supported   | Value Type  | Considerations                     |
| :--------------- | :---------- | :--------------------------------- |
| `user_id`        | `integer`    | **Required**. Id of existing user |
| `team_id`        | `integer`    | **Required**. Id of existing team |
| `seed`           | `integer`    | |

**Note:** Exactly one of user_id or team_id is accepted and which one is accepted relies on the tournament's line up type.

### Event Owner resources. You must be hosting the event.

#### Update an event

```http
  PATCH /api/events/{event_id}
```
| Path Param      | Type      | Description                         |
| :-------------- | :-------- | :---------------------------------- |
| `event_id`      | `integer` | **Required**. Id of event to update |

| Keys supported   | Value Type  |
| :--------------- | :---------- |
| `name`           | `integer`   |
| `start`          | `datetime`  |
| `end`            | `datetime`  |
| `in_person`      | `boolean`   |
| `location`       | `string`    |
| `description`    | `text`      |
| `rules`          | `text`      |

#### Delete an event

```http
  DELETE /api/events/{event_id}
```
| Path Param      | Type      | Description                         |
| :-------------- | :-------- | :---------------------------------- |
| `event_id`      | `integer` | **Required**. Id of event to delete |

#### Back an event with a sponsor

```http
  POST /api/events/{event_id}/sponsors
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |

| Keys supported      | Value Type  | Considerations               |
| :------------------ | :---------- | :--------------------------- |
| `sponsor`           | `string`    | **Required**. Sponsor's name |
| `sponsorship_tier`  | `string`    | Accepts community, bronze, silver and gold |
| `amount`            | `decimal`   | |

#### Remove a sponsor from an event

```http
  DELETE /api/events/{event_id}/sponsors
```
| Keys supported      | Value Type  | Considerations               |
| :-------------------| :---------- | :--------------------------- |
| `sponsor`           | `string`    | **Required**. Sponsor's name |


#### Add a tournament to an event

```http
  POST /api/events/{id}/tournaments
```
| Path Param | Type     | Description                        |
| :--------- | :------- | :--------------------------------- |
| `id`       | `integer`| **Required**. Id of existing event |

| Keys supported         | Value Type  | Considerations                      |
| :--------------------- | :---------- | :---------------------------------- |
| `game_id`              | `integer`   | **Required**. Id of available game  |
| `name`                 | `string`    | **Required** |
| `start`                | `datetime`  | **Required** |
| `registration_deadline`| `datetime`  | |
| `gaming_platform`      | `string`    | Accepts ps4, ps4_pro, ps5, MiSTeR FPGA or other |
| `line_up_type`         | `string`    | Accepts singles, teams or other |

#### Update a tournament within an event

```http
  PATCH /api/events/{event_id}/tournaments/{tournament_id}
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |
| `tournament_id` | `integer` | **Required**. Id of tournament to update |

| Keys supported         | Value Type  | Considerations                      |
| :--------------------- | :---------- | :---------------------------------- |
| `name`                 | `string`    | **Required** |
| `start`                | `datetime`  | **Required** |
| `registration_deadline`| `datetime`  | |
| `gaming_platform`      | `string`    | Accepts ps4, ps4_pro, ps5, MiSTeR FPGA or other |

#### Delete a tournament within an event

```http
  DELETE /api/events/{event_id}/tournaments/{tournament_id}
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |
| `tournament_id` | `integer` | **Required**. Id of tournament to delete |

#### Removes a tournament competitor from a tournament.

```http
  DELETE /api/events/{event_id}/tournaments/{tournament_id}/competitors/{competitor_id}
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |
| `tournament_id` | `integer` | **Required**. Id of existing tournament |
| `competitor_id` | `integer` | **Required**. Id of tournament competitor to delete |

#### Update a competitor's standing in a tournament

```http
  PATCH /api/events/{event_id}/tournaments/{tournament_id}/competitors/{competitor_id}
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |
| `tournament_id` | `integer` | **Required**. Id of existing tournament |
| `competitor_id` | `integer` | **Required**. Id of tournament competitor to update |

| Keys supported | Value Type  |
| :------------- | :---------- |
| `points`       | `integer`   |
| `rank`         | `integer`   |

#### Add a bracket

```http
  POST /api/events/{event_id}/tournaments/{tournament_id}/bracket
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |
| `tournament_id` | `integer` | **Required**. Id of existing tournament |

| Keys supported  | Value Type  | Considerations                      |
| :-------------- | :---------- | :---------------------------------- |
| `url`           | `text`      | **Required**. Link to bracket       |

#### Update a bracket's url

```http
  PATCH /api/events/{event_id}/tournaments/{tournament_id}/bracket/{bracket_id}
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |
| `tournament_id` | `integer` | **Required**. Id of existing tournament |
| `bracket_id`    | `integer` | **Required**. Id of bracket to update |

| Keys supported  | Value Type  |
| :-------------- | :---------- |
| `url`           | `text`      |

#### Delete a bracket

```http
  DELETE /api/events/{event_id}/tournaments/{tournament_id}/bracket/{bracket_id}
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |
| `tournament_id` | `integer` | **Required**. Id of existing tournament |
| `bracket_id`    | `integer` | **Required**. Id of bracket to delete |

#### Add a match

```http
  POST /api/events/{event_id}/tournaments/{tournament_id}/matches
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |
| `tournament_id` | `integer` | **Required**. Id of existing tournament |

| Keys supported    | Value Type  | Considerations               |
| :---------------- | :---------- | :--------------------------- |
| `round`           | `string`    | **Required**.                |
| `start_time`      | `datetime`  |  |
| `status`          | `string`    | Default is 'Pending'. Accepts in progress, canceled, or completed        |
| `competitor_a_id` | `integer`   | **Required**. Must match a tournament_competitor |
| `competitor_b_id` | `integer`   | **Required**. Must match a tournament_competitor |
| `winner_id`       | `integer`   | Must match competitor a or b | 

#### Update a match

```http
  PATCH /api/events/{event_id}/tournaments/{tournament_id}/matches/{match_id}
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |
| `tournament_id` | `integer` | **Required**. Id of existing tournament |
| `match_id`      | `integer` | **Required**. Id of match to update |

| Keys supported    | Value Type  |
| :---------------- | :---------- |
| `round`           | `string`    |
| `start_time`      | `datetime`  |
| `status`          | `string`    |
| `competitor_a_id` | `integer`   |
| `competitor_b_id` | `integer`   |
| `winner_id`       | `integer`   |

#### Delete a match

```http
  DELETE /api/events/{event_id}/tournaments/{tournament_id}/matches/{match_id}
```
| Path Param      | Type      | Description                        |
| :-------------- | :-------- | :--------------------------------- |
| `event_id`      | `integer` | **Required**. Id of existing event |
| `tournament_id` | `integer` | **Required**. Id of existing tournament |
| `match_id`      | `integer` | **Required**. Id of match to delete |


### Host Resources

#### Create an event

```http
  POST /api/events
```

| Keys supported    | Value Type  | Considerations               |
| :---------------- | :---------- | :--------------------------- |
| `name`            | `string`    | **Required**.                |
| `start`           | `datetime`  | **Required**.                |
| `end`             | `datetime`  |                              |
| `in_person`       | `boolean`   | Default is false             |
| `location`        | `string`    |                              |
| `description`     | `text`      |                              |
| `rules`           | `text`      |                              |

**Note:** The host_id will be assigned from the current user_id


### Admin Resources

#### Delete a user

```http
  DELETE /api/users/{user_id}
```
| Path Param | Type      | Description                        |
| :--------- | :-------- | :--------------------------------- |
| `user_id`  | `integer` | **Required**. Id of user to delete |

#### Assign a role to a user

```http
  POST /api/users/{user_id}/roles
```
| Path Param | Type      | Description                        |
| :--------- | :-------- | :--------------------------------- |
| `user_id`  | `integer` | **Required**. Id of user to update |

| Keys supported  | Value Type  | Considerations                      |
| :-------------- | :---------- | :---------------------------------- |
| `role`          | `string`      | **Required**. Accepts admin, host, player or viewer |

#### Removes a role from a user

```http
  DELETE /api/users/{user_id}/roles
```
| Path Param | Type      | Description                        |
| :--------- | :-------- | :--------------------------------- |
| `user_id`  | `integer` | **Required**. Id of user to update |

| Keys supported  | Value Type  | Considerations                      |
| :-------------- | :---------- | :---------------------------------- |
| `role`          | `string`      | **Required**. Admin, host, player or viewer |


####  Add a game to the app. Games will be used for tournaments

```http
  POST /api/games
```
| Keys supported  | Value Type  | Considerations                      |
| :-------------- | :---------- | :---------------------------------- |
| `name`          | `string`    | Must be unique                      |
| `slug`          | `string`    | Must be unique                      |
| `publisher`     | `string`    |                                     | 
| `genre`         | `string`    |                                     | 
| `picture_url`   | `text`      |                                     | 

####  Update a game from the app

```http
  PATCH /api/games/{game_id}
```
| Path Param | Type      | Description                        |
| :--------- | :-------- | :--------------------------------- |
| `game_id`  | `integer` | **Required**. Id of game to update |

| Keys supported  | Value Type  | Considerations                      |
| :-------------- | :---------- | :---------------------------------- |
| `name`          | `string`    | Must be unique                      |
| `slug`          | `string`    | Must be unique                      |
| `publisher`     | `string`    |                                     | 
| `genre`         | `string`    |                                     | 
| `picture_url`   | `text`      |                                     | 

####  Delete a game from the app

```http
  DELETE /api/games/{game_id}
```

####  Add a sponsor to the app. Sponsors will be used to back events

```http
  POST /api/sponsors
```
| Keys supported  | Value Type  | Considerations                      |
| :-------------- | :---------- | :---------------------------------- |
| `name`          | `string`    | **Required**. Must be unique        |
| `logo_url`      | `text`      | Must be unique                      |
| `website`       | `text`      |                                     | 
| `contact_email` | `text`      | Must be a valid format with @ in the address    | 

####  Update a sponsor from the app

```http
  PATCH /api/sponsors/{sponsor_id}
```
| Path Param   | Type      | Description                           |
| :----------- | :-------- | :------------------------------------ |
| `sponsor_id` | `integer` | **Required**. Id of sponsor to update |

| Keys supported  | Value Type  | Considerations                      |
| :-------------- | :---------- | :---------------------------------- |
| `name`          | `string`    | Must be unique                      |
| `logo_url`      | `text`      | Must be unique                      |
| `website`       | `text`      |                                     | 
| `contact_email` | `text`      | Must be a valid format with @ in the address    | 

####  Delete a sponsor from the app

```http
  DELETE /api/sponsors/{sponsor_id}
```
