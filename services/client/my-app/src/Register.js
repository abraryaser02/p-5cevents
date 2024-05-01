import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Login from './Login';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const navigate = useNavigate();

  const handleRegister = (e) => {
    e.preventDefault();
    // Placeholder for registration logic
    if (password !== passwordConfirm) {
      alert('Passwords do not match.');
      return;
    }
    console.log('Registering with', email, password);
    
    // Prepare the registration data
    const userData = {
      email: email,
      password: password
    };

    // Send a POST request to the backend login endpoint
    fetch('http://localhost:5001/create_user', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Account creation successful!');
        navigate('/login'); // Navigate to events page upon successful login
      } else {
        alert(data.message || 'Invalid email or password'); // Use message from backend or a default message
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Failed to create a account');
    });
  };

  const handleLogin = (e) => {
    e.preventDefault();
    navigate('/login'); // Use navigate to go to the register page
  }

  return (
    <div className="login-container">
      <h2>Register</h2>
      <form className="login-form" onSubmit={handleRegister}>
        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <label>
          Confirm Password:
          <input
            type="password"
            value={passwordConfirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
            required
          />
        </label>
        <button type="submit">Register</button>
      </form>
      <button type="login" onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Register;
