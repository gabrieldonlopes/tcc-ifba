import React, { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser, fetchUserProfile, registerUser } from '../api/api_auth.js';
import { toast } from "react-toastify";

const AuthContext = createContext({});

const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (token) {
            const getUser = async () => {
                const user = await fetchUserProfile(token);
                setUser(user);
            };
            getUser();
        }
    }, [token]);

    const login = async (username, password) => {
        try {
            const response = await loginUser({ username, password });
            if (response?.access_token) {
                setToken(response.access_token);
                localStorage.setItem('token', response.access_token);
                const userProfile = await fetchUserProfile(response.access_token);
                setUser(userProfile);
                navigate('/user_labs');
            }
        } catch (error) {
            toast.error(error.message);
        }
    };

    const register = async (username, email, password) => {
        try {
            await registerUser({ username, email, password });
            navigate('/');
        } catch (error) {
            toast.error(error.message);
        }
    };

    const logout = () => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <AuthContext.Provider value={{ token, user, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export {AuthProvider, AuthContext}