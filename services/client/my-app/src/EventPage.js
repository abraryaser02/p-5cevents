import React, { useState } from 'react';
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
    // Here you can store or process the event data
    console.log('Event submitted:', { eventName, date, location, description });
    // Reset the form fields
    setEventName('');
    setDate('');
    setLocation('');
    setDescription('');
    // Set submitted state to true
    setSubmitted(true);
    // Close the popup after submission (optional)
    setShowCreateEventPopup(false);
  };

  return (
    <div className="App">
      <div className="left-bar">
        <img src={logo} alt="Logo" id="logo1" /> {/* Include the logo */}
        <ul>
          <li><a href="/EventPage.js">Events</a></li>
          <li><a href="/CalendarPage.js">Calendar</a></li>
          <li><a href="/MapPage.js">Map</a></li>
          <li><button onClick={toggleCreateEventPopup}>Create Event</button></li>
        </ul>
      </div>
      <div class="dropdown">
        <button class="dropbtn">Create</button>
        <div class="dropdown-content">
            <a href="#">Link 1</a>
            <a href="#">Link 2</a>
            <a href="#">Link 3</a>
        </div>
      </div>

      <header className="App-header">
        <h1>Events</h1>
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
      </header>
    </div>
  );
}

export default EventPage;
