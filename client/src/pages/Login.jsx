import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import NavBar from '../components/NavBar'

function Login() {
  const { authenticateUser } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault();
    setError('')
    setIsSubmitting(true)
    try {
      await authenticateUser({ email, password })
      navigate('/')
    } catch (error) {
      setError(error.message || 'unable to log in')
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
              <h1>Welcome Back</h1>
            </div>

            <div className="row-form">
              <form onSubmit={handleSubmit}>
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
                {error && <p role="alert">{error}</p>}
                <button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? 'Logging in…' : 'Log in'}
                </button>
              </form>
            </div>

            <div className="row-link">
              <p>
                Joining us for the first time? <Link to="/signup">Signup</Link>
              </p>
            </div>
          </div>
        </section>
      </main>
    </>
  )
}

export default Login;


