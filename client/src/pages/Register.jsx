import { useState } from "react";
import { useNavigate, useParams, useOutletContext } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { register } from "../services/tournamentService";

// Leaving Register as page to add competitors for tournament
// May develop into Payment Page in the future. Status paid? Methods of payment?

function Register() {
  const { eventId, tournamentId } = useParams();
  const { user } = useAuth();
  const { event, setEvent } = useOutletContext();
  const navigate = useNavigate();
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const tournament = event.tournaments.find((item) => String(item.id) === String(tournamentId))

  async function handleSubmit(e) {
    e.preventDefault();
    setError('')
    setIsSubmitting(true)
    try {
      const competitor = await register(eventId, tournamentId, user.id)
      setEvent((currentEvent) => ({
        ...currentEvent,
        tournaments: currentEvent.tournaments.map((item) =>
          String(item.id) === String(tournamentId)
            ? {
                ...item,
                competitors: [...item.competitors, competitor]
              }
            : item
        )
      }))
      navigate(`/events/${eventId}/tournaments/${tournamentId}`)
    } catch (err) {
      setError(err.message || 'Unable to register to tournament')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <>
      <h1>Register to {tournament.name} for Event {event.name}</h1>
      <p>Event Registration Fee: c2,000 colones </p>
      <p>Tournament Competitor Registration Fee: c3,000 colones </p>
      <p>Payment to be made to SINPE Movil: ####-####</p>
      <form>
        {error && <p role="alert">{error}</p>}
        <button type="submit" onClick={handleSubmit}>
          {isSubmitting ? 'Registering...' : 'Confirm Registration'}
        </button>
      </form>
    </>
  )
}

export default Register;