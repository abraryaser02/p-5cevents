import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import AboutPage from './AboutPage';
import CalendarPage from './CalendarPage';
import EventDetailPage from './EventDetail';
import EventPage from './EventPage';
import LoginPage from './Login';
import MapPage from './MapPage';
import NotFoundPage from './NotFoundPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route exact path="/" element={<LoginPage />} /> {/* Default route */}
          <Route path="/Events" element={<EventPage />} />
          <Route path="/Calendar" element={<CalendarPage />} />
          <Route path="/Map" element={<MapPage />} />
          <Route path='/About' element={<AboutPage />} />
          <Route path='/Login' element={<LoginPage />} />
          <Route path='/EventDetail' element={<EventDetailPage />} />
          <Route path="*" element={<NotFoundPage />} /> {/* This route will be matched for any other route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
