import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from react-router-dom
import './App.css'; // Import the app.css file

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  
  // Initialize useNavigate hook
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    // Figure out backend stuff! 
    // Use temporary email and password for now to do login for demo
    if (email === 'example@example.com' && password === 'password') {
      setIsLoggedIn(true);
      alert('Login successful!');
      // Go to events page when logged in for now, create separate homepage in the future(?)
      navigate('/events');
    } else {
      alert('Invalid email or password');
    }
  };

  return (
    <div className="login-container"> {/* Add the login-container class here */}
      <h2>Login</h2>
      <form className="login-form" onSubmit={handleLogin}>
        <label>
          Email:
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label>
          Password:
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
