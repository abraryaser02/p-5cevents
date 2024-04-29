// Modify ProfileIcon component
import React, { useState } from 'react';
import './App.css'; // Import CSS for styling the profile icon

// Import Link component from 'react-router-dom' package for navigation
import { Link } from 'react-router-dom';

const ProfileIcon = ({ imageUrl }) => {
  const [showPopup, setShowPopup] = useState(false);

  const togglePopup = () => {
    setShowPopup(!showPopup);
  };

  return (
    <div className="profile-icon-container">
      {/* Clickable profile icon */}
      <img src={imageUrl} alt="" className="profile-icon" onClick={togglePopup} />
      {/* Popup container */}
      {showPopup && (
        <div className="popup-container">
          <ul>
            <li>My Events</li>
            <li>Liked Events</li>
            <li><Link to="/login">Log Out</Link></li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default ProfileIcon;
