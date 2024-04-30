import React from 'react';
import { Link } from 'react-router-dom';
import './App.css'; // Import the app.css file
import logo from './logo-1.png';

function AboutPage() {
  return (
    <div className="App">
      <div className="top-bar">
        <h1>About</h1>
      </div>
      <div className="left-bar">
      <img src={logo} alt="Logo" id="logo1" /> {/* Include the logo */}
        <ul>
        <li><Link to="/events">Events</Link></li>
        <li><Link to="/map">Map</Link></li>
        <li><Link to="/about">About</Link></li>
        </ul>
      </div>
      <header className="About-header">
        <h2>AI-Powered Event Planner for 5Cs Students</h2>
        <p>P-5cEvents is a web app designed to organize on-campus events and student calendars, offering comprehensive event scheduling assistance including maps and g-Cal integration. We will use imaplib to scrape Outlook/Gmail email content from various servers across campus to populate this web app but users can also submit the event details directly on this website. Beyond scheduling, p-5cEvents enhances user experience with an AI-driven recommendation system, employing natural language processing to tailor event suggestions based on individual preferences and historical attendance.</p>
      </header>
      <header className="About-team">
        <h2>Meet the team</h2>
        <h3>Project Management</h3>
        <p>Abrar Yaser POM '25</p>
        <p>Sae Furukawa POM '25</p>

        <h4>Members</h4>
        <p>David Wong POM '25</p>
        <p>Dylan O'Connor POM '26</p>
        <p>Landen Isacson POM '27</p>
        <p>Oncel Aldanmaz HMC '26</p>
        <p>Sadhvi Narayanan HMC '27</p>
        <p>Sumi Vora POM '25</p>
        <p>Yunju Song POM '26</p>
      </header>
    </div>
  );
}

export default AboutPage;
