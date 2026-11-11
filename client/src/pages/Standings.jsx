import { useState } from "react";
import { useParams, useOutletContext } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { createStanding } from "../services/standingService";
import StandingRow from "../components/standings/StandingRow";

function Standings() {
  const { eventId, tournamentId } = useParams();
  const { event } = useOutletContext();
  const { user } = useAuth();
  const tournament = event.tournaments.find((t) => String(t.id) === String(tournamentId)) || null
  const [standings, setStandings] = useState(tournament.standings);
  const [isOpen, setIsOpen] = useState(false);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  // Controlled inputs
  const [competitorId, setCompetitorId] = useState('');  
  const [points, setPoints] = useState('');

  // Authorization check: render button if admin or owner
  const isOwner = Boolean(tournament && user && event.host_id === user.id)
  const isAdmin = Boolean(tournament && user?.roles?.some(userRole => userRole.role?.name === "admin"))

  async function handleAdd(e) {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)
    let data = {
      competitor_id: parseInt(competitorId), 
      points: parseInt(points), 
      tournament_id: parseInt(tournamentId)
    }
    try {
      const newStanding = await createStanding(eventId, tournamentId, data)
      setStandings((current) => [newStanding, ...current])
    } catch (err) {
      setError(err.message || 'Unable to add a standing')
    } finally {
      setIsSubmitting(false)
      setIsOpen(false)
    }
  }

  if (!standings) return <p>Standings not found</p>
  const isEmpty = Boolean(standings.length === 0)

  return (
    <>
      <div className="standings-standing-container">
        {isEmpty ? (
          <>
            <p> No Standings posted yet</p>
          </>
        ) : (
          <>
            {standings.map((standing)=> (
              <StandingRow
                key={standing.id}
                standing={standing}
                eventId={eventId}
                tournamentId={tournamentId}
                isOwner={isOwner}
                isAdmin={isAdmin}
                setStandings={setStandings}
              />
            ))}
          </>
        )}
      </div>
      <div className="standings-add-standing">
        {isOpen ? (
          <>
            <select
              value={competitorId}
              onChange={(e) => setCompetitorId(e.target.value)}
              required
            >
              <option value="">Select a Competitor</option>
              {tournament.competitors.map(competitor => (
                <option key={competitor.id} value={competitor.id}>{competitor.user.username}</option>
              ))}
            </select>
            <input
              type="number"
              placeholder="points"
              value={points}
              onChange={(e) => setPoints(e.target.value)}
              required
            />
            <button onClick={handleAdd} disabled={isSubmitting}>
              {isSubmitting ? 'Adding...' : 'Confirm New Standing'}
            </button>
            <button onClick={(e) => setIsOpen(false)}>Cancel</button>
            {error && <p role="alert">{error}</p>}
          </>
        ) : (
          <>
            {(isOwner || isAdmin) && (
              <button onClick={()=> setIsOpen(true)}>Add a Standing</button>
            )}
          </>
        )}
      </div>
    </>
  )
}

export default Standings;