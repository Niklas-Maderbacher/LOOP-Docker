import './Projects.modules.css';
import React, { useState, useEffect } from 'react';
import ArchiveButton from '../ArchiveButton/ArchiveButton.jsx';
import axios from 'axios';

function Projects() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [projects, setProjects] = useState([]);
    const [newProject, setNewProject] = useState({ name: "", key: "", type: "", lead: "", description: "" });

    useEffect(() => {
        async function fetchProjects() {
            try {
                const response = await axios.get('http://localhost:8000/api/v1/projects/'); // Adjust with your API endpoint
                setProjects(response.data);
            } catch (error) {
                console.error("There was an error fetching the projects!", error);
            }
        }
    
        fetchProjects();
    }, []);    

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
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                    {projects.map((project) => (
                        <tr key={project.id}>
                            <td>{project.name}</td>
                            <td>{project.key}</td>
                            <td>{project.type}</td>
                            <td>{project.lead}</td>
                            <td>
                                <ArchiveButton projectName={project.name} actionType={"archive"} />
                            </td>
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
