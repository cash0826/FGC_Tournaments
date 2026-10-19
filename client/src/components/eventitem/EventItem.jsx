import { Link } from 'react-router-dom'
import { formatLongDate } from "../../utils/dateUtils"

function EventItem({ event }) {
  return (
    <div className="row">
      <Link to={`/events/${event.id}`}><h2>{event.name}</h2></Link>
      <p>{formatLongDate(event.start)}</p>
      <p>{event.location}</p>
    </div>
  )
}

export default EventItem;