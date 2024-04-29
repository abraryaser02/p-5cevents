import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useUser } from './UserContext'; // adjust path as needed

function ProtectedRoute({ children }) {
    const { isAuthenticated } = useUser();
    const location = useLocation();

    if (!isAuthenticated) {
        // Redirect them to the /login page, but save the current location they were trying to go to
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    return children;
}

export default ProtectedRoute;  // Ensure it's exported as default