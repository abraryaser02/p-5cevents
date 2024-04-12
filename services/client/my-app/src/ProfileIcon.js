import React from 'react';
import './App.css'; // Import CSS for styling the profile icon

const ProfileIcon = ({ imageUrl }) => {
  return (
    <div className="profile-icon-container">
      <img src={imageUrl} alt="" className="profile-icon" />
    </div>
  );
};

export default ProfileIcon;
