import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './App.css'; // Import the app.css file
import logo from './logo-1.png';

function EventPage() {
  const [showCreateEventPopup, setShowCreateEventPopup] = useState(false);
  const [eventName, setEventName] = useState('');
  const [date, setDate] = useState('');
  const [location, setLocation] = useState('');
  const [description, setDescription] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const toggleCreateEventPopup = () => {
    setShowCreateEventPopup(!showCreateEventPopup);
  };

  const handleSubmitEvent = (e) => {
    e.preventDefault();
    console.log('Event submitted:', { eventName, date, location, description });
    setEventName('');
    setDate('');
    setLocation('');
    setDescription('');
    setSubmitted(true);
    setShowCreateEventPopup(false);
  };

  return (
    <div className="App">
      <div className="top-bar">
        <h1>Events</h1>
      </div>
      <div className="left-bar">
        <img src={logo} alt="Logo" id="logo1" />
        <ul>
        <li><Link to="/events">Events</Link></li>
        <li><Link to="/calendar">Calendar</Link></li>
        <li><Link to="/map">Map</Link></li>
          <li><button onClick={toggleCreateEventPopup}>Create Event</button></li>
        </ul>
      </div>
      {/* Event creation popup */}
      {showCreateEventPopup && (
        <div className="create-event-popup">
          <h2>Create Event</h2>
          <form onSubmit={handleSubmitEvent}>
            <label>
              Event Name:
              <input
                type="text"
                value={eventName}
                onChange={(e) => setEventName(e.target.value)}
                required
              />
            </label>
            <label>
              Date:
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
              />
            </label>
            <label>
              Location:
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                required
              />
            </label>
            <label>
              Description:
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </label>
            <button type="submit">Submit Event</button>
          </form>
          {submitted && (
            <div>
              <p>Thank you for submitting your event.</p>
              <button onClick={() => setSubmitted(false)}>Create Another Event</button>
            </div>
          )}
        </div>
      )}
      <header className="App-header">
      <h2>Events Page</h2>
        <p>This is the evnets page content.</p>
      </header>
    </div>
  );
}

export default EventPage;
