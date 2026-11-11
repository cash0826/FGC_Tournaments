import { api } from "./api";

// get bracket (public)
export function getBracket(eventId, tournamentId) {
  return api.get(`/events/${eventId}/tournaments/${tournamentId}/bracket`)
}

// create, update or delete (admin or owner)
export function addBracket(eventId, tournamentId, newBracket) {
  return api.post(`/events/${eventId}/tournaments/${tournamentId}/bracket`, newBracket)
}

export function updateBracket(eventId, tournamentId, bracketId, updated) {
  return api.patch(`/events/${eventId}/tournaments/${tournamentId}/bracket/${bracketId}`, updated)
}

export function deleteBracket(eventId, tournamentId, bracketId) {
  return api.delete(`/events/${eventId}/tournaments/${tournamentId}/bracket/${bracketId}`)
}