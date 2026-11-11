import { useState } from "react";
import { updateStanding, deleteStanding } from "../../services/standingService";

function StandingRow({ standing, eventId, tournamentId, isOwner, isAdmin, setStandings, ...props }) {
  const [error, setError] = useState('')  
  const [isEditing, setIsEditing] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [points, setPoints] = useState(standing.points);

  // Toggle inline editing
  function startEditing() {
    setPoints(points)
    setIsEditing(true)
  }

  // Update
  async function handleSave(e) {
    setError('')
    setIsSubmitting(true)
    try {
      const updatedStanding = await updateStanding(eventId, tournamentId, standing.id, {points: parseInt(points)})
      setStandings((current) => 
        current.map((item) => item.id === updatedStanding.id ? updatedStanding : item)
      )
    } catch (err) {
      setError(err.message || 'Unable to update standing')
    } finally {
      setIsSubmitting(false)
      setIsEditing(false)
    }
  }

  // Delete
  async function handleDelete(e) {
    setIsSubmitting(true)
    try {
      await deleteStanding(eventId, tournamentId, standing.id)
      setStandings((current) => current.filter((item) => item.id !== standing.id))
    } catch (err) {
      setError(err.message || 'Unable to delete standing')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="standings-standing-row">
      {isEditing ? (
        <>
          <p>{standing.competitor.user.username}</p>
          <input
            type="number"
            placeholder="points"
            value={points}
            onChange={(e) => setPoints(e.target.value)}
            required
          />
          <button onClick={handleSave} disabled={isSubmitting}>
            {isSubmitting ? 'Saving...' : 'Save'}
          </button>
          <button onClick={() => setIsEditing(false)}>Cancel</button>
        </>
      ) : (
        <>
          <p>{standing.competitor.user.username}--{standing.points}</p>
          {(isOwner || isAdmin) && (
            <>
              <button onClick={startEditing}>Edit</button>
              <button onClick={handleDelete}>Delete</button>
              {error && <p role="alert">{error}</p>}
            </>
          )}
        </>
      )}
    </div>
  )
}

export default StandingRow;