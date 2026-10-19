import { useState } from "react";
import { updateMatch, deleteMatch } from "../../services/matchService";
import { formatLongDateTime } from "../../utils/dateUtils"
import DateTimePicker from "../../components/DateTimePicker";

function MatchRow({ match, eventId, tournamentId, isOwner, isAdmin, setMatches, ...props }) {
  const [error, setError] = useState('')  
  const [isEditing, setIsEditing] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [form, setForm] = useState({
    round: '',
    start_time: new Date(),
    status: '',
  })

  // Toggle Inline Editing (using existing data)
  function startEditing() {
    setForm({
      round: match.round,
      start_time: match.start_time,
      status: match.status
    })
    setIsEditing(true)
  }

  // Update
  async function handleSave(e) {
    setError('')
    setIsSubmitting(true)
    try {
      const updatedMatch = await updateMatch(eventId, tournamentId, match.id, form)
      setMatches((current) =>
        current.map((item) => item.id === updatedMatch.id ? updatedMatch : item)
      )
    } catch (err) {
      setError(err.message || 'Unable to update match')
    } finally {
      setIsSubmitting(false)
      setIsEditing(false)
    }
  }

  // Delete
  async function handleDelete(e) {
    setIsSubmitting(true)
    try {
      await deleteMatch(eventId, tournamentId, match.id)
      setMatches((current) => current.filter((item) => item.id !== match.id))   // Removes match from list of matches
    } catch (err) {
      setError(err.message || 'Unable to delete match')
    } finally {
      setIsSubmitting(false)
    }
  }  

  return (
    <>
      {isEditing ? (
        <div className="form-container">
          <form>
            <div className="row-form">
              Round:
              <input
                name="round"
                value={form.round}
                onChange={(e)=> setForm({...form, round: e.target.value})}
                required
              />
              Start_time:
              <DateTimePicker
                name="start_time"
                value={form.start_time}
                onChange={(dt)=> setForm({...form, start_time: dt})}
                required
              />
              Status:
              <input
                name="status"
                placeholder="pending, in_progress, cancelled, completed"
                value={form.status}
                onChange={(e)=> setForm({...form, status: e.target.value})}
              />
              <button onClick={handleSave} disabled={isSubmitting}>
                {isSubmitting ? 'Saving...' : 'Save'}
              </button>
              <button onClick={() => setIsEditing(false)}>Cancel</button>
            </div>
          </form>
        </div>
      ) : (
        <div className="row">
          <p>{match.round} | {match.status}</p>
          <p>Time: {formatLongDateTime(match.start_time)}</p>
          {(isOwner || isAdmin) && (
            <>
              <button onClick={startEditing}>Edit</button>
              <button onClick={handleDelete}>Delete</button>
              {error && <p role="alert">{error}</p>}
            </>
          )}
        </div>
      )}
    </>
  )
}

export default MatchRow;