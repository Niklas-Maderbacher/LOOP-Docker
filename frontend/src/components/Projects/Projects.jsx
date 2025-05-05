import './Projects.modules.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

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

    const [message, setMessage] = useState(null);

    
    const [isAdmin, setIsAdmin] = useState(null); // null = noch nicht geprüft
    const [error, setError] = useState(false);

    useEffect(() => {
        const checkAdmin = async () => {
        try {
            const token = localStorage.getItem("jwt");
            const response = await axios.get("http://localhost:8000/api/v1/security/users/check/admin", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
            });

            const admin = response.data[0]?.admin_state === true;
            setIsAdmin(admin);
        } catch (err) {
            console.error("Admin-Check fehlgeschlagen", err);
            setError(true);
        }
        };

        checkAdmin();
    }, []);

    // Wenn noch geladen wird
    if (isAdmin === null && !error) {
        return <p>Loading...</p>;
    }

    // Kein Admin → blockieren
    if (!isAdmin || error) {
        return <h1 className='error-message'>403 - Zugriff verweigert</h1>;
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

    async function handleArchive() {
        // TODO add parameter for project_id
        try {
        //     const response = await fetch(`/api/v1/projects/archive/${projectId}`, {
        //         method: "PUT",
        //         headers: {
        //             "Authorization": `Bearer ${localStorage.getItem("token")}`,
        //             "Content-Type": "application/json",
        //         },
        //     });

        //     if (!response.ok) {
        //         throw new Error("Failed to archive project");
            // }

            setMessage("Button not yet functioning!");

            // // Remove archived project from state
            // setProjects(projects.filter(project => project.id !== projectId));

            // Hide message after 3 seconds
            setTimeout(() => {
                setMessage(null);
            }, 3000);
        } catch (error) {
            console.error("Error:", error);
            setMessage("Error archiving project ❌");
        }
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
                                <button className="archive-project-btn" onClick={() => handleArchive()}>
                                    Archive
                                </button>
                                {message && <div className="message-box">{message}</div>}
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
