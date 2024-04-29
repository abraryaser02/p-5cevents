// Modify ProfileIcon component
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useUser } from './UserContext'; // Adjust the import path as needed

import './App.css'; // Import CSS for styling the profile icon

const ProfileIcon = ({ imageUrl }) => {
  const [showPopup, setShowPopup] = useState(false);
  const { logoutUser } = useUser();
  const navigate = useNavigate();

  const togglePopup = () => {
    setShowPopup(!showPopup);
  };

  const handleLogout = () => {
    logoutUser();
    navigate('/login'); // Redirect to login page after logout
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
            <li onClick={handleLogout} >Log Out</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default ProfileIcon;
