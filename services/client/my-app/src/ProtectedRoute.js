import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useUser } from './UserContext'; // adjust path as needed

function ProtectedRoute({ children }) {
    // const { isAuthenticated } = useUser();
    // const location = useLocation();

    const { user } = useUser();
    if (!user) {
        // Redirect them to the /login page, but save the current location they were trying to go to
        return <Navigate to="/login" />;
    }

    return children;
}

export default ProtectedRoute;  // Ensure it's exported as default