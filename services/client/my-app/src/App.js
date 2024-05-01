import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import AboutPage from './AboutPage';
import CalendarPage from './CalendarPage';
import EventDetailPage from './EventDetail';
import EventPage from './EventPage';
import LoginPage from './Login';
import Register from './Register';
import MapPage from './MapPage';
import NotFoundPage from './NotFoundPage';
import { UserProvider } from './UserContext';
import ProtectedRoute from './ProtectedRoute'; // Make sure this is imported

function App() {
  return (
    <UserProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<LoginPage />} /> {/* Consider redirecting to a more appropriate default route */}
            <Route path="/events" element={
              <ProtectedRoute>
                <EventPage />
              </ProtectedRoute>
            } />
            <Route path="/calendar" element={
              <ProtectedRoute>
                <CalendarPage />
              </ProtectedRoute>
            } />
            <Route path="/map" element={
              <ProtectedRoute>
                <MapPage />
              </ProtectedRoute>
            } />
            <Route path="/about" element={
              <ProtectedRoute>
                <AboutPage />
              </ProtectedRoute>
            } />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<Register />} />
            <Route path="/eventdetail" element={
              <ProtectedRoute>
                <EventDetailPage />
              </ProtectedRoute>
            } />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </div>
      </Router>
    </UserProvider>
  );
}

export default App;
