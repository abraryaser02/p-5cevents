import React from 'react';
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
          <li><a href="/EventPage.js">Events</a></li>
          <li><a href="/CalendarPage.js">Calendar</a></li>
          <li><a href="/MapPage.js">Map</a></li>
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
