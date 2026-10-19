import { Link } from 'react-router-dom'

function TournamentListItem({ event, tournament }) {
  return (
    <div className="row">
      <Link to={`/events/${event.id}/tournaments/${tournament.id}`}>
        <h2>{tournament.name}</h2>
      </Link>
      <p>({tournament.platform})</p>
    </div>
  )
}

export default TournamentListItem;