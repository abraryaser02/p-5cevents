import React from 'react';
import { Link } from 'react-router-dom';
import './App.css'; // Import the app.css file
import logo from './logo-1.png';

function MapPage() {
  return (
    <div className="App">
      <div className="top-bar">
        <h1>Map</h1>
      </div>
      <div className="left-bar">
      <img src={logo} alt="Logo" id="logo1" /> {/* Include the logo */}
        <ul>
        <li><Link to="/events">Events</Link></li>
        <li><Link to="/map">Map</Link></li>
        <li><Link to="/about">About</Link></li>
        </ul>
      </div>
      <header className="App-header">
        <h2>Map Page</h2>
        <p>This is the map page content.</p>
      </header>
    </div>
  );
}

export default MapPage;
