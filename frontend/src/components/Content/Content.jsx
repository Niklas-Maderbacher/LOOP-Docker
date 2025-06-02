import './Content.modules.css';

import React from 'react';
import FileUpload from './FileUploader/FileUploader';
import ProjectsDashboard from './ProjectsDashboard/ProjectsDashboard'


function Content() {
    return (
      <div className="content">
        <h1>Welcome to Loop</h1>

        <p>Start managing your tasks and projects efficiently!</p>
        <ProjectsDashboard />
        <FileUpload />
      </div>
    );
}

export default Content;