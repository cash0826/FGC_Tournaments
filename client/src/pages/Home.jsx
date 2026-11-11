import { useState, useEffect } from "react";
import { listEvents } from "../services/eventService";
import EventItem from "../components/eventitem/EventItem";
import '../styles/home.css';
import dagger from "../assets/logo-icon-black.svg";

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
      <main>
        <section className="hero-section">
          <div className="display-text">
            <p className="display">dagger</p>
            <div className="subtitle">
              <p>A website based in Costa Rica that joins year-round, fighting-game tournaments to one source: dagger.</p>
              <p>Learn more about our upcoming events below.</p>
            </div>
          </div>
        </section>

        <section className="main-events-section">
          <div className="top-banner">
            <img src={dagger}></img>
            <p>dagger</p>
            <img src={dagger}></img>
            <p>dagger</p>
            <img src={dagger}></img>
          </div>

          <div className="title">
            <h1>Upcoming Events:</h1>
          </div>

          <div className="list">
            <div className="row-1-card"> {/* 1 card under row-1 */}
              <div className="details">
                <h3>Nov 3</h3>
                <h3>San Pedro</h3>
              </div>
              <h2>Fight for Glory</h2>
            </div>

            <div className="row-2"> {/* 3 cards under row-2 */}
              <div className="card" id="card-2">
                <div className="details">
                  <h3>Dec 12</h3>
                  <h3>Coronado</h3>
                </div>
                <h2>Coliseum Nights</h2>
              </div>
              <div className="card" id="card-3">
                <div className="details">
                  <h3>Jan 10</h3>
                  <h3>Barreal</h3>
                </div>
                <h2>Casual Nights</h2>
              </div>
              <div className="card" id="card-4">
                <div className="details">
                  <h3>Mar 8</h3>
                  <h3>San Pedro</h3>
                </div>
                <h2>Tekken League</h2>
              </div>
            </div>
          </div>
        </section>

        <section className="past-winners-section">
          <div className="display-text">
            <p className="display">hall of fame</p>
            <div className="subtitle">
              <p>All of our sharpest hall of famers, listed from past events.</p>
            </div>
            <button type="button" >View Champions</button>
          </div>
        </section>

        <section id="contact">
          <div className="top-banner">
            <img src={dagger}></img>
            <p>dagger</p>
            <img src={dagger}></img>
            <p>dagger</p>
            <img src={dagger}></img>
          </div>

          <div className="title">
            <h1>Become a Sponsor:</h1>
          </div>

          <div className="form"> {/* Form */ }
            <div className="form-inputs">
              <div className="input">
                <p>Full Name</p> {/*Placeholder text */}
              </div>

              <div className="input">
                <p>Email</p> {/*Placeholder text */}
              </div>

              <div className="input" id="text-input">
                <p>Message</p> {/*Placeholder text */}
              </div>

              <button type="button" >Submit</button>
            </div>

          </div>
        </section>

      </main>
    </>
  )
}

export default Home;