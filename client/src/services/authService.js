import { api } from "./api";

// Basic Authorization
export function signup(userData) {
  return api.post('/signup', userData)
}

export function login(userData) {
  return api.post('/login', userData)
}

export function getCurrentUser(token) {
  return api.get('/me', token)
}

// Profile (user) - GET/PATCH
export function updateProfile(userId, updatedProfile) {
  return api.patch(`/me/${userId}`, updatedProfile)
}