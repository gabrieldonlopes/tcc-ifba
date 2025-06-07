import React from 'react';
import { ToastContainer } from 'react-toastify'; // Importe o ToastContainer
import 'react-toastify/dist/ReactToastify.css'; // Importe o CSS do toastify
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext.jsx';

import HomePage from './components/HomePage.jsx';

import Login from './components/auth/Login.jsx';
import Register from  './components/auth/Register.jsx';

import Lab from './components/lab/Lab.jsx';
import UserLabs from './components/lab/UserLabs.jsx';
//import './App.css'

const App = () => {
  return (
      <Router>
          <AuthProvider>
          <ToastContainer
                  toastClassName="bg-gray-800 text-white rounded-lg shadow-lg p-4"
                  bodyClassName="text-sm"
                  position="top-right"
                  autoClose={3000}
                  hideProgressBar={false}
                  closeOnClick
                  pauseOnHover
                  draggable
              />
              <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path='/login' element={<Login />}/>
                  <Route path="/register" element={<Register />} />
                  <Route path="/user_labs" element={<UserLabs />} />
                  <Route path="/lab" element={<Lab />} />

              </Routes>
          </AuthProvider>
      </Router>
  );
};

export default App;
