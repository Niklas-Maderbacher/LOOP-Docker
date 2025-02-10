import React, { useState, useEffect } from 'react';
import './TopBar.modules.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBell } from '@fortawesome/free-solid-svg-icons'


// TopBar Component
const TopBar = () => {
  const [isDropdownVisible, setIsDropdownVisible] = useState(false);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);

  const toggleDropdown = () => {
    setIsDropdownVisible(!isDropdownVisible);
  };

  const toggleProfileModal = () => {
    setIsProfileModalOpen(!isProfileModalOpen);
  };

  return (
    <div className="top-bar">
      <a href="#home" className="logo">L∞p</a>

      <div className="search">
        <input type="text" placeholder="Search..." />
      </div>

      <div className="navigation">
        <a href="#dashboard">Dashboard</a>
        <a href="#projects">Projects</a>
        <a href="#tasks">Tasks</a>
      </div>

      <div className="hamburger-menu" onClick={toggleDropdown}>
        <span></span>
        <span></span>
        <span></span>
      </div>

      {isDropdownVisible && (
        <div className="dropdown-navigation">
          <a href="#dashboard">Dashboard</a>
          <a href="#projects">Projects</a>
          <a href="#tasks">Tasks</a>
        </div>
      )}

      <div className="profile">
        <a href="#notifications"><FontAwesomeIcon icon={faBell} style={{color: "#ffffff",}} /></a>
        <div className="name">John Doe</div>
        <a href="#profile"  onClick={toggleProfileModal}>
          <div className="avatar">JD</div>
        </a>
      </div>
      {isProfileModalOpen && (
        <div className="profile-modal">
          <div className="profile-modal-content">
            <a href="#profile-settings">Profile Settings</a>
            <a href="#logout">Logout</a>
          </div>
        </div>
      )}
    </div>
  );
};

export default TopBar;