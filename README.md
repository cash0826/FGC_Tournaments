# FGC_Tournaments

This is a single page application that registers players in fighting game tournaments. Users can manage their profile information, update their password, create teams for team-type tournaments, and register to tournaments. 

Event owners, which are stored as hosts, can manage their event information, manage tournaments in an event, manage sponsors backing the event, manage matches, manage brackets and remove registered competitors. 

Users with host permissions can create an event.

Admins can permanently delete a user, add games to the app, and manage sponsors. 

## Backend
```
pipenv run python app.py
```

## Testing 
```
pipenv run python -m pytest -q
```

