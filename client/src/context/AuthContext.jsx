// src/context/AuthContext.jsx
import { createContext, useContext, useState, useEffect } from "react";
import { getCurrentUser, login, signup } from "../services/authService";

const AuthContext = createContext(null);

export function useAuthContext() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load user profile if token exists
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      setIsLoading(false)
      setUser(null)
      return
    }
    getCurrentUser()
      .then((data)=> setUser(data))
      .catch(()=> {
        localStorage.removeItem('token')
        setUser(null)
      })
      .finally( () => setIsLoading(false))
  }, []);

  async function authenticateUser(credentials) {
    const { token: token, user: loggedInUser } = await login(credentials)
    localStorage.setItem("token", token);
    setUser(loggedInUser)
    return loggedInUser
  }

  async function createUser(newUserDetails) {
    const { token: token, user: newUser } = await signup(newUserDetails)
    localStorage.setItem("token", token);
    setUser(newUser)
    return newUser
  }

  async function logout() {
    localStorage.removeItem('token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{user, setUser, isLoading, authenticateUser, createUser, logout}}>
      {children}
    </AuthContext.Provider>
  )
}
