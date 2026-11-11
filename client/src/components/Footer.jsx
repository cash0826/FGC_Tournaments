import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import '../styles/footer.css';

function Footer() {
  const { user } = useAuth();
  const roles = ["admin", "host"]  

  return (
    <footer>
      {/* Content */}
      <div className="footer-content-section">
        {user ? (
          <div className="footer-column" id="profile-column">
            <p className="column-title">Profile</p>
            <div className="links">
              <Link label="My Profile" to="/profile">{user.first_name}</Link>
            </div>
          </div>
        ) : (
          <></>
        )}
        <div className="footer-column" id="website-column">
          <p className="column-title">Website Navigation</p>
          <div className="links">
            <Link label="About" to="/about">About</Link>
            <Link label="Events" to="/">Events</Link>
            <Link label="Contact" to="/#contact">Become a Sponsor</Link>
          </div>
        </div>

        <div className="footer-column" id="host-column">
          <p className="column-title">Host Navigation</p>
          <div className="links">
            <Link label="Host Dashboard" to="/host_dashboard">Host Dashboard</Link>
            <Link label="Your Events" to="/your_events">Your Events</Link>
            <Link label="New Event" to="/new_event">New Event</Link>
          </div>
        </div>

        <div className="footer-column" id="admin-column">
          <p className="column-title">Admin Navigation</p>
          <div className="links">
            <Link label="Admin Dashboard" to="/admin_dashboard">Admin Dashboard</Link>
            <Link label="New Sponsor" to="/new_sponsor">New Sponsor</Link>
            <Link label="Update Contact Info" to="/update_contact_form">Update Contact Information</Link>
          </div>
        </div>

      </div>

      {/* Footer-Footer */}
      <div className="footer-footer">
        <div className="footer-bottom" id="bottom-left">
          <a>Partner Sites:</a>
        </div>

        <div className="footer-bottom" id="bottom-center">
          <a>Terms of Use - Code of Conduct</a>
        </div>

        <div className="footer-bottom" id="bottom-right">
          <a>Social Sites:</a>
        </div>
      </div>
    </footer>
  )
}

export default Footer;