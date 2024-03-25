// Import necessary dependencies from React
import React, { useState } from 'react';

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
    // Here you can store or process the event data
    console.log('Event submitted:', { eventName, date, location, description });
    // Reset the form fields
    setEventName('');
    setDate('');
    setLocation('');
    setDescription('');
    // Set submitted state to true
    setSubmitted(true);
    // Close the popup after submission (change this part to have "thanks for submitting" screen)
    setShowCreateEventPopup(false);
  };

  // Return JSX for rendering
  return (
    <div className="App">
      {/* Top bar */}
      <div className="top-bar">
        <h1>Events</h1>
      </div>

      {/* Left bar */}
      <div className="left-bar">
        <img src={logo} alt="Logo" id="logo1" /> {/* Include the logo */}
        <ul>
          <li><a href="/EventPage.js">Events</a></li>
          <li><a href="/CalendarPage.js">Calendar</a></li>
          <li><a href="/MapPage.js">Map</a></li>
        </ul>
        {/* Button on top of the left bar */}
        <button onClick={toggleCreateEventPopup}>Create Event</button>
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
    </div>
  );
}

// Export the EventPage component
export default EventPage;
