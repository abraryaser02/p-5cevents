import React from 'react';
import './App.css'; // Import the app.css file
import logo from './logo-1.png';

function CalendarPage() {
  return (
    <div className="App">
      <div className="top-bar">
        <h1>Calendar</h1>
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
        <h2>Calendar Page</h2>
        <p>This is the calendar page content.</p>
      </header>
    </div>
  );
}

export default CalendarPage;
