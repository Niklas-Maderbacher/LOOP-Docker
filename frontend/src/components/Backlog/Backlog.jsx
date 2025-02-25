import './Backlog.modules.css';
import React, { useState } from 'react';

function Backlog() {
    const [isSelectITypeOpen, setIsSelectITypeOpen] = useState(false);

    const [newIssue, setNewIssue] = useState({ issueType: "", name: "", category_id: "", sprint_id: "", responsible_id: "", priority_id: "", description: "", story_points: "", attachment: "" });

    function handleOpenSelectIType() {
        setIsSelectITypeOpen(true);
    }

    function handleInputChange(event) {
        setNewIssue({ ...newIssue, [event.target.name]: event.target.value });
    }

    function handleCloseSelectIType() {
        setIsSelectITypeOpen(false);
        setNewIssue({ issueType: "",name: "", category_id: "", sprint_id: "", responsible_id: "", priority_id: "", description: "", story_points: "", attachment: "" });
    }

    function handleSubmitIssueType() {


    }
    
    return (
        <div className="Backlog">
            
            <button className="add-issue-btn" onClick={handleOpenSelectIType}>
                Create Issue
            </button>

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

        </div>  
    );

}

export default Backlog;