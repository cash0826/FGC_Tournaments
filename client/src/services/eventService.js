import { api } from "./api";

// get all events (public)

export function listEvents() {
  return api.get('/events')
}

// create, update and delete (admin or host)
export function createEvent(newEvent) {
  return api.post('/events', newEvent)
}

export function updateEvent(eventId, updatedEvent) {
  return api.patch(`/events/${eventId}`, updatedEvent)
}

export function deleteEvent(eventId) {
  return api.delete(`/events/${eventId}`)
}

// view event details (public)
export function getEvent(eventId) {
  return api.get(`/events/${eventId}`)
}