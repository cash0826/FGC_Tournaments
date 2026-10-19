import { useState, useEffect } from "react";
import { listEvents } from "../services/eventService";
import EventItem from "../components/eventitem/EventItem";
import NavBar from '../components/NavBar'
import img from "../assets/banner-img.png";

function Home() {
  const [events, setEvents] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect( ()=> {
    listEvents()
      .then((data) => setEvents( data.events || [] ))
      .catch((err) => setError(err.message || 'Unable to load events'))
      .finally(() => setIsLoading(false))
  }, []);

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (events.message) return <p>{events.message}</p>;

  return (
    <>
      <header>
        <NavBar/>
      </header>
      <main>
        <section>
          <div className="inner-banner">
            <div className="container">
              <div className="row">
                <div className="banner-img">
                  <img src={img}/>
                </div>
                <div className="banner-headers">
                  <h1>Join our upcoming events!</h1>
                  <h2>Street Fighter 6, Marvel Tokon, Fatal Fury and more...</h2>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section className="upcoming-games">
          <div className="container">
            {events.map((event) => (
              <EventItem 
                key={event.id}
                event={event}
              />
          ))}
          </div>
        </section>
      </main>
    </>
  )
}

export default Home;