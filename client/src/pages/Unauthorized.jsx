import NavBar from '../components/NavBar'

function Unauthorized() {
  return (
    <>
      <header>
        <NavBar/>
      </header>
      <h1>Unauthorized</h1>
      <p>You do not have permission to view this page.</p>
    </>
  );
}

export default Unauthorized;

