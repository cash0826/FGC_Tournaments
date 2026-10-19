import { useState } from "react";
import { useParams, useOutletContext } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { addBracket, deleteBracket } from "../services/bracketService";

function Bracket() {
  const { eventId, tournamentId } = useParams();
  const { user } = useAuth();
  const { event } = useOutletContext();
  const tournament = event.tournaments.find((t) => String(t.id) === String(tournamentId)) || null
  const [bracket, setBracket] = useState(null);   // Not an array, just a single bracket object
  const [isOpen, setIsOpen] = useState(false);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  // Controlled input
  const [url, setUrl] = useState('');

  // Authorization check: render button if admin or owner
  const isOwner = Boolean(tournament && user && event.host_id === user.id)
  const isAdmin = Boolean(tournament && user?.roles?.some(userRole => userRole.role?.name === "admin"))

  // Add Bracket
  async function handleAdd(e) {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)
    let data = {
      url: url,
      tournament_id: parseInt(tournamentId)
    }
    try {
      const newBracket = await addBracket(eventId, tournamentId, data)
      setBracket(newBracket)
      setUrl('')
    } catch (err) {
      setError(err.message || 'Unable to add bracket')
    } finally {
      setIsSubmitting(false)
      setIsOpen(false)
    }
  }

  // Delete Bracket
  async function handleDelete(e) {
    setError('')
    setIsSubmitting(true)
    try {
      await deleteBracket(eventId, tournamentId, bracket.id)
      setBracket(null)
      setUrl('')
    } catch (err) {
      setError(err.message || 'Unable to delete bracket')
    } finally {
      setIsSubmitting(false)
    }
  }

  const isEmpty = !bracket

  return (
    <>
      <div className="bracket-add-bracket">
        {isOpen ? (
          <>
            <input
              type="url"
              placeholder="link to bracket"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
            <button onClick={handleAdd} disabled={isSubmitting}>
              {isSubmitting ? 'Adding...' : 'Confirm Bracket'}
            </button>
            <button onClick={(e) => setIsOpen(false)}>Cancel</button>
            {error && <p role="alert">{error}</p>}
          </>
        ) : (
          <>
            <div className="bracket-container">
              {isEmpty ? (
                <>
                  <p>No Bracket posted yet</p>
                  {(isOwner || isAdmin) && (
                    <button onClick={()=> setIsOpen(true)}>Add Bracket Link</button>
                  )}
                </>
              ) : (
                <>
                  <p>{bracket.url}</p>
                  <button onClick={handleDelete}>
                    {isSubmitting ? 'Deleting...' : 'Delete Bracket'}
                  </button>
                  {error && <p role="alert">{error}</p>}
                </>
              )}
            </div>
          </>
        )}
      </div>
    </>
  )
}

export default Bracket;