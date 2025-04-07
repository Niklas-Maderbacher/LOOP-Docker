import './Projects.modules.css';
import React, { useState, useEffect } from 'react';

function Projects() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [projects, setProjects] = useState([
        { name: "Project Alpha", key: "ALPHA", type: "Software", lead: "Alice" },
        { name: "Project Beta", key: "BETA", type: "Marketing", lead: "Bob" },
        { name: "Project Gamma", key: "GAMMA", type: "Design", lead: "Charlie" }
    ]);
    const [isAdmin, setIsAdmin] = useState(false);
    const [newProject, setNewProject] = useState({ name: "", key: "", type: "", lead: "", description: "" });
    const [message, setMessage] = useState(null);
    const [loading, setLoading] = useState(true);

    // Check if user is admin when component mounts
    useEffect(() => {
        checkIfAdmin();
    }, []);

    // Function to check if user is admin via the API
    const checkIfAdmin = async () => {
        try {
            const token = localStorage.getItem('jwt');
            if (!token) {
                setIsAdmin(false);
                setLoading(false);
                return;
            }

            // Option 1: Use the specific admin check endpoint
            const response = await fetch('http://localhost:8000/api/v1/security/users/check/admin', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            // If successful, the user is an admin
            if (response.ok) {
                setIsAdmin(true);
            } else {
                // If 403 Forbidden, user is not an admin
                setIsAdmin(false);
            }

            // Option 2: Get the full user profile and check is_admin
            /*
            const userResponse = await fetch('http://localhost:8000/api/v1/security/users/me/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (userResponse.ok) {
                const userData = await userResponse.json();
                setIsAdmin(userData.is_admin);
            } else {
                setIsAdmin(false);
            }
            */
        } catch (error) {
            console.error("Error checking admin status:", error);
            setIsAdmin(false);
        } finally {
            setLoading(false);
        }
    };

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

    async function handleArchive() {
        // TODO add parameter for project_id
        try {
        //     const response = await fetch(`/api/v1/projects/archive/${projectId}`, {
        //         method: "PUT",
        //         headers: {
        //             "Authorization": `Bearer ${localStorage.getItem("jwt")}`,
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

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="projects">
            <h1>Projects</h1>
            
            {/* Only show the Create Project button if user is admin */}
            {isAdmin && (
                <button className="add-project-btn" onClick={handleOpenModal}>
                    Create Project  
                </button>
            )}

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
                            {isAdmin && <th>Actions</th>}
                        </tr>
                    </thead>
                    <tbody>
                        {projects.map((project, index) => (
                            <tr key={index}>
                                <td>{project.name}</td>
                                <td>{project.key}</td>
                                <td>{project.type}</td>
                                <td>{project.lead}</td>
                                {isAdmin && (
                                    <td>
                                        <button 
                                            className="archive-project-btn" 
                                            onClick={() => handleArchive()}
                                        >
                                            Archive
                                        </button>
                                    </td>
                                )}
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