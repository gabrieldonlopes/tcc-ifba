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
import MachinePage from './components/machine/MachinePage.jsx';
import MachineList from './components/machine/MachineList.jsx';
import TaskPage from './components/tasks/TaskPage.jsx';
import StudentsPage from './components/student/StudentPage.jsx';
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
                  <Route path="/lab/:lab_id" element={<Lab />} />
                  <Route path="/lab/:lab_id/machines" element={<MachineList />} />
                  <Route path='/lab/:lab_id/students' element={<StudentsPage />} />
                  <Route path="/lab/:lab_id/tasks" element={<TaskPage />} />
                  <Route path="/maquina/:machine_key" element={<MachinePage />} />
              </Routes>
          </AuthProvider>
      </Router>
  );
};

export default App;
