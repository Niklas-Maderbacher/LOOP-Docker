import './Content.modules.css';

import ProjectsDashboard from './ProjectsDashboard/ProjectsDashboard'


function Content( {isSidebarShrunk} ) {
    return (
      <div className="content">
        <h1>Welcome to Loop</h1>

        <p>Start managing your tasks and projects efficiently!</p>
        <ProjectsDashboard />
      </div>
    );
}

export default Content;