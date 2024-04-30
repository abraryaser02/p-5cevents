

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
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilterPopup, setShowFilterPopup] = useState(false);
  const [checkedKeywords, setCheckedKeywords] = useState([]);

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
        setOrganization('');
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
  
    // Formatting the start and end times to combine date and time for correct datetime format
    const formattedStartTime = `${date}T${startTime}`;
    const formattedEndTime = `${date}T${endTime}`;
  
    const eventData = {
      name: eventName,
      date: date,
      start_time: formattedStartTime,
      end_time: formattedEndTime,
      location: location,
      description: description,
      organization: organization,
      contact_information: contactInformation,
      registration_link: registrationLink,
      keywords: keywords.split(',').map(keyword => keyword.trim()) // Converts comma-separated string to an array of trimmed strings
    };
  
    // Log to console or remove in production
    console.log(eventData);
    
    // Call the function to post event data to the backend
    postEventData(eventData);
    setShowCreateEventPopup(false); // Optionally close the popup after submission
  };

   // Filter events based on the search query
   const filteredEvents = events.filter(event => 
    event.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    event.keywords.some(keyword => keyword.toLowerCase().includes(searchQuery.toLowerCase()))
  );
  
  // Define the keywords for the filter
  const filter = ["keyword1", "keyword2", "keyword3"];

  // Function to handle toggling of checked keywords
  const handleKeywordCheckboxChange = (keyword) => {
    // If the keyword is already checked, remove it from the checkedKeywords array
    // If it's not checked, add it to the checkedKeywords array
    setCheckedKeywords(prevCheckedKeywords =>
      prevCheckedKeywords.includes(keyword)
        ? prevCheckedKeywords.filter(k => k !== keyword)
        : [...prevCheckedKeywords, keyword]
    );
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
            <label>Date:
              <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
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
      <div className="search-filter-container">
        {/* Search input */}
        <input
          className="search-input"
          type="text"
          placeholder="Search by name or keyword"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />

        {/* Filter button */}
        <button className="filter-button" onClick={() => setShowFilterPopup(prevState => !prevState)}>Filter</button>
      </div>
        {/* Filter popup container */}
        {showFilterPopup && (
          <div className="filter-popup">
            <ul>
              {/* Filter checkboxes */}
              {filter.map((keyword, index) => (
                <div key={index} className="filter-checkbox">
                  <input
                    type="checkbox"
                    checked={checkedKeywords.includes(keyword)}
                    onChange={() => handleKeywordCheckboxChange(keyword)}
                  />
                  <label>{keyword}</label>
                </div>
              ))}
            </ul>
          </div>
        )}
      </header>
      

      <div className="events-list">
        <ul>
          {filteredEvents.map(event => (
            <li key={event.id} className="event">
              <Link to={`/eventdetail/${event.id}`}>
                <h3>{event.name}</h3>
              </Link>
              <p>Description: {event.description}</p>
              <p>Location: {event.location}</p>
              <p>Start Time: {new Date(event.start_time).toLocaleString()}</p>
              <p>End Time: {new Date(event.end_time).toLocaleString()}</p>
              <p>Organization: {event.organization}</p>
              <p>Contact Information: {event.contact_information}</p>
              <p>Registration Link: <a href={event.registration_link}>{event.registration_link}</a></p>
              <p>Keywords: {event.keywords.join(', ')}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

// Export the EventPage component
export default EventPage;
