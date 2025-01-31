import './Sidebar.modules.css';
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHome, faFolder, faTasks, faClipboard, faChartBar } from '@fortawesome/free-solid-svg-icons';

const Sidebar = ({ isSidebarShrunk, toggleSidebar }) => {
  useEffect(() => {
    const updateSidebarHeight = () => {
      document.querySelector('.sidebar').style.height = `${window.innerHeight}px`;
    };

    updateSidebarHeight();
    window.addEventListener('resize', updateSidebarHeight);

    return () => window.removeEventListener('resize', updateSidebarHeight);
  }, []);

  return (
    <div className={`sidebar ${isSidebarShrunk ? 'shrink' : ''}`}>
      <ul>
        <li>
            <a href='/'>
                <FontAwesomeIcon icon={faHome} className="icon" />
                <span className="text">Dashboard</span>
            </a>
        </li>
        <li>
            <a href='/projects'>
                <FontAwesomeIcon icon={faFolder} className="icon" />
                <span className="text">Projects</span>
            </a>
        </li>
        <li>
            <a href='/backlog'>
                <FontAwesomeIcon icon={faClipboard} className="icon" />
                <span className="text">Backlog</span>
            </a>
        </li>
        <li> 
            <a href='/tasks'>
                <FontAwesomeIcon icon={faTasks} className="icon" />
                <span className="text">Tasks</span>
            </a>   
        </li>
        <li>
            <a href='/reports'>
                <FontAwesomeIcon icon={faChartBar} className="icon" />
                <span className="text">Reports</span>
            </a>
        </li>
      </ul>
      <button 
        id="shrinkButton" 
        onClick={toggleSidebar} 
        className={isSidebarShrunk ? 'rotated' : ''}
      >
        =
      </button>
    </div>
  );
};


export default Sidebar;