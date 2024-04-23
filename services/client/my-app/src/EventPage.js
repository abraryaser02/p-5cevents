

//curl -X POST http://localhost:5001/create_event -H "Content-Type: application/json" -d "{\"name\":\"Event Name\",\"description\":\"Event Description\",\"location\":\"Event location\",\"time\":\"2024-03-22T15:30:00\",\"organization\":\"Event Organization\"}"


// Import React and useState hook from the 'react' package
import React, { useEffect, useState } from 'react';

// Import Link component from 'react-router-dom' package for navigation
import { Link } from 'react-router-dom';

// Import CSS file for styling
import './App.css'; // Import the app.css file

// Import logo image
import logo from './logo-1.png';

// Import ProfileIcon component
import ProfileIcon from './ProfileIcon';

// Import profile image 
import profileimg from './profileimg.png';

// Define the EventPage component
function EventPage() {
  // Define state variables using the useState hook
  const [showCreateEventPopup, setShowCreateEventPopup] = useState(false);
  const [eventName, setEventName] = useState('');
  const [date, setDate] = useState('');
  const [location, setLocation] = useState('');
  const [description, setDescription] = useState('');
  const [organization, setOrganizatoin] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [events, setEvents] = useState([]); // State to hold fetched events

  //fetching data from the backend
  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch('http://localhost:5001/all_events'); 
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setEvents(data); // Store fetched data in state
      } catch (error) {
        console.error('There was a problem fetching the event data:', error);
      }
    };

    fetchEvents();
  }, []); 

  // Function to post event data to the backend
  const postEventData = async (eventData) => {
    try {
      const response = await fetch('http://localhost:5001/create_event', { // wrong endpoint
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      } else {
        console.log('Event created successfully:', await response.json());
        setSubmitted(true);
        // Reset form fields
        setEventName('');
        setDate('');
        setLocation('');
        setDescription('');
        setOrganizatoin('');
        setShowCreateEventPopup(false);
      }
    } catch (error) {
      console.error('Error submitting event:', error);
    }
  };


  // Function to toggle the event creation popup
  const toggleCreateEventPopup = () => {
    setShowCreateEventPopup(!showCreateEventPopup);
  };

  const handleSubmitEvent = (e) => {
    e.preventDefault();
    const eventData = {
      name: eventName,
      date: date,
      location: location,
      description: description,
      organization: organization,
    };
    // Call the function to post event data
    postEventData(eventData);
    setShowCreateEventPopup(false); // Close the popup after submission
  };


  // Return JSX for rendering
  const imageUrl = profileimg;
  return (
    <div className="App">
      {/* Navigation bar */}
      <div className="top-bar">
        <h1>Events</h1>
        {/* Profile icon */}
        <ProfileIcon imageUrl={imageUrl} />
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
          <li><Link to="/about">About</Link></li>
          <li><button type= "event-button" button onClick={toggleCreateEventPopup}>Create Event</button></li>
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
      <h2>Upcoming Events</h2>
      </header>

      <div className="events-list">
        <ul>
            {events.map(event => (
              <li key={event.id} className="event">
                <h3>{event.name}</h3>
                <p>Description: {event.description}</p>
                <p>Location: {event.location}</p>
                <p>Time: {new Date(event.time).toLocaleString()}</p>
                <p>Organization: {event.organization}</p>
              </li>
            ))}
          </ul>
      </div>
      
    </div>
  );
}

// Export the EventPage component
export default EventPage;
