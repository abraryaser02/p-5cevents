import React from 'react';
import { Link } from 'react-router-dom';
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
        <li><Link to="/events">Events</Link></li>
        <li><Link to="/calendar">Calendar</Link></li>
        <li><Link to="/map">Map</Link></li>
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
