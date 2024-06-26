import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from react-router-dom
import './App.css'; // Import the app.css file
import { useUser } from './UserContext';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { loginUser } = useUser();  // Use loginUser function from context
  
  // Initialize useNavigate hook
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    // Figure out backend stuff! 
    // Use temporary email and password for now to do login for demo
    // Prepare the login data
    const loginData = {
      email: email,
      password: password
    };

    // Send a POST request to the backend login endpoint
    fetch('http://localhost:5001/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(loginData)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Login successful!');
        // Assume data contains the user's email and an id. Adjust according to actual API response.
        const userInfo = { email: data.email, userId: data.userId}; 
        console.log(data.userID)
        loginUser(userInfo);  // Use loginUser to set user data and authenticate
        sessionStorage.setItem('user', JSON.stringify(userInfo)); // Corrected to use userInfo
        navigate('/events'); // Navigate to events page upon successful login
      } else {
        alert(data.message || 'Invalid email or password'); // Use message from backend or a default message
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Failed to login');
    });
  };

  const handleRegister = (e) => {
    e.preventDefault();
    navigate('/register'); // Use navigate to go to the register page
  }

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
      <button type="register" onClick={handleRegister}>Register</button>

    </div>
  );
}

export default Login;
