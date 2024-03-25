import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import CalendarPage from './CalendarPage';
import EventPage from './EventPage';
import MapPage from './MapPage';
import NotFoundPage from './NotFoundPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route exact path="/" element={<EventPage />} /> {/* Default route */}
          <Route path="/Events" element={<EventPage />} />
          <Route path="/Calendar" element={<CalendarPage />} />
          <Route path="/Map" element={<MapPage />} />
          <Route path="*" element={<NotFoundPage />} /> {/* This route will be matched for any other route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
