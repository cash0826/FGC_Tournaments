import { api } from "./api";

// Mainly admin service

// Returns all users 
export function getUsers() {
  return api.get('/users')
}

// create, update or delete a user
export function createUser(newUser) {
  return api.post('/users', newUser)
}

export function updateUser(userId, updatedUser) {
  return api.patch(`/users/${userId}`, updatedUser)
}

export function deleteUser(userId) {
  return api.delete(`/users/${userId}`)
}

// Add or delete roles to users
export function addRole(userId, role_name) {
  return api.post(`/users/${userId}/roles`, role_name)
}

export function removeRole(userId, role_name){
  return api.delete(`/users/${userId}/roles/${role_name}`)
}