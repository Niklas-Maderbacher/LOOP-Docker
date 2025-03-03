import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import TopBar from './components/TopBar/TopBar.jsx'
import Sidebar from './components/Sidebar/Sidebar.jsx'
import Content from './components/Content/Content.jsx'
import Projects from './components/Projects/Projects.jsx'
import Backlog from  './components/Backlog/Backlog.jsx';
import {Routes, Route, BrowserRouter} from 'react-router-dom'


function App() {
  const [isSidebarShrunk, setIsSidebarShrunk] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarShrunk(!isSidebarShrunk);
  };

  return (
    <div>
      <TopBar />
      <Sidebar isSidebarShrunk={isSidebarShrunk} toggleSidebar={toggleSidebar} />

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Content isSidebarShrunk={isSidebarShrunk} />}></Route>
          <Route path="/projects" element={<Projects isSidebarShrunk={isSidebarShrunk} />}></Route>
          {/* Integrate Backlog(Add Issue Only)*/}
          <Route path="/backlog" element={<Backlog isSidebarShrunk={isSidebarShrunk}/>}></Route>
          <Route path="/tasks" element={<h1>In progress</h1>}></Route>
          <Route path="/reports" element={<h1>In progress</h1>}></Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
};

export default App;
