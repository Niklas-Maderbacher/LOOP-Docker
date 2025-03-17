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
        category_id: "", 
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
            category_id: "", 
            sprint_id: "", 
            responsible_id: "", 
            priority_id: "", 
            description: "", 
            story_points: "" 
        });
    }

    // Function to handle the submission of the issue creation form
    function handleSubmitIssueForm() {
        if (!newIssue.name.trim() || !newIssue.description.trim()) {
            alert("Please fill in all required fields: name and description."); // Shows an alert if name or description is missing
            return;
        }
        setIsIssueFormOpen(false);
        // Add API call to create the issue here
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

                        {/* Dropdown for selecting the category */}
                        <select
                            className='issue-dropdown' 
                            name="category_id" 
                            value={newIssue.category_id} 
                            onChange={handleInputChange}
                        >
                            <option value="">Category ↓</option>
                            <option value="1">Category A</option>
                            <option value="2">Category B</option>
                        </select>

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
                            <option value="1">Low</option>
                            <option value="2">Medium</option>
                            <option value="3">High</option>
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
                        {["epic", "subtask"].includes(newIssue.issueType) && (
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
