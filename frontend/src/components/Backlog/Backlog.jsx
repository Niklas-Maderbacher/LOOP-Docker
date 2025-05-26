import './Backlog.modules.css';
import React, { useState } from 'react';

function Backlog() {
    const [isSelectITypeOpen, setIsSelectITypeOpen] = useState(false);
    const [isIssueFormOpen, setIsIssueFormOpen] = useState(false);

    const [newIssue, setNewIssue] = useState({ 
        name: "", 
        responsible_user_id: "", 
        priority_id: "", 
        story_points: "" 
    });

    // Neuer State für die Liste aller Issues
    const [issues, setIssues] = useState([]);

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

    function handleCloseSelectIType() {
        setIsSelectITypeOpen(false);
        setNewIssue({ 
            issueType: "", 
            name: "", 
            category: "", 
            sprint_id: "", 
            responsible_user_id: "", 
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
            category_id: "", 
            sprint_id: "", 
            responsible_user_id: "", 
            priority_id: "", 
            description: "", 
            story_points: "" 
        });
    }

    function handleSubmitIssueForm() {
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
        console.log(JSON.stringify({
            name: newIssue.name,
            category: newIssue.issueType,
            sprint_id: newIssue.sprint_id || null,
            responsible_id: newIssue.responsible_id || null,
            priority_id: newIssue.priority_id || null,
            description: newIssue.description,
            story_points: newIssue.story_points || null,
            project_id: null
        }));

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

            {/* Tabelle mit allen Issues */}
            <table className="issue-table">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Priority</th>
                        <th>Story Points</th>
                        <th>Responsible</th>
                    </tr>
                </thead>
                <tbody>
                    {issues.map(issue => (
                        <tr key={issue.id}>
                            <td>{issue.name}</td>
                            <td>{issue.priority}</td>
                            <td>{issue.story_points}</td>
                            <td>{issue.responsible_user_id}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

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
                            name="responsible_user_id" 
                            value={newIssue.responsible_user_id} 
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
                            <option value="1">Low</option>
                            <option value="2">Medium</option>
                            <option value="3">High</option>
                        </select>

                        {["story", "subtask"].includes(newIssue.issueType) && (
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
        </div>  
    );
}

export default Backlog;