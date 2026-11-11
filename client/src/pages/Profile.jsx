import { useAuth } from "../hooks/useAuth";
import { useState } from "react";
import { updateProfile } from "../services/authService";
import NavBar from '../components/NavBar'

function Profile() {
  const { user, setUser, logout, isLoading } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    email: '',
    username: '',
    full_name: '',
    bio: '',
    profile_pic_url: '',
    contact_number: ''
  })

  // Toggle inline editing
  function startEditing() {
    setError('')
    setForm({
      email: user.email,
      username: user.username,
      full_name: user.full_name,
      bio: user.bio,
      profile_pic_url: user.profile_pic_url,
      contact_number: user.contact_number
    })
    setIsEditing(true)
  }

  // Update
  async function handleSave(e) {
    e.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      const updated = await updateProfile(user.id, form)
      setUser(updated)
      setIsEditing(false)
    } catch (err) {
      setError(err.message || 'Unable to update profile')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) return <p>Loading...</p>;

  return (
    <>
      <header>
        <NavBar/>
      </header>
      
      {isEditing ? (
        <>
          <section>
            <div className="form-container">
              <div className="row-header">
                <h1>Profile</h1>
              </div>
              <div className="row-form">
                <form>
                  <input
                    placeholder="Profile Picture URL"
                    type="url"
                    value={form.profile_pic_url}
                    onChange={(e) => setForm({...form, profile_pic_url: e.target.value})}
                  />
                  <input
                    placeholder="Username"
                    value={form.username}
                    onChange={(e) => setForm({...form, username: e.target.value})}
                  />
                  <input
                    placeholder="Name to go by"
                    value={form.full_name}
                    onChange={(e) => setForm({...form, full_name: e.target.value})}
                  />
                  <input
                    placeholder="Email"
                    type="email"
                    value={form.email}
                    onChange={(e) => setForm({...form, email: e.target.value})}
                    required
                  />
                  <input
                    placeholder="Phone number to contact"
                    type="tel"
                    value={form.contact_number}
                    onChange={(e) => setForm({...form, contact_number: e.target.value})}
                  />
                  <textarea
                    placeholder="Biography"
                    value={form.bio}
                    onChange={(e) => setForm({...form, bio: e.target.value})}
                  />
                  <button onClick={handleSave} disabled={isSubmitting}>
                    {isSubmitting ? 'Saving...' : 'Save'}
                  </button>
                  <button onClick={() => setIsEditing(false)}>Cancel</button>
                  {error && <p role="alert">{error}</p>}
                </form>
              </div>
            </div>
          </section>
        </>
      ) : (
        <>
          <section>
            <div className="profile">
              <div className="container">
                <div className="row">
                  <div className="profile-img">
                    {user.profile_pic_url ? (
                      <>
                        <img src={user.profile_pic_url} alt={user.username}></img>
                        <h2>{user.full_name}</h2>
                      </>
                      ) : (
                        <>
                          <p>No image</p>
                          <p>{user.full_name}</p>
                        </>
                    )}
                  </div>
                </div>

                <div className="row">
                  <div>
                    <div className="profile-details">
                      <h3>Username:</h3><p>{user.username}</p>
                    </div>
                    <div className="profile-details">
                      <h3>Email:</h3><p>{user.email}</p>
                    </div>
                    <div className="profile-details">
                      <h3>Phone:</h3><p>{user.contact_number}</p>
                    </div>
                    <div className="profile-details">
                      <h3>Bio:</h3><p>{user.bio}</p>
                    </div>
                    <button onClick={startEditing}>Edit Profile Details</button>
                    <button type="button" onClick={logout}>Log out</button>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </>
      )}
    </>
  )
}

export default Profile;