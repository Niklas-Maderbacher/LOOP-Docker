//Leo Tandl
import './Backlog.modules.css';
import React, { useState } from 'react';


function Backlog() {
    // State variables to control opening and closing of modals and to store new issue data
    const [isSelectITypeOpen, setIsSelectITypeOpen] = useState(false);  // Controls whether the issue type selection modal is open
    const [isIssueFormOpen, setIsIssueFormOpen] = useState(false);  // Controls whether the issue creation form modal is open

    // Initializes state for the new issue
    const [newIssue, setNewIssue] = useState({ 
        issueType: "", 
        name: "", 
        sprint_id: "", 
        responsible_id: "", 
        priority_id: "", 
        description: "", 
        story_points: "" 
    });

    // Function to open the modal for selecting the issue type
    function handleOpenSelectIType() {
        setIsSelectITypeOpen(true);
    }

    // Function to handle input field changes
    function handleInputChange(event) {
        const { name, value } = event.target;
        
        setNewIssue((prevIssue) => {
            let newValue = value;
    
            // Story Points field validation: only allows numbers
            if (name === "story_points") {
                newValue = value.replace(/[^0-9]/g, "");  // Removes non-numeric characters
                if (newValue !== "" && parseInt(newValue) < 1) {
                    newValue = "1"; // Sets minimum value to 1
                }
            }
    
            return { ...prevIssue, [name]: newValue };  // Returns updated issue state
        });
    }

    // Function to close the issue type selection modal and reset the form state
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

    // Function to handle the submission of the issue type selection
    function handleSubmitIssueType() {
        if (!newIssue.issueType) {
            alert("Choose the type of your issue!"); // Shows an alert if no issue type is selected
            return;
        }
        setIsSelectITypeOpen(false);
        setIsIssueFormOpen(true); // Opens the form to create the new issue
    }

    // Function to close the issue creation form and reset the form state
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

    // Function to handle the submission of the issue creation form
    async function handleSubmitIssueForm() {
        if (!newIssue.name.trim() || !newIssue.description.trim()) {
            alert("Please fill in all required fields: name and description."); // Shows an alert if name or description is missing
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
            category_id: newIssue.issueType,
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
            {/* Button to open the issue type selection modal */}
            <button className="add-issue-btn" onClick={handleOpenSelectIType}>
                Create Issue
            </button>

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

            {/* Modal for inputting issue details */}
            {isIssueFormOpen && (
                <div className="issue-modal">
                    <div className="issue-modal-content">
                        <h2>Create new {newIssue.issueType}</h2>
                        
                        {/* Input for the issue name */}
                        <input 
                            type="text" 
                            name="name" 
                            placeholder="Name" 
                            value={newIssue.name} 
                            onChange={handleInputChange} 
                        />

                        {/* Dropdown for selecting the sprint */}
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

                        {/* Dropdown for selecting the responsible person */}
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

                        {/* Dropdown for selecting the priority */}
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

                        {/* Input for the issue description */}
                        <input 
                            type="text"
                            name="description" 
                            placeholder="Description" 
                            value={newIssue.description} 
                            onChange={handleInputChange} 
                        />

                        {/* Parent Issue dropdown shown only for Subtasks */}
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

                        {/* Story Points field shown only for Epic or Subtask */}
                        {["story", "subtask"].includes(newIssue.issueType) && (
                            <input 
                                type="text"  // Text input to prevent the number input spinner
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
