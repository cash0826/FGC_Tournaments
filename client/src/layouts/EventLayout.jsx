import { useState, useEffect } from "react";
import { useParams, Outlet } from "react-router-dom";
import { getEvent } from "../services/eventService"
import BackButton from "../components/BackButton";
import NavBar from '../components/NavBar'

function EventLayout() {
  const { eventId } = useParams();
  const [event, setEvent] = useState(null)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(()=> {
    getEvent(eventId)
      .then((fetchedEvent) => setEvent(fetchedEvent))
      .catch((err) => setError(err.message || 'Unable to load event details'))
      .finally(() => setIsLoading(false))
  }, [eventId])

  // isLoading and error state should live in layout. Child routes should never fetch the event
  // index element (EventDetails) should assume event is already loaded and event exists
  
  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!event) return <p>Event not found.</p>;

  return (
    <>
      <header>
        <NavBar/>
      </header>
      <Outlet context={{ event, setEvent }} />
      <div className="back-btn-container">
        <BackButton/>
      </div>
    </>
  )
}

export default EventLayout;