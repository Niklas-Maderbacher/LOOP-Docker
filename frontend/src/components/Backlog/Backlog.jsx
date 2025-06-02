// Leo Tandl
// LOOP-117
// LOOP-33

import './Backlog.modules.css';
import React, { useState, useEffect, useRef } from 'react';
import { UploadCloud, X, RefreshCw, CheckCircle, AlertCircle } from "lucide-react";
import axios from "axios";


function Backlog() {
    const [isSelectITypeOpen, setIsSelectITypeOpen] = useState(false);
    const [isIssueFormOpen, setIsIssueFormOpen] = useState(false);
    const [isSprintFormOpen, setIsSprintFormOpen] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [uploadStatus, setUploadStatus] = useState(null); // null, 'uploading', 'success', 'error'
  
    // File upload related state
    const [uploads, setUploads] = useState([]);
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef(null);
    const maxFileSize = 100; // Maximum file size in MB
    const maxFileSizeBytes = maxFileSize * 1024 * 1024;

    const [newSprint, setNewSprint] = useState({
        name: "",
        start_date: "",
        end_date: "",
        goal: "",
        project_id: ""

    // Initializes state for the new issue
    const [newIssue, setNewIssue] = useState({ 
        issueType: "", 
        name: "", 
        sprint_id: "", 
        responsible_id: "", 
        priority_id: "", 
        description: "", 
        story_points: "",
        issue_id: null  // To store the ID of the created issue
    });

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
        resetForm();
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
        // Only allow closing if we're not in the middle of uploading files
        if (uploadStatus === 'uploading') {
            alert("Please wait until file uploads complete or cancel the uploads.");
            return;
        }
        
        setIsIssueFormOpen(false);
        resetForm();
    }

    // Function to reset all form state
    function resetForm() {
        setNewIssue({ 
            issueType: "", 
            name: "", 
            sprint_id: "", 
            responsible_id: "", 
            priority_id: "", 
            description: "", 
            story_points: "",
            issue_id: null
        });
        setUploads([]);
        setUploadStatus(null);
        setIsSubmitting(false);
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
        
        setIsSubmitting(true);

        try {
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
            
            // Check if the response is OK
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server error: ${response.status} - ${errorText}`);
            }
            
            // Check the content type
            const contentType = response.headers.get('Content-Type');
            
            // Handle the response based on content type
            let data;
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                // If not JSON, get the response as text and try to parse it
                const text = await response.text();
                try {
                    data = JSON.parse(text);
                } catch (parseError) {
                    console.error("Response is not JSON:", text);
                    throw new Error(`Invalid JSON response: ${text.substring(0, 100)}`);
                }
            }
            
            console.log("Issue created:", data);
            
            // Check if the issue was created successfully and we got an ID back
            if (data && data.id) {
                // Update the issue_id in our state
                setNewIssue(prev => ({ ...prev, issue_id: data.id }));
                
                // If there are files to upload, start uploading them
                if (uploads.length > 0) {
                    setUploadStatus('uploading');
                    await uploadAllFiles(data.id);
                } else {
                    // No files to upload, close the form
                    setIsIssueFormOpen(false);
                    resetForm();
                }
            } else {
                throw new Error("Failed to create issue: No issue ID returned");
            }
        } catch (error) {
            console.error("Error creating issue:", error);
            alert("Failed to create issue: " + error.message);
            setIsSubmitting(false);
        }
    }

    // File upload functions
    const validateFile = (file) => {
        if (file.size > maxFileSizeBytes) {
            return {
                valid: false,
                error: `File exceeds maximum size of ${maxFileSize}MB`,
            };
        }
        return { valid: true };
    };

    const addFiles = (files) => {
        const newUploads = Array.from(files).map((file) => {
            const validation = validateFile(file);
            return {
                id: `${file.name}-${Date.now()}`,
                file,
                progress: 0,
                status: validation.valid ? "pending" : "invalid",
                error: validation.valid ? null : validation.error,
                filename: null
            };
        });

        setUploads((prev) => [...prev, ...newUploads]);

        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    const uploadFile = async (fileItem, issueId) => {
        if (fileItem.status === "invalid") {
            return { success: false, id: fileItem.id };
        }

        // Prepare FormData
        const formData = new FormData();
        formData.append("files", fileItem.file);
        formData.append("issue_id", issueId.toString());

        try {
            const response = await axios.post("http://localhost:8000/api/v1/attachments/", formData, {
                onUploadProgress: (event) => {
                    if (event.total) {
                        const percent = Math.round((event.loaded / event.total) * 100);
                        setUploads((prevUploads) =>
                            prevUploads.map((item) =>
                                item.id === fileItem.id
                                    ? { ...item, progress: percent }
                                    : item
                            )
                        );
                    }
                },
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            if (response.status >= 200 && response.status < 300) {
                const data = response.data;
                const newFilename = data?.uploaded_attachments?.[0]?.filename || data?.filename;

                setUploads((prevUploads) =>
                    prevUploads.map((item) =>
                        item.id === fileItem.id
                            ? {
                                ...item,
                                status: "uploaded",
                                progress: 100,
                                filename: newFilename || item.file.name,
                            }
                            : item
                    )
                );
                return { success: true, id: fileItem.id };
            } else {
                // Handle non-JSON responses
                if (typeof response.data === 'string') {
                    throw new Error(`Upload failed with status ${response.status}: ${response.data.substring(0, 100)}`);
                } else {
                    const errorMsg = response.data?.message || `Upload failed with status ${response.status}`;
                    throw new Error(errorMsg);
                }
            }
        } catch (error) {
            console.error("Upload error:", error);
            // Extract response data for Axios errors
            const errorMessage = error.response 
                ? (typeof error.response.data === 'string' 
                    ? error.response.data.substring(0, 100) 
                    : (error.response.data?.message || `Error ${error.response.status}`))
                : (error.message || "Upload failed");
                
            setUploads((prevUploads) =>
                prevUploads.map((item) =>
                    item.id === fileItem.id
                        ? {
                            ...item,
                            status: "error",
                            error: errorMessage,
                        }
                        : item
                )
            );
            return { success: false, id: fileItem.id };
        }
    };

    const uploadAllFiles = async (issueId) => {
        try {
            // Mark all files as uploading
            setUploads((prevUploads) =>
                prevUploads.map((item) =>
                    item.status === "pending"
                        ? { ...item, status: "uploading" }
                        : item
                )
            );

            // Get all files that need to be uploaded
            const filesToUpload = uploads.filter(
                (item) => item.status === "uploading" || item.status === "pending"
            );

            // Upload all files in parallel
            const results = await Promise.all(
                filesToUpload.map((item) => uploadFile(item, issueId))
            );

            // Check if all uploads were successful
            const allSuccessful = results.every((result) => result.success);
            
            if (allSuccessful) {
                setUploadStatus('success');
                // Close the form after successful uploads
                setTimeout(() => {
                    setIsIssueFormOpen(false);
                    resetForm();
                }, 1000);
            } else {
                setUploadStatus('error');
                // Don't close the form, allow retrying failed uploads
            }
        } catch (error) {
            console.error("Error uploading files:", error);
            setUploadStatus('error');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleRetryUpload = (fileItemId) => {
        setUploads((prevUploads) =>
            prevUploads.map((item) =>
                item.id === fileItemId
                    ? { ...item, status: "pending", progress: 0, error: null }
                    : item
            )
        );
    };

    const handleRemoveFile = (fileItemId) => {
        setUploads((prevUploads) =>
            prevUploads.filter((item) => item.id !== fileItemId)
        );
    };

    const handleFileChange = (event) => {
        if (event.target.files && event.target.files.length > 0) {
            addFiles(event.target.files);
        }
    };

    const handleDragEnter = (event) => {
        event.preventDefault();
        setDragActive(true);
    };

    const handleDragLeave = (event) => {
        event.preventDefault();
        setDragActive(false);
    };

    const handleDragOver = (event) => {
        event.preventDefault();
    };

    const handleDrop = (event) => {
        event.preventDefault();
        setDragActive(false);
        if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
            addFiles(event.dataTransfer.files);
        }
    };

    const formatFileSize = (bytes) => {
        if (bytes === 0) return "0 Bytes";
        const k = 1024;
        const sizes = ["Bytes", "KB", "MB", "GB"];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    };

    // Function to handle retrying all failed uploads
    const handleRetryAllUploads = async () => {
        if (!newIssue.issue_id) {
            alert("Cannot retry uploads: No issue ID available");
            return;
        }

        setUploadStatus('uploading');
        setIsSubmitting(true);
        
        // Reset all failed uploads to pending
        setUploads((prevUploads) =>
            prevUploads.map((item) =>
                item.status === "error"
                    ? { ...item, status: "pending", progress: 0, error: null }
                    : item
            )
        );
        
        // Upload all pending files
        await uploadAllFiles(newIssue.issue_id);
    };

    return (
        <div className="Backlog">
            <button className="add-issue-btn" onClick={handleOpenSelectIType}>
                Create Issue
            </button>

            <button className="add-sprint-btn" onClick={handleOpenSprintForm}>
                Create Sprint
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

                        {/* Story Points field shown only for Epic or Subtask */}
                        {["story", "subtask"].includes(newIssue.issueType.toLowerCase()) && (
                            <input 
                                type="text"  // Text input to prevent the number input spinner
                                name="story_points" 
                                placeholder="Story Points (optional)" 
                                value={newIssue.story_points} 
                                onChange={handleInputChange} 
                            />
                        )}

                        {/* Integrated File Upload */}
                        {newIssue.issueType.toLowerCase() !== "epic" && (
                            <div className="file-upload-container">
                                {/* File input for selection */}
                                <input
                                    type="file"
                                    multiple
                                    onChange={handleFileChange}
                                    className="file-input"
                                    id="file-input"
                                    ref={fileInputRef}
                                    aria-label="File upload"
                                    disabled={isSubmitting}
                                />
                                
                                {/* Label serves as drop zone, and also as a clickable area for the input */}
                                <label
                                    htmlFor="file-input"
                                    onDrop={handleDrop}
                                    onDragOver={handleDragOver}
                                    onDragEnter={handleDragEnter}
                                    onDragLeave={handleDragLeave}
                                    className={`upload-label ${dragActive ? "drag-active" : ""} ${isSubmitting ? "disabled" : ""}`}
                                    aria-label="Drop files here"
                                >
                                    <UploadCloud />
                                    <span>Attach or Drop Files here</span>
                                    <span className="upload-hint">All file types accepted (Max: {maxFileSize}MB)</span>
                                </label>

                                {/* Render upload list */}
                                {uploads.length > 0 && (
                                    <div className="upload-list" role="list" aria-label="File upload list">
                                        {uploads.map((item) => (
                                            <div key={item.id} className="upload-item" role="listitem">
                                                <div className="upload-item-header">
                                                    <div className="file-info">
                                                        <span className="file-name">{item.filename || item.file.name}</span>
                                                        <span className="file-size">{formatFileSize(item.file.size)}</span>
                                                    </div>
                                                    {!isSubmitting && item.status !== "uploading" && (
                                                        <button
                                                            onClick={() => handleRemoveFile(item.id)}
                                                            className="remove-btn"
                                                            aria-label={`Remove ${item.file.name}`}
                                                        >
                                                            <X size={16} />
                                                        </button>
                                                    )}
                                                </div>

                                                {/* Uploading progress */}
                                                {item.status === "uploading" && (
                                                    <div
                                                        className="progress-container"
                                                        role="progressbar"
                                                        aria-valuenow={item.progress}
                                                        aria-valuemin="0"
                                                        aria-valuemax="100"
                                                    >
                                                        <div className="progress-fill" style={{ width: `${item.progress}%` }}></div>
                                                        <span className="progress-text">{item.progress}%</span>
                                                    </div>
                                                )}

                                                {/* Error state */}
                                                {item.status === "error" && (
                                                    <div className="status-container error">
                                                        <AlertCircle size={16} />
                                                        <span className="error-msg">{item.error || "Upload failed"}</span>
                                                        {!isSubmitting && (
                                                            <button
                                                                onClick={() => handleRetryUpload(item.id)}
                                                                className="retry-btn"
                                                                aria-label={`Retry uploading ${item.file.name}`}
                                                            >
                                                                <RefreshCw size={16} />
                                                                <span>Retry</span>
                                                            </button>
                                                        )}
                                                    </div>
                                                )}

                                                {/* Invalid file */}
                                                {item.status === "invalid" && (
                                                    <div className="status-container error">
                                                        <AlertCircle size={16} />
                                                        <span className="error-msg">{item.error}</span>
                                                    </div>
                                                )}

                                                {/* Pending */}
                                                {item.status === "pending" && (
                                                    <div className="status-container pending">
                                                        <span className="pending-msg">Ready to upload</span>
                                                    </div>
                                                )}

                                                {/* Uploaded */}
                                                {item.status === "uploaded" && (
                                                    <div className="status-container success">
                                                        <CheckCircle size={16} />
                                                        <span className="success-msg">Upload complete</span>
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Upload Status Information */}
                        {uploadStatus === 'error' && (
                            <div className="upload-status error">
                                <AlertCircle size={16} />
                                <span>Some files failed to upload</span>
                                <button onClick={handleRetryAllUploads} className="retry-all-btn">
                                    <RefreshCw size={16} />
                                    <span>Retry Failed Uploads</span>
                                </button>
                            </div>
                        )}

                        {uploadStatus === 'success' && (
                            <div className="upload-status success">
                                <CheckCircle size={16} />
                                <span>All files uploaded successfully</span>
                            </div>
                        )}

                        <div className="modal-buttons">
                            <button 
                                onClick={handleSubmitIssueForm} 
                                disabled={isSubmitting}
                                className={isSubmitting ? "disabled" : ""}
                            >
                                {isSubmitting ? "Creating..." : "Create issue"}
                            </button>
                            <button 
                                onClick={handleCloseIssueForm}
                                disabled={isSubmitting && uploadStatus === 'uploading'}
                                className={isSubmitting && uploadStatus === 'uploading' ? "disabled" : ""}
                            >
                                Cancel
                            </button>
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
