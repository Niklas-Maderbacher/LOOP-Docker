import './Content.modules.css';
import React from 'react';

function Content({ isSidebarShrunk }) {
    return (
      <div className="content">
        <h1>Welcome to Loop</h1>
        <p>Start managing your tasks and projects efficiently!</p>
      </div>
    );
}

export default Content;