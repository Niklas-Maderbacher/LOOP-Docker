import './Backlog.modules.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import EditIssueForm from './EditIssue/EditIssueForm';


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
    // LOOP-124
    const [isSelectITypeOpen, setIsSelectITypeOpen] = useState(false);
    const [isIssueFormOpen, setIsIssueFormOpen] = useState(false);
    const [issues, setIssues] = useState([]);
    const [selectedIssue, setSelectedIssue] = useState(null);
    
    });
    // LOOP-124
    const [isModalOpen, setIsModalOpen] = useState(true); // Manage modal visibility

    // LOOP-124
    // This function will close the modal
    const closeModal = () => {
        setIsSelectITypeOpen(false);
    };

    useEffect(() => {
        fetchIssues();
    }, []);
    // LOOP-124
    const fetchIssues = async () => {
        try {
            const { data } = await axios.get('http://localhost:8000/api/v1/issues/');
            setIssues(data);
        } catch (error) {
            console.error("Error fetching issues", error);
        }
    };

    function handleOpenSelectIType() {
        setIsSelectITypeOpen(true);
    }

    function handleInputChange(event) {
        const { name, value } = event.target;
        setNewIssue((prevIssue) => ({ ...prevIssue, [name]: value }));
    }

    function handleCloseSelectIType() {
        setIsSelectITypeOpen(false);
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

    function handleIssueClick(issue) {
        setSelectedIssue(issue);
    }

    function handleCloseEditForm() {
        setSelectedIssue(null);
    }

    return (
        <div className="Backlog">
            <button className="add-issue-btn" onClick={handleOpenSelectIType}>Create Issue</button>
            
            {isSelectITypeOpen && (
                <div className="issue-modal">
                    <div className="issue-modal-content">
                        <h2>Select Issue Type</h2>
                        <select name="issueType" value={newIssue.issueType} onChange={handleInputChange}>
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
            // LOOP-124
            <div className="issue-list">
                <h2>Issues</h2>
                {issues?.length > 0 ? (
                <ul>
                    {issues?.map((issue) => (
                        <li key={issue.id} className={`issue ${selectedIssue && selectedIssue.id === issue.id ? 'selected' : ''}`} onClick={() => handleIssueClick(issue)}>
                            {issue.name} - Story points: {issue.story_points}
                        </li>
                    ))}
                </ul>
                ) : (
                    <p className="no-issues">No issues found.</p>
                )}
            </div>

            {selectedIssue && (
                <div>
                  <EditIssueForm
                    issueId={selectedIssue.id}
                    onClose={handleCloseEditForm}
                  />
              </div>
            )}
        </div>
    );
}

export default Backlog;
