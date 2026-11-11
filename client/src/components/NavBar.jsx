import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import logo from "../assets/logo.png";
import '../styles/navbar.css';

function NavBar() {
  const { user } = useAuth();
  const roles = ["admin", "host"]  

  // function getCreateEvent() {
  //   if (user) {
  //     const hasRole = user.roles.some(userRole => roles.includes(userRole.role?.name))
  //     return hasRole ? <NavLink label="Create_Event" to="/events/create">Create Event</NavLink> : null
  //   }
  // }

  return (
    <nav>
      {/* Logo */}
      <a className="logo" href="/">
        <img src={logo}></img>
      </a>

      {/* Header Links */}
      <div className="header-links">
        {user ? (
          <>
            <Link label="About" to="/about">About</Link>
            <Link label="Events" to="/">Events</Link>
            <a href="#contact">Contact</a>
            <Link label="My Profile" to="/profile">My Profile</Link>
            
          </>
        ) : (
          <>
            <Link label="About" to="/about" >About</Link>
            <Link label="Events" to="/" >Events</Link>
            <a href="/events#contact" >Contact</a>
          </>
        )}
      </div>

      {/* Buttons or Message */}
      <div className="header-auth-state">
        {user ? (
          <>
            <p>Welcome {user.name}!</p>
          </>
        ) : (
          <>
            <button type="button"><a href="/signup">Signup</a></button>
            <button type="button"><a href="/login">Login</a></button>
          </>
        )}
      </div>
    </nav>
  )
}

export default NavBar;