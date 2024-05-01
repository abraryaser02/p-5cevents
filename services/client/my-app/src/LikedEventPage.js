

//curl -X POST http://localhost:5001/create_event -H "Content-Type: application/json" -d "{\"name\":\"Event Name\",\"description\":\"Event Description\",\"location\":\"Event location\",\"time\":\"2024-03-22T15:30:00\",\"organization\":\"Event Organization\"}"


// Import React and useState hook from the 'react' package
import React, { useEffect, useState } from 'react';

import { useUser } from './UserContext';
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
function EventPage({}) {
  const { user: currentUser } = useUser();
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
  const [favoritedEvents, setFavoritedEvents] = useState(new Set());
  const [favoritedEventsData, setFavoritedEventDetails] = useState([]);
  console.log(currentUser.userId)

//   fetching data from the backend
  useEffect(() => {
    async function fetchData() {
      const eventsResponse = await fetch('http://localhost:5001/all_events');
      const eventsData = await eventsResponse.json();
      setEvents(eventsData);
    }
    fetchData();
  }, [currentUser]);

  useEffect(() => {
    async function fetchFavoritedEvents() {
      if (currentUser && currentUser.userId) {
        try {
          const response = await fetch(`http://localhost:5001/events_by_user/${currentUser.userId}`);
          if (response.ok) {
            const favoritedEventsData = await response.json();
            console.log('Favorited events:', favoritedEventsData);
            setFavoritedEventDetails(favoritedEventsData);
            const favoriteIds = new Set(favoritedEventsData.map(event => event.id));
            setFavoritedEvents(favoriteIds);
          } else {
            throw new Error('Failed to fetch favorited events');
          }
        } catch (error) {
          console.error('Error fetching favorited events:', error);
        }
      }
    }
    fetchFavoritedEvents();
  }, [currentUser]);
  
  // Toggle favorite status of an event
  const toggleFavorite = async (eventId) => {
    if (!currentUser || !currentUser.id) {
      alert("Please log in to favorite events.");
      return;
    }
  
    try {
      const response = await fetch('http://localhost:5001/toggle_user_event', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: currentUser.id, event_id: eventId })
      });
  
      if (response.ok) {
        const updatedFavoritedEvents = new Set(favoritedEvents);
        if (updatedFavoritedEvents.has(eventId)) {
          updatedFavoritedEvents.delete(eventId);
        } else {
          updatedFavoritedEvents.add(eventId);
        }
        setFavoritedEvents(updatedFavoritedEvents);
      } else {
        throw new Error('Failed to toggle favorite status');
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

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
  
  
  // Filter events based on the search query and key events
  const filteredEvents = events.filter(event => 
    (event.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    event.keywords.some(keyword => keyword.toLowerCase().includes(searchQuery.toLowerCase()))) &&
    (checkedKeywords.length === 0 || // If no keywords are checked, show all events
    checkedKeywords.some(keyword => event.keywords.includes(keyword)))
  );

  const favoritedEventsfilterd = favoritedEventsData.filter(event => 
    (event.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    event.keywords.some(keyword => keyword.toLowerCase().includes(searchQuery.toLowerCase()))) &&
    (checkedKeywords.length === 0 || // If no keywords are checked, show all events
    checkedKeywords.some(keyword => event.keywords.includes(keyword)))
  );

  // Return JSX for rendering
  const imageUrl = profileimg;
  return (
    <div className="App">
      {/* Navigation bar */}
      <div className="top-bar">
        <h1>Liked Events</h1>
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
          <li><Link to="/map">Map</Link></li>
          <li><Link to="/about">About</Link></li>
        </ul>
      </div>


      <div className="events-list">
        <ul>
          {favoritedEventsfilterd.map(event => (
            <li key={event.id} className="event">
              <Link to={`/eventdetail/${event.id}`}>
                <h3>{event.name}</h3>
              </Link>
              <button onClick={() => toggleFavorite(event.id)} className="favorite-button">
              {favoritedEvents.has(event.id) ? '★' : '☆'}
              </button>
              <p>Description: {event.description}</p>
              <p>Location: {event.location}</p>
              <p>Start Time: {new Date(event.start_time).toLocaleString()}</p>
              <p>End Time: {new Date(event.end_time).toLocaleString()}</p>
              <p>Organization: {event.organization}</p>
              <p>Contact Information: {event.contact_information}</p>
              <p>Registration Link: <a href={event.registration_link}>{event.registration_link}</a></p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

// Export the EventPage component
export default EventPage;