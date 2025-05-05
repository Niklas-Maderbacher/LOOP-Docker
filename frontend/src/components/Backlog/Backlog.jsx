import './Backlog.modules.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import EditIssueForm from './EditIssue/EditIssueForm';

function Backlog() {
    // LOOP-124
    const [isSelectITypeOpen, setIsSelectITypeOpen] = useState(false);
    const [isIssueFormOpen, setIsIssueFormOpen] = useState(false);
    const [issues, setIssues] = useState([]);
    const [selectedIssue, setSelectedIssue] = useState(null);
    
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
    }

    function handleSubmitIssueForm() {
        fetch("http://localhost:8000/api/v1/issues/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newIssue)
        }).then(() => {
            setIsIssueFormOpen(false);
            fetchIssues();
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
                        <input type="text" name="name" placeholder="Name" value={newIssue.name} onChange={handleInputChange} />
                        <button onClick={handleSubmitIssueForm}>Create issue</button>
                        <button onClick={handleCloseIssueForm}>Cancel</button>
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
