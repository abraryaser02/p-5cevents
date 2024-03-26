// Import React and useState hook from the 'react' package
import React, { useState } from 'react';

// Import Link component from 'react-router-dom' package for navigation
import { Link } from 'react-router-dom';

// Import CSS file for styling
import './App.css'; // Import the app.css file

// Import logo image
import logo from './logo-1.png';

// Define the EventPage component
function EventPage() {
  // Define state variables using the useState hook
  const [showCreateEventPopup, setShowCreateEventPopup] = useState(false);
  const [eventName, setEventName] = useState('');
  const [date, setDate] = useState('');
  const [location, setLocation] = useState('');
  const [description, setDescription] = useState('');
  const [submitted, setSubmitted] = useState(false);

  // Function to toggle the event creation popup
  const toggleCreateEventPopup = () => {
    setShowCreateEventPopup(!showCreateEventPopup);
  };

  // Function to handle event submission
  const handleSubmitEvent = (e) => {
    e.preventDefault();
    // Log event data to the console
    console.log('Event submitted:', { eventName, date, location, description });
    // Reset form fields
    setEventName('');
    setDate('');
    setLocation('');
    setDescription('');
    // Set submitted state to true
    setSubmitted(true);
    // Close the popup after submission
    setShowCreateEventPopup(false);
  };

  // Return JSX for rendering
  return (
    <div className="App">
      {/* Navigation bar */}
      <div className="top-bar">
        <h1>Events</h1>
      </div>

      {/* Left bar */}
      <div className="left-bar">
        {/* Logo */}
        <img src={logo} alt="Logo" id="logo1" />
        <ul>
          {/* Navigation links */}
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
            {/* Event form inputs */}
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
            {/* Submit button */}
            <button type="submit">Submit Event</button>
          </form>
          {/* Confirmation message and button */}
          {submitted && (
            <div>
              <p>Thank you for submitting your event.</p>
              <button onClick={() => setSubmitted(false)}>Create Another Event</button>
            </div>
          )}
        </div>
      )}

      {/* Page header */}
      <header className="App-header">
        <h2>Events Page</h2>
        <p>This is the events page content.</p>
      </header>
    </div>
  );
}

// Export the EventPage component
export default EventPage;
