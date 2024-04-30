import React, { createContext, useContext, useState, useEffect} from 'react';

const UserContext = createContext({ user: null, isAuthenticated: false});

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(JSON.parse(sessionStorage.getItem('user')));

    const loginUser = (userData) => {
        sessionStorage.setItem('user', JSON.stringify(userData));
        setUser(userData);
        // setIsAuthenticated(true);
    };

    const logoutUser = () => {
        sessionStorage.removeItem('user');
        setUser(null);
        // setIsAuthenticated(false);
    };

    useEffect(() => {
        const storedUser = JSON.parse(sessionStorage.getItem('user'));
        if (storedUser) {
            setUser(storedUser);
        }
    }, []);


    return (
        <UserContext.Provider value={{ user, setUser, loginUser, logoutUser }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);
