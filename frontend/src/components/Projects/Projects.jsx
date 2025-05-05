import './Projects.modules.css';
import React, { useState, useEffect } from 'react';

function Projects() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [projects, setProjects] = useState([]);
    const [isAdmin, setIsAdmin] = useState(false);
    const [newProject, setNewProject] = useState({ name: "", key: "", start_date: "", end_date: "", github_token: "" });
    const [message, setMessage] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch projects and check admin status when component mounts
    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                await Promise.all([
                    fetchProjects(),
                    checkIfAdmin()
                ]);
            } catch (error) {
                console.error("Error initializing data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchInitialData();
    }, []);

    // Function to fetch projects from the API
    const fetchProjects = async () => {
        try {
            const token = localStorage.getItem('jwt');
            if (!token) {
                setError("Authentication required");
                return;
            }

            const response = await fetch('http://localhost:8000/api/v1/projects/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch projects: ${response.status}`);
            }

            const projectsData = await response.json();
            setProjects(projectsData);
        } catch (error) {
            console.error("Error fetching projects:", error);
            setError("Failed to load projects");
        }
    };

    // Function to check if user is admin via the API
    const checkIfAdmin = async () => {
        try {
            const token = localStorage.getItem('jwt');
            if (!token) {
                setIsAdmin(false);
                return;
            }

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
        } catch (error) {
            console.error("Error checking admin status:", error);
            setIsAdmin(false);
        }
    };

    function handleOpenModal() {
        setIsModalOpen(true);
    }

    function handleCloseModal() {
        setIsModalOpen(false);
        setNewProject({ name: "", key: "", start_date: "", end_date: "", github_token: "" });
    }

    function handleInputChange(event) {
        setNewProject({ ...newProject, [event.target.name]: event.target.value });
    }

    async function handleSubmit() {
        if (!newProject.name.trim() || !newProject.key.trim()) {
            setMessage("Name and Key are required fields.");
            setTimeout(() => setMessage(null), 3000);
            return;
        }

        try {
            const token = localStorage.getItem('jwt');
            if (!token) {
                setError("Authentication required");
                return;
            }

            const response = await fetch('http://localhost:8000/api/v1/projects/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ...newProject,
                    start_date: newProject.start_date.trim() === "" ? null : newProject.start_date,
                    end_date: newProject.end_date.trim() === "" ? null : newProject.end_date
                })
            });

            const responseData = await response.json();

            if (!response.ok) {
                throw new Error(`Failed to create project: ${response.status} - ${responseData.detail || responseData.message}`);
            }

            // Refresh the project list after successful creation
            await fetchProjects();
            handleCloseModal();
            setMessage("Project created successfully!");
            setTimeout(() => setMessage(null), 3000);
        } catch (error) {
            console.error("Error creating project:", error.message);
            setMessage(`Error creating project: ${error.message}`);
            setTimeout(() => setMessage(null), 3000);
        }
    }

    async function handleArchive(projectId) {
        try {
            const token = localStorage.getItem('jwt');
            if (!token) {
                setError("Authentication required");
                return;
            }

            const response = await fetch(`http://localhost:8000/api/v1/projects/archive-project/${projectId}`, {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error("Failed to archive project");
            }

            // Refresh the project list after successful archiving
            await fetchProjects();
            setMessage("Project archived successfully!");
            setTimeout(() => setMessage(null), 3000);
        } catch (error) {
            console.error("Error:", error);
            setMessage("Error archiving project");
            setTimeout(() => setMessage(null), 3000);
        }
    }

    if (loading) {
        return <div className="loading">Loading projects...</div>;
    }

    if (error) {
        return <div className="error-message">{error}</div>;
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

            {message && <div className="message-box">{message}</div>}

            <div className="project-list">
                {projects.length === 0 ? (
                    <p>No projects found.</p>
                ) : (
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Key</th>
                                <th>Start Date</th>
                                <th>End Date</th>
                                {isAdmin && <th>Actions</th>}
                            </tr>
                        </thead>
                        <tbody>
                            {projects.filter(project => !project.archived_at).map(project => (
                                <tr key={project.id}>
                                    <td>{project.name}</td>
                                    <td>{project.key}</td>
                                    <td style={{ textAlign: 'center' }}>{project.start_date || '-'}</td>
                                    <td  style={{ textAlign: 'center' }}>{project.end_date || '-'}</td>
                                    {isAdmin && (
                                        <td>
                                            <button 
                                                className="archive-project-btn" 
                                                onClick={() => handleArchive(project.id)}
                                            >
                                                Archive
                                            </button>
                                        </td>
                                    )}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
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
                            required
                        />
                        <input 
                            type="text" 
                            name="key" 
                            placeholder="Project Key" 
                            value={newProject.key} 
                            onChange={handleInputChange} 
                            required
                        />
                        <input 
                            type="date" 
                            name="start_date" 
                            placeholder="Project Start Date" 
                            value={newProject.start_date} 
                            onChange={handleInputChange} 
                        />
                        <input 
                            type="date" 
                            name="end_date" 
                            placeholder="Project End Date" 
                            value={newProject.end_date} 
                            onChange={handleInputChange}
                        />

                        <input 
                            type="text" 
                            name="github_token" 
                            placeholder="Project GitHub Token" 
                            value={newProject.github_token} 
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