import React from 'react';
import { ToastContainer } from 'react-toastify'; // Importe o ToastContainer
import 'react-toastify/dist/ReactToastify.css'; // Importe o CSS do toastify
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login.jsx'; 
import Register from './components/Register.jsx';
import { AuthProvider } from './contexts/AuthContext.jsx';
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
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
              </Routes>
          </AuthProvider>
      </Router>
  );
};

export default App;
