import './Backlog.modules.css';
import React, { useState } from 'react';

function Backlog() {
    const [isSelectITypeOpen, setIsSelectITypeOpen] = useState(false);
    const [isIssueFormOpen, setIsIssueFormOpen] = useState(false);

    const [newIssue, setNewIssue] = useState({ 
        issueType: "", 
        name: "", 
        category_id: "", 
        sprint_id: "", 
        responsible_id: "", 
        priority_id: "", 
        description: "", 
        story_points: "" 
    });

    function handleOpenSelectIType() {
        setIsSelectITypeOpen(true);
    }

    function handleInputChange(event) {
        const { name, value } = event.target;
        
        setNewIssue((prevIssue) => {
            let newValue = value;
    
            // Story Points nur für story, epic, subtask
            if (name === "story_points") {
                newValue = value.replace(/[^0-9]/g, ""); // Entfernt alle Nicht-Zahlen
                if (newValue !== "" && parseInt(newValue) < 1) {
                    newValue = "1"; // Setzt min. Wert auf 1
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
            category_id: "", 
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
            category_id: "", 
            sprint_id: "", 
            responsible_id: "", 
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
        setIsIssueFormOpen(false)
        console.log("Issue wird gesendet:", newIssue);
        // Hier den API-Call einfügen
        setNewIssue({ 
            issueType: "", 
            name: "", 
            category_id: "", 
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

            {/* Modal für die Auswahl des Issue-Typs */}
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
                            <option value="bug">Bug</option>
                            <option value="epic">Epic</option>
                            <option value="story">Story</option>
                            <option value="subtask">Subtask</option>
                        </select>
                        <div className="modal-buttons">
                            <button onClick={handleSubmitIssueType}>Submit</button>
                            <button onClick={handleCloseSelectIType}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}

            {/* Modal für die Erstellung des Issues */}
            {isIssueFormOpen && (
                <div className="issue-modal">
                    <div className="issue-modal-content">
                        <h2>Create new {newIssue.issueType}</h2>
                        
                        {/* Name */}
                        <input 
                            type="text" 
                            name="name" 
                            placeholder="Name" 
                            value={newIssue.name} 
                            onChange={handleInputChange} 
                        />

                        {/* Kategorie */}
                        <select
                            className='issue-dropdown' 
                            name="category_id" 
                            value={newIssue.category_id} 
                            onChange={handleInputChange}
                        >
                            <option value="">Category ↓</option>
                            <option value="1">Kategorie A</option>
                            <option value="2">Kategorie B</option>
                        </select>

                        {/* Sprint */}
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

                        {/* Verantwortlicher */}
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

                        {/* Priorität */}
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

                        {/* Beschreibung */}
                        <input 
                            type="text"
                            name="description" 
                            placeholder="Description" 
                            value={newIssue.description} 
                            onChange={handleInputChange} 
                        />

                        {/* Story Points nur anzeigen, wenn nötig */}
                        {["epic", "subtask"].includes(newIssue.issueType) && (
                            <input 
                                type="text"  // Textfeld, damit kein Zähler angezeigt wird
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
