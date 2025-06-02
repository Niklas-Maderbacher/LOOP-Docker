//Leo Tandl
import './Backlog.modules.css';
import React, { useState, useEffect } from 'react';



function Backlog() {
    // State variables to control opening and closing of modals and to store new issue data
    const [isSelectITypeOpen, setIsSelectITypeOpen] = useState(false);  // Controls whether the issue type selection modal is open
    const [isIssueFormOpen, setIsIssueFormOpen] = useState(false);  // Controls whether the issue creation form modal is open
    const [project, setProject] = useState(null);

    const [newIssue, setNewIssue] = useState({
        issueType: "",
        name: "",
        sprint_id: "",
        responsible_id: "",
        priority_id: "",
        description: "",
        story_points: ""
    });

    const [newSprint, setNewSprint] = useState({
        name: "",
        start_date: "",
        end_date: "",
        goal: "",
        project_id: ""
    });

    useEffect(() => {
        const stored = localStorage.getItem("selectedProject");
        if (stored) {
        setProject(JSON.parse(stored));
        }
    }, []);

    if (!project) {
        return <h1 className='message'>Kein Projekt ausgewählt.</h1>;
    }

    function handleOpenSelectIType() {
        setIsSelectITypeOpen(true);
    }

    function handleInputChange(event) {
        const { name, value } = event.target;

        setNewIssue((prevIssue) => {
            let newValue = value;

            if (name === "story_points") {
                newValue = value.replace(/[^0-9]/g, "");
                if (newValue !== "" && parseInt(newValue) < 1) {
                    newValue = "1";
                }
            }

            return { ...prevIssue, [name]: newValue };
        });
    }

    function handleOpenSprintForm() {
        setIsSprintFormOpen(true);
    }

    function handleSprintInputChange(event) {
        const { name, value } = event.target;
        setNewSprint((prevSprint) => ({
            ...prevSprint,
            [name]: value
        }));
    }

    function handleCloseSprintForm() {
        setIsSprintFormOpen(false);
        setNewSprint({ name: "", start_date: "", end_date: "", goal: "" });
    }

    function handleCloseSelectIType() {
        setIsSelectITypeOpen(false);
        setNewIssue({
            issueType: "",
            name: "",
            sprint_id: "",
            responsible_id: "",
            priority_id: "",
            description: "",
            story_points: ""
        });
    }

    function handleSubmitIssueType() {
        if (!newIssue.issueType) {
            alert("Choose the type of your issue!");
            return;
        }
        setIsSelectITypeOpen(false);
        setIsIssueFormOpen(true);
    }

    function handleCloseIssueForm() {
        setIsIssueFormOpen(false);
        setNewIssue({
            issueType: "",
            name: "",
            sprint_id: "",
            responsible_id: "",
            priority_id: "",
            description: "",
            story_points: ""
        });
    }

    async function handleSubmitSprintForm() {
        const { name, start_date, end_date, goal, project_id } = newSprint;

        if (!name || !start_date || !end_date || !goal || !project_id ) {
            alert("Please fill in all sprint fields including goal.");
            return;
        }
        const token = localStorage.getItem("jwt");
        const response = await fetch("http://localhost:8000/api/v1/sprints/create", {
        
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`, // <<< wichtig!
            },
            body: JSON.stringify({
                name,
                start_date,
                end_date,
                goal,
                project_id,
            })
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Fehler beim Erstellen des Sprints:", response.status, errorText);
            alert("Fehler beim Erstellen des Sprints. Siehe Konsole.");
            return;
        }    

        const data = await response.json();
        console.log("Sprint created:", data);
        handleCloseSprintForm();
    }


    async function handleSubmitIssueForm() {
        if (!newIssue.name.trim() || !newIssue.description.trim()) {
            alert("Please fill in all required fields: name and description.");
            return;
        }

        const response = await fetch("http://localhost:8000/api/v1/issues/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: newIssue.name,
                category: newIssue.issueType,
                sprint_id: newIssue.sprint_id || null,
                responsible_id: newIssue.responsible_id || null,
                priority_id: newIssue.priority_id || null,
                description: newIssue.description,
                story_points: newIssue.story_points || null,
                project_id: 1
            })
        });

        const data = await response.json();
        console.log(data);

        setIsIssueFormOpen(false);
        setNewIssue({
            issueType: "",
            name: "",
            sprint_id: "",
            responsible_id: "",
            priority_id: "",
            description: "",
            story_points: ""
        });
    }

    return (
        <div className="Backlog">
            <button className="add-issue-btn" onClick={handleOpenSelectIType}>
                Create Issue
            </button>

            <button className="add-sprint-btn" onClick={handleOpenSprintForm}>
                Create Sprint
            </button>

            <h1 className='message'>Project {localStorage.getItem("selectedProject")} selected</h1>

            {/* Modal for selecting the issue type */}
            {isSelectITypeOpen && (
                <div className="issue-modal">
                    <div className="issue-modal-content">
                        <h2>Select Issue Type</h2>
                        <select
                            className='issue-dropdown'
                            name="issueType"
                            value={newIssue.issueType}
                            onChange={handleInputChange}
                        >
                            <option value="">Select...</option>
                            <option value="Bug">Bug</option>
                            <option value="Epic">Epic</option>
                            <option value="User Story">Story</option>
                            <option value="Subtask">Subtask</option>
                        </select>
                        <div className="modal-buttons">
                            <button onClick={handleSubmitIssueType}>Submit</button>
                            <button onClick={handleCloseSelectIType}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}

            {isIssueFormOpen && (
                <div className="issue-modal">
                    <div className="issue-modal-content">
                        <h2>Create new {newIssue.issueType}</h2>

                        <input
                            type="text"
                            name="name"
                            placeholder="Name"
                            value={newIssue.name}
                            onChange={handleInputChange}
                        />

                        <select
                            className='issue-dropdown'
                            name="sprint_id"
                            value={newIssue.sprint_id}
                            onChange={handleInputChange}
                        >
                            <option value="">Sprint ↓</option>
                            <option value="1">Sprint 1</option>
                            <option value="2">Sprint 2</option>
                        </select>

                        <select
                            className='issue-dropdown'
                            name="responsible_id"
                            value={newIssue.responsible_id}
                            onChange={handleInputChange}
                        >
                            <option value="">Responsible ↓</option>
                            <option value="1">Max</option>
                            <option value="2">Anna</option>
                        </select>

                        <select
                            className='issue-dropdown'
                            name="priority_id"
                            value={newIssue.priority_id}
                            onChange={handleInputChange}
                        >
                            <option value="">Priority ↓</option>
                            <option value="Very high">Very high</option>
                            <option value="High">High</option>
                            <option value="Medium">Medium</option>
                            <option value="Low">Low</option>
                            <option value="Very low">Very low</option>
                        </select>

                        <input
                            type="text"
                            name="description"
                            placeholder="Description"
                            value={newIssue.description}
                            onChange={handleInputChange}
                        />

                        {newIssue.issueType === "subtask" && (
                            <select
                                className='issue-dropdown'
                                name="parent_issue_id"
                                value={newIssue.parent_issue_id}
                                onChange={handleInputChange}
                            >
                                <option value="">Parent Issue</option>
                                <option value="1">Parent Issue 1</option>
                                <option value="2">Parent Issue 2</option>
                            </select>
                        )}

                        {["story", "subtask"].includes(newIssue.issueType.toLowerCase()) && (
                            <input
                                type="text"
                                name="story_points"
                                placeholder="Story Points (optional)"
                                value={newIssue.story_points}
                                onChange={handleInputChange}
                            />
                        )}

                        <div className="modal-buttons">
                            <button onClick={handleSubmitIssueForm}>Create issue</button>
                            <button onClick={handleCloseIssueForm}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}

            {isSprintFormOpen && (
                <div className="issue-modal">
                    <div className="issue-modal-content">
                        <h2>Create Sprint</h2>

                        <input
                            type="text"
                            name="name"
                            placeholder="Sprint Name"
                            value={newSprint.name}
                            onChange={handleSprintInputChange}
                        />

                        <input
                            type="date"
                            name="start_date"
                            value={newSprint.start_date}
                            onChange={handleSprintInputChange}
                        />

                        <input
                            type="date"
                            name="end_date"
                            value={newSprint.end_date}
                            onChange={handleSprintInputChange}
                        />

                        <input
                            type="text"
                            name="goal"
                            placeholder="Sprint Goal"
                            value={newSprint.goal}
                            onChange={handleSprintInputChange}
                        />

                        <input
                            type="text"
                            name="project_id"
                            placeholder="Project ID"
                            value={newSprint.project_id}
                            onChange={handleSprintInputChange}
                        />


                        <div className="modal-buttons">
                            <button onClick={handleSubmitSprintForm}>Create Sprint</button>
                            <button onClick={handleCloseSprintForm}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Backlog;
