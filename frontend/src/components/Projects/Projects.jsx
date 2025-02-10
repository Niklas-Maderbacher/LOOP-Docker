import './Projects.modules.css';
import React, { useState } from 'react';

function Projects() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [projects, setProjects] = useState([
        { name: "Project Alpha", key: "ALPHA", type: "Software", lead: "Alice" },
        { name: "Project Beta", key: "BETA", type: "Marketing", lead: "Bob" },
        { name: "Project Gamma", key: "GAMMA", type: "Design", lead: "Charlie" }
    ]);

    const [newProject, setNewProject] = useState({ name: "", key: "", type: "", lead: "", description: "" });

    function handleOpenModal() {
        setIsModalOpen(true);
    }

    function handleCloseModal() {
        setIsModalOpen(false);
        setNewProject({ name: "", key: "", type: "", lead: "", description: "" });
    }

    function handleInputChange(event) {
        setNewProject({ ...newProject, [event.target.name]: event.target.value });
    }

    function handleSubmit() {
        setProjects([...projects, newProject]);
        handleCloseModal();
    }

    return (
        <div className="projects">
            <h1>Projects</h1>
            <button className="add-project-btn" onClick={handleOpenModal}>
                Create Project
            </button>
            <div className="search">
                <input type="text" placeholder="Search..." />
            </div>

            <div className="project-list">
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Key</th>
                            <th>Type</th>
                            <th>Lead</th>
                        </tr>
                    </thead>
                    <tbody>
                        {projects.map((project, index) => (
                            <tr key={index}>
                                <td>{project.name}</td>
                                <td>{project.key}</td>
                                <td>{project.type}</td>
                                <td>{project.lead}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {isModalOpen && (
                <div className="modal">
                    <div className="modal-content">
                        <h2>Create a New Project</h2>
                        <input 
                            type="text" 
                            name="name" 
                            placeholder="Project Name" 
                            value={newProject.name} 
                            onChange={handleInputChange} 
                        />
                        <input 
                            type="text" 
                            name="key" 
                            placeholder="Project Key" 
                            value={newProject.key} 
                            onChange={handleInputChange} 
                        />
                        <input 
                            type="text" 
                            name="type" 
                            placeholder="Project Type" 
                            value={newProject.type} 
                            onChange={handleInputChange} 
                        />
                        <input 
                            type="text" 
                            name="lead" 
                            placeholder="Project Lead" 
                            value={newProject.lead} 
                            onChange={handleInputChange} 
                        />
                        <input 
                            type="text" 
                            name="description" 
                            placeholder="Project Description" 
                            value={newProject.description} 
                            onChange={handleInputChange} 
                        />

                        <div className="modal-buttons">
                            <button onClick={handleSubmit}>Submit</button>
                            <button onClick={handleCloseModal}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}
        </div>  
    );
}

export default Projects;
