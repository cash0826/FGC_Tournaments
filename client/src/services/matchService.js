import { api } from "./api";

// get all matches (public)
export function listMatches(eventId, tournamentId) {
  return api.get(`/events/${eventId}/tournaments/${tournamentId}/matches`)
}

// create, update or delete (admin or owner)
export function createMatch(eventId, tournamentId, newMatch) {
  return api.post(`/events/${eventId}/tournaments/${tournamentId}/matches`, newMatch)
}

export function updateMatch(eventId, tournamentId, matchId, updated) {
  return api.patch(`/events/${eventId}/tournaments/${tournamentId}/matches/${matchId}`, updated)
}

export function deleteMatch(eventId, tournamentId, matchId) {
  return api.delete(`/events/${eventId}/tournaments/${tournamentId}/matches/${matchId}`)
}

// view match details (public)
export function getMatch(eventId, tournamentId, matchId) {
  return api.get(`/events/${eventId}/tournaments/${tournamentId}/matches/${matchId}`)
}