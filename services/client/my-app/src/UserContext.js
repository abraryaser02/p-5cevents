import React, { createContext, useContext, useState } from 'react';

const UserContext = createContext({ user: null, isAuthenticated: false});

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const loginUser = (userData) => {
        setUser(userData);
        setIsAuthenticated(true);
    };

    const logoutUser = () => {
        setUser(null);
        setIsAuthenticated(false);
    };

    return (
        <UserContext.Provider value={{ user, isAuthenticated, loginUser, logoutUser }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);
