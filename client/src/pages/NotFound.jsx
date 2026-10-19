import NavBar from '../components/NavBar'

function NotFound() {
  return (
    <>
      <header>
        <NavBar/>
      </header>
      <h1>Page Not Found</h1>
      <p>The page you're looking for doesn't exist or may have been moved.</p>
    </>
  );
}

export default NotFound;
