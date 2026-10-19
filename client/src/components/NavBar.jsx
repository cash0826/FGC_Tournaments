import { NavLink } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import logo from "../assets/logo.png";
import '../styles/navbar.css';

function NavBar() {
  const { user } = useAuth();
  const roles = ["admin", "host"]  

  function getCreateEvent() {
    if (user) {
      const hasRole = user.roles.some(userRole => roles.includes(userRole.role?.name))
      return hasRole ? <NavLink label="Create_Event" to="/events/create">Create Event</NavLink> : null
    }
  }

  return (
    <nav>
      <div className="container">

        {/* Logo */}
        <a className="navbar-brand-logo" href="/">
          <img src={logo}></img>
        </a>

        {/* Navbar Toggler */}
        <button className="navbar-toggler" type="button">
          <span className="icon-bar"></span>
          <span className="icon-bar"></span>
          <span className="icon-bar"></span>
        </button>

        {/* Nav Links */}
        <div className="navbar-links">
        {user ? (
          <>
            <NavLink label="Home" to="/" >Home</NavLink>
            <NavLink label="Profile" to="/profile" >Profile</NavLink>
            {getCreateEvent()}
          </>
        ) : (
          <>
            <NavLink label="Home" to="/" >Home</NavLink>
            <NavLink label="Login" to="/login">Login</NavLink>
            <NavLink label="Signup" to="/signup">Signup</NavLink>
          </>
        )}
        </div>

      </div>
    </nav>
  )
}

export default NavBar;