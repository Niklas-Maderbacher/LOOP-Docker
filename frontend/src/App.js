// Updated App.js
import React, { useState, useEffect } from 'react';
import { Routes, Route, BrowserRouter, Navigate } from 'react-router-dom';
import './App.css';
import TopBar from './components/TopBar/TopBar.jsx';
import Sidebar from './components/Sidebar/Sidebar.jsx';
import Content from './components/Content/Content.jsx';
import Backlog from './components/Backlog/Backlog.jsx';
import Projects from './components/Projects/Projects.jsx';
import LoginPage from './components/LoginPage/LoginPage.jsx';
import SignUpPage from './components/SignUpPage/SignUpPage.jsx'; // Import the new SignUpPage

function App() {
  const [isSidebarShrunk, setIsSidebarShrunk] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('jwt');
    if (token) {
      // Optional: Token validieren, um sicherzugehen
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
    }
  }, []);

  const toggleSidebar = () => {
    setIsSidebarShrunk(!isSidebarShrunk);
  };

  return (
    <BrowserRouter>
      {isAuthenticated ? (
        <>
          <TopBar />
          <Sidebar isSidebarShrunk={isSidebarShrunk} toggleSidebar={toggleSidebar} />
          <Routes>
            <Route path="/" element={<Content isSidebarShrunk={isSidebarShrunk} />} />
            <Route path="/projects" element={<Projects isSidebarShrunk={isSidebarShrunk} />} />
            <Route path="/backlog" element={<Backlog isSidebarShrunk={isSidebarShrunk} />} />
            <Route path="/tasks" element={<h1>In progress</h1>} />
            <Route path="/reports" element={<h1>In progress</h1>} />
            <Route path="/login" element={<Navigate to="/" />} />
            <Route path="/signup" element={<Navigate to="/" />} />
          </Routes>
        </>
      ) : (
        <Routes>
          <Route path="/login" element={<LoginPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/signup" element={<SignUpPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      )}
    </BrowserRouter>
  );
}

export default App;