import React, { useEffect, useState } from 'react';
import axios from "axios";
import './ProjectsDashboard.modules.css';

// Loop-125
const ProjectList = () => {
    const [projects, setProjects] = useState([]);

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                const token = localStorage.getItem("jwt");
            
                const response = await axios.get("http://localhost:8000/api/v1/projects/me", {
                  headers: {
                    Authorization: `Bearer ${token}`
                  }
                });
            
                setProjects(response.data);
              } catch (error) {
                console.error("Fehler beim Laden der Projekte:", error);
              }
        };

        fetchProjects();
    }, []);

    const handleProjectClick = (project) => {
        localStorage.setItem("selectedProject", JSON.stringify(project));
        window.location.href = "/backlog";
    };

    if (projects.length === 0) {
        return (
            <div className="project-list-container">
                <p>You are not in a project.</p>
            </div>
        );
    }

    return (
        <div className="project-list-container">
            <div className="project-list">
                {projects.map((project) => (
                    <div key={project.id} className="project-card">
                        <div className="project-info">
                            <div>
                                <div className="project-name">{project.name}</div>
                                <div className="project-key">{project.key}</div>
                            </div>
                        </div>
                        <button
                            className="project-button"
                            onClick={() => handleProjectClick(project.id)}
                        >
                            Auswählen
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ProjectList;
