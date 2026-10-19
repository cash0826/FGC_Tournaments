import { Routes, Route } from "react-router-dom"
// Pages
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Profile from "./pages/Profile";
import Unauthorized from "./pages/Unauthorized";
import CreateEvent from "./pages/CreateEvent";
import AddTournament from "./pages/AddTournament";
import EventDetails from "./pages/EventDetails";
import TournamentDetails from "./pages/TournamentDetails";
import Register from "./pages/Register";
import Matches from "./pages/Matches";
import Standings from "./pages/Standings";
import Bracket from "./pages/Bracket";
import NotFound from "./pages/NotFound";

// Components
import Footer from './components/Footer'
import ProtectedRoute from "./components/ProtectedRoute";
import RequireRole from "./components/RequireRole";

// Layout
import EventLayout from "./layouts/EventLayout";

function App() {

  return (
    <>
      {/* Public Routes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/unauthorized" element={<Unauthorized />} />

        {/* Protected - any authenticated user */}
        <Route element={<ProtectedRoute/>}>
          <Route path="/profile" element={<Profile />} />
        </Route>

        {/* Host or admin */}
        <Route element={<RequireRole roles={["host", "admin"]} />}>
          <Route path="/events/create" element={<CreateEvent /> } />
          <Route path="/events/:eventId/tournaments/create" element={<AddTournament/>}></Route>
        </Route>

        {/* Public. Event-Scoped Routes */}
        <Route path="/events/:eventId" element={<EventLayout />} >
          <Route index element={<EventDetails />} />
          <Route path="tournaments/:tournamentId" element={<TournamentDetails />} />
          <Route path="tournaments/:tournamentId/register" element={<Register />} />
          <Route path="tournaments/:tournamentId/matches" element={<Matches />} />
          <Route path="tournaments/:tournamentId/standings" element={<Standings />} />
          <Route path="tournaments/:tournamentId/bracket" element={<Bracket />} />
        </Route>

        <Route path="*" element={<NotFound/> }/>
      </Routes>

      <Footer/>
    </>
  )
}

export default App;
