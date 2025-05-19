import './Projects.modules.css';
import React, { useState } from 'react';
import { createSprint } from '../../services/sprintService'; // Pfad anpassen!

function Sprints() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [sprints, setSprints] = useState([]);
    const [message, setMessage] = useState(null);

    const [newSprint, setNewSprint] = useState({
        name: "",
        startDate: "",
        endDate: "",
        goal: "",
        projectId: ""  // falls notwendig
    });

    function handleOpenModal() {
        setIsModalOpen(true);
    }

    function handleCloseModal() {
        setIsModalOpen(false);
        setNewSprint({
            name: "",
            startDate: "",
            endDate: "",
            goal: "",
            projectId: ""
        });
    }

    function handleInputChange(event) {
        setNewSprint({ ...newSprint, [event.target.name]: event.target.value });
    }

    async function handleSubmit() {
        try {
            const created = await createSprint(newSprint);
            setSprints([...sprints, created]);
            setMessage("Sprint erfolgreich erstellt ✅");
            handleCloseModal();
        } catch (error) {
            console.error("Fehler beim Erstellen des Sprints:", error);
            setMessage("Fehler beim Erstellen des Sprints ❌");
        }

        setTimeout(() => setMessage(null), 3000);
    }

    return (
        <div className="projects">
            <h1>Sprints</h1>
            <button className="add-project-btn" onClick={handleOpenModal}>
                Create Sprint
            </button>

            <div className="search">
                <input type="text" placeholder="Search..." />
            </div>

            <div className="project-list">
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Start</th>
                            <th>End</th>
                            <th>Goal</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sprints.map((sprint, index) => (
                            <tr key={index}>
                                <td>{sprint.name}</td>
                                <td>{sprint.startDate}</td>
                                <td>{sprint.endDate}</td>
                                <td>{sprint.goal}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {message && <div className="message-box">{message}</div>}
            </div>

            {isModalOpen && (
                <div className="modal">
                    <div className="modal-content">
                        <h2>Create a New Sprint</h2>
                        <input
                            type="text"
                            name="name"
                            placeholder="Sprint Name"
                            value={newSprint.name}
                            onChange={handleInputChange}
                        />
                        <input
                            type="date"
                            name="startDate"
                            placeholder="Start Date"
                            value={newSprint.startDate}
                            onChange={handleInputChange}
                        />
                        <input
                            type="date"
                            name="endDate"
                            placeholder="End Date"
                            value={newSprint.endDate}
                            onChange={handleInputChange}
                        />
                        <input
                            type="text"
                            name="goal"
                            placeholder="Sprint Goal"
                            value={newSprint.goal}
                            onChange={handleInputChange}
                        />
                        <input
                            type="text"
                            name="projectId"
                            placeholder="Project ID"
                            value={newSprint.projectId}
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

export default Sprints;
