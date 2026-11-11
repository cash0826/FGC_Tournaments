import { useState } from "react";
import { useNavigate, useParams, useOutletContext } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { updateEvent, deleteEvent } from "../services/eventService"
import TournamentListItem from "../components/tournamentitem/TournamentListItem";
import DateTimePicker from "../components/DateTimePicker"
import { formatLongDate } from "../utils/dateUtils"

// Public Page (Read-only)
// If owner of the event or admin, Inline PATCH/DEL
function EventDetails() {
  const { eventId } = useParams();
  const { user } = useAuth();
  const { event, setEvent } = useOutletContext()
  const navigate = useNavigate();
  // Edit + Delete (owner or admin)
  const [isEditing, setIsEditing] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    name: '',
    start: new Date(),
    end: new Date(),
    in_person: false,
    location: '',
    description: '',
    tie_breaking_rule: ''
  })

  // Edit + Delete (owner or admin)
  const isOwner = Boolean(event && user && event.host_id === user.id)
  const isAdmin = Boolean(event && user?.roles?.some(userRole => userRole.role?.name === "admin"))

  function addTournament() {navigate(`/events/${eventId}/tournaments/create`)}

  function startEditing() {
    setError('')
    setForm({
      name: event.name,
      start: event.start,
      end: event.end,
      in_person: event.in_person,
      location: event.location,
      description: event.description,
      tie_breaking_rule: event.tie_breaking_rule
    })
    setIsEditing(true)
  }

  function handleChange(e) {setForm({...form, [e.target.name]: e.target.value})}
  
  async function handleSave(e) {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      const updated = await updateEvent(eventId, form)
      setEvent(updated)
      setIsEditing(false)
    } catch (err) {
      setError(err.message || 'Unable to update event')
    } finally {
      setIsSubmitting(false)
    }
  }

  async function handleDelete(e) {
    setError('')
    setIsSubmitting(true)
    try {
      await deleteEvent(eventId)
      navigate('/')
    } catch (err) {
      setError(err.message || 'Unable to delete event')
    } finally{
      setIsSubmitting(false)
    }
  }

  return (
    <>
      <section className="title">
        {isEditing ? (
          <div className="form-container">
            <form>
              <div className="row-form">
                <input
                  placeholder="Name"
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                />
              </div>
            </form>
          </div>
        ) : (
          <div className="container">
            <div className="row">
              <h2>{event.name}</h2>
            </div>

            <div className="row">
              <p>{formatLongDate(event.start)}</p>
            </div>

            <div className="row">
              <p>📍{event.location}</p>
            </div>
          </div>
        )}
      </section>

      <section className="event-FAQ-container">
        {isEditing ? (
          <div className="form-container">
            <form>
              <div className="row-form"></div>
                Start:
                <DateTimePicker
                  name="start"
                  value={form.start}
                  onChange={(dt)=> setForm({...form, start: dt})}
                />
                <br/>
                End:
                <DateTimePicker
                  name="end"
                  value={form.end}
                  onChange={(dt)=> setForm({...form, end: dt})}
                />
                <br/>
                Location
                <input
                  name="location"
                  value={form.location}
                  onChange={handleChange}
                />
                Description
                <textarea
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                />
                Rules
                <textarea
                  name="tie_breaking_rule"
                  value={form.tie_breaking_rule}
                  onChange={handleChange}
                />
                <button onClick={handleSave} disabled={isSubmitting}>
                  {isSubmitting ? 'Saving...' : 'Save'}
                </button>
                <button onClick={() => setIsEditing(false)}>Cancel</button>
                {error && <p role="alert">{error}</p>}
            </form>
          </div>
        ) : (
          <div className="details">
            <div className="container">
              <h2>Event Details</h2>
              <div className="row">
                <h3>Start</h3>
                <p>{formatLongDate(event.start)}</p>
              </div>
              <div className="row">
                <h3>End</h3>
                <p>{formatLongDate(event.start)}</p>
              </div>
              <div className="row">
                <h3>Location</h3>
                <p>{event.location}</p>
              </div>
              <div className="row">
                <h3>Description</h3>
                <p>{event.description}</p>
              </div>
              {event.tie_breaking_rule && (
                <div className="row">
                  <h3>Rules</h3>
                  <p>{event.tie_breaking_rule}</p>
                </div>
              )}
            </div>
          </div>
        )}
      </section>

      {event.tournaments.length !== 0 ? (
        <>
          <section>
            <div className="tournaments-banner">
              <div className="container">
                <h2>Open Tournaments (Click to Register)</h2>
              </div>
            </div>
            <div className="tournaments">
              <div className="container">
                {event.tournaments.map((tournament) => (
                  <TournamentListItem
                    key={tournament.id}
                    event={event}
                    tournament={tournament}
                  />
                ))} 
              </div>
            </div>
      </section>
        </>
      ) : (
        <section>
          <div className="tournaments-banner">
            <div className="container">
              <h2>No Tournaments Posted Yet</h2>
            </div>
          </div>
        </section>
      )}  


      <section className="nav-buttons">
        <div className="container">
          {(isOwner || isAdmin) && (
            <>
              <button onClick={addTournament}>Add Tournament to Event</button>
              <button onClick={startEditing}>Edit Event Details</button>
              <button onClick={handleDelete}>
                {isSubmitting ? 'Deleting...' : 'Delete Event'}
              </button>
              {error && <p role="alert">{error}</p>}
            </>
          )}
        </div>
      </section>
    </>
  )
}

export default EventDetails;