import { api } from "./api";

// get all tournaments (public)
export function listEventTournaments(eventId) {
  return api.get(`/events/${eventId}/tournaments`)
}

// create, update or delete (admin or owner)
export function createEventTournament(eventId, newTournament) {
  return api.post(`/events/${eventId}/tournaments`, newTournament)
}

export function updateEventTournament(eventId, tournamentId, updated) {
  return api.patch(`/events/${eventId}/tournaments/${tournamentId}`, updated)
}

export function deleteEventTournament(eventId, tournamentId) {
  return api.delete(`/events/${eventId}/tournaments/${tournamentId}`)
}

// view tournament details (public)
export function getTournament(eventId, tournamentId) {
  return api.get(`/events/${eventId}/tournaments/${tournamentId}`)
}

/* Manage Competitors */

// register as a competitor (public)
export function register(eventId, tournamentId, userId) {
  return api.post(`/events/${eventId}/tournaments/${tournamentId}/competitors`, userId)
}

// delete a tournament competitor (admin or owner)
export function deleteCompetitor(eventId, tournamentId, userId) {
  return api.delete(`/events/${eventId}/tournaments/${tournamentId}/competitors/${userId}`, )
}