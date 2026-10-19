import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { createEventTournament } from "../services/tournamentService";
import DateTimePicker from "../components/DateTimePicker";
import BackButton from "../components/BackButton";
import NavBar from '../components/NavBar'

function AddTournament() {
  const { eventId } = useParams();
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();
  // Controlled input using form
  const [form, setForm] = useState({
    name: '',
    start_time: new Date(),
    registration_deadline: new Date(),
    game: '',
    platform: '',
    line_up_type: '',
    event_id: parseInt(eventId),
  })

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      const newTournament = await createEventTournament(eventId, form)
      navigate(`/events/${eventId}/tournaments/${newTournament.id}`)
    } catch (err) {
      setError(err.message || 'Unable to create a new tournament for event')
      setIsSubmitting(false)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <>
      <header>
        <NavBar/>
      </header>

      <main>
        <section >
          <div className="form-container">
            <div className="row-header">
              <h1>Add a tournament:</h1>
            </div>
            <div className="row-form">
              <form onSubmit={handleSubmit}>
                <input
                  placeholder="Name"
                  value={form.name}
                  onChange={(e) => setForm({...form, name: e.target.value})}
                  required
                />
                <DateTimePicker
                  placeholder="Start Time"
                  value={form.start_time}
                  onChange={(dt)=> setForm({...form, start_time: dt})}
                  required
                />
                <DateTimePicker
                  placeholder="Registration Deadline"
                  value={form.registration_deadline}
                  onChange={(dt)=> setForm({...form, registration_deadline: dt})}
                  required
                />
                <input
                name
                  placeholder="Game"
                  value={form.game}
                  onChange={(e) => setForm({...form, game: e.target.value})}
                  required
                />
                <input
                  placeholder="Platform"
                  value={form.platform}
                  onChange={(e) => setForm({...form, platform: e.target.value})}
                  required
                />
                <input
                  placeholder="1v1 (Singles), Teams..."
                  value={form.line_up_type}
                  onChange={(e) => setForm({...form, line_up_type: e.target.value})}
                  required
                />
                {error && <p role="alert">{error}</p>}
                <button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? 'Adding...' : 'Add a new tournament'}
                </button>
              </form>
            </div>
          </div>
        </section>
        <BackButton/>
      </main>
    </>
  )
}

export default AddTournament;