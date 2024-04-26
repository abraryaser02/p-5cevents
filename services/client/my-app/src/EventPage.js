

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
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [location, setLocation] = useState('');
  const [description, setDescription] = useState('');
  const [organization, setOrganization] = useState('');
  const [contactInformation, setContactInformation] = useState('');
  const [registrationLink, setRegistrationLink] = useState('');
  const [keywords, setKeywords] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [events, setEvents] = useState([]);

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
      start_time: startTime,
      end_time: endTime,
      location: location,
      description: description,
      organization: organization,
      contact_information: contactInformation,
      registration_link: registrationLink,
      keywords: keywords.split(',')  // Assuming keywords as comma-separated values
    };
    // Call the function to post event data
    console.log(eventData);
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
            // Updated form fields...
            <label>Event Name:
              <input type="text" value={eventName} onChange={(e) => setEventName(e.target.value)} required />
            </label>
            <label>Start Time:
              <input type="time" value={startTime} onChange={(e) => setStartTime(e.target.value)} required />
            </label>
            <label>End Time:
              <input type="time" value={endTime} onChange={(e) => setEndTime(e.target.value)} required />
            </label>
            <label>Location:
              <input type="text" value={location} onChange={(e) => setLocation(e.target.value)} required />
            </label>
            <label>Description:
              <textarea value={description} onChange={(e) => setDescription(e.target.value)} required />
            </label>
            <label>Organization:
              <input type="text" value={organization} onChange={(e) => setOrganization(e.target.value)} required />
            </label>
            <label>Contact Information:
              <input type="text" value={contactInformation} onChange={(e) => setContactInformation(e.target.value)} required />
            </label>
            <label>Registration Link:
              <input type="url" value={registrationLink} onChange={(e) => setRegistrationLink(e.target.value)} required />
            </label>
            <label>Keywords:
              <input type="text" value={keywords} onChange={(e) => setKeywords(e.target.value)} placeholder="Comma-separated" />
            </label>
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
              {/* Use Link component for event name */}
              <Link to={`/eventdetail/${event.id}`}>
                <h3>{event.name}</h3>
              </Link>
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
