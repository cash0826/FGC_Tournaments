import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import NavBar from '../components/NavBar'

function Signup() {
  const { createUser } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault();
    setError('')
    setIsSubmitting(true)
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }
    setIsSubmitting(true)
    try {
      await createUser({ username, email, password})
      navigate('/')
    } catch (error) {
      setError(error.message || 'Unable to signup')
    } finally {
      setIsSubmitting(false)
    }
  }

  return(
    <>
      <header>
        <NavBar/>
      </header>

      <main>
        <section>
          <div className="form-container">
            <div className="row-header">
              <h1>Sign up and join our events!</h1>
            </div>

            <div className="row-form">
              <form onSubmit={handleSubmit}>
                <input
                  placeholder="Desired Username"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  required
                />
                <input
                  placeholder="Email"
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                />
                <input
                  placeholder="Password"
                  type="password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                />
                <input
                  placeholder="Confirm Password"
                  type="password"
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  required
                />
                {error && <p role="alert">{error}</p>}
                <button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? 'Submitting...' : 'Submit'}
                </button>
              </form>
            </div>

            <div className="row-link">
              <p>
                Already have an account? <Link to="/login">Log in</Link>
              </p>
            </div>
          </div>
        </section>
      </main>
    </>
  )
}

export default Signup;