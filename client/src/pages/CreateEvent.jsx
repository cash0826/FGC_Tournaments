import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { createEvent } from "../services/eventService";
import DateTimePicker from "../components/DateTimePicker"
import BackButton from "../components/BackButton";
import NavBar from '../components/NavBar'

function CreateEvent() {
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { user } = useAuth();
  const navigate = useNavigate();
  // Controlled input for form
  const [form, setForm] = useState({
    name: '',
    start: new Date(),
    end: new Date(),
    in_person: false,
    location: '',
    description: '',
    tie_breaking_rule: '',
    host_id: user.id
  })

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      const newEvent = await createEvent(form)
      navigate(`/events/${newEvent.id}`)
    } catch (err) {
      setError(err.message || 'Unable to create event')
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
        <section>
          <div className="form-container">
            <div className="row-header">
              <h1>New Event to host:</h1>
            </div>

            <div className="row-form">
              <form onSubmit={handleSubmit}> 
                <input
                  placeholder="Name of the event"
                  value={form.name}
                  onChange={(e)=> setForm({...form, name: e.target.value})}
                  required
                />
                Start:
                <DateTimePicker
                  value={form.start}
                  onChange={(dt)=> setForm({...form, start: dt})}
                  required
                />
                <br/>
                (Optional) End:
                <DateTimePicker
                  value={form.end}
                  onChange={(dt)=> setForm({...form, end: dt})}
                />
                <br/>
                In Person?:
                <input
                  type="checkbox"
                  checked={form.in_person}
                  onChange={(e)=> setForm({...form, in_person: e.target.checked})}
                />
                <input
                  placeholder="Location"
                  value={form.location}
                  onChange={(e)=> setForm({...form, location: e.target.value})}
                  required
                />
                <textarea
                  placeholder="(Optional) Include all relevant details about the event..."
                  value={form.description}
                  onChange={(e)=> setForm({...form, description: e.target.value})}
                />
                <textarea
                  placeholder="(Optional) Include any rules or general code of conduct..."
                  value={form.tie_breaking_rule}
                  onChange={(e)=> setForm({...form, tie_breaking_rule: e.target.value})}
                />
                {error && <p role="alert">{error}</p>}
                <button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? 'Creating Event...' : 'Create New Event'}
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

export default CreateEvent;
