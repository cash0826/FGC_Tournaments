import { api } from "./api";

// get all standings (public)
export function listStandings(eventId, tournamentId) {
  return api.get(`/events/${eventId}/tournaments/${tournamentId}/standings`)
}

// create, update or delete (admin or owner)
export function createStanding(eventId, tournamentId, newStanding) {
  return api.post(`/events/${eventId}/tournaments/${tournamentId}/standings`, newStanding)
}

export function updateStanding(eventId, tournamentId, standingId, updated) {
  return api.patch(`/events/${eventId}/tournaments/${tournamentId}/standings/${standingId}`, updated)
}

export function deleteStanding(eventId, tournamentId, standingId) {
  return api.delete(`/events/${eventId}/tournaments/${tournamentId}/standings/${standingId}`)
}