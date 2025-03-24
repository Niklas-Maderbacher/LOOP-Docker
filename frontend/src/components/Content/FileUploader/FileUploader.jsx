import React, { useState, useRef, useEffect } from "react";
import { UploadCloud, X, Send, RefreshCw, CheckCircle, AlertCircle } from "lucide-react";
import './FileUploader.modules.css';

const fileServerIP = process.env.REACT_APP_FILE_SERVER_IP;
const fileServerPort = process.env.REACT_APP_FILE_SERVER_PORT;

const apiEndpoint = `http://${fileServerIP}:${fileServerPort}/dump`;
const deleteEndpoint = `http://${fileServerIP}:${fileServerPort}/attachments`;

/**
 * A reusable card component for wrapping content.
 * @component
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Content to be rendered inside the card
 * @param {string} [props.className=""] - Additional CSS classes for styling
 * @returns {JSX.Element} Card component
 */
export const Card = ({ children, className = "" }) => {
    return <div className={`card ${className}`}>{children}</div>;
};

/**
 * A container component for card content with proper padding and spacing.
 * @component
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Content to be rendered inside the card content area
 * @param {string} [props.className=""] - Additional CSS classes for styling
 * @returns {JSX.Element} CardContent component
 */
export const CardContent = ({ children, className = "" }) => {
    return <div className={`card-content ${className}`}>{children}</div>;
};

/**
 * Main file upload component with drag-and-drop functionality, progress tracking,
 * and server communication capabilities.
 * @component
 * @param {Object} props - Component props
 * @param {number} [props.maxFileSize=100] - Maximum allowed file size in megabytes
 * @returns {JSX.Element} FileUpload component
 */
const FileUpload = ({ maxFileSize = 100 }) => {
    const [uploads, setUploads] = useState([]);
    const [isUploading, setIsUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef(null);
    const activeXhrRefs = useRef({});

    const maxFileSizeBytes = maxFileSize * 1024 * 1024;

    useEffect(() => {
        return () => {
            Object.values(activeXhrRefs.current).forEach(xhr => {
                if (xhr) {
                    xhr.abort();
                }
            });
        };
    }, []);

    /**
     * Validates a file against size constraints.
     * @param {File} file - File object to validate
     * @returns {Object} Validation result
     * @property {boolean} valid - Indicates if the file is valid
     * @property {string|null} error - Error message if invalid
     */
    const validateFile = (file) => {
        if (file.size > maxFileSizeBytes) {
            return {
                valid: false,
                error: `File exceeds maximum size of ${maxFileSize}MB`
            };
        }
        return { valid: true };
    };

    /**
     * Adds files to the upload queue and performs initial validation.
     * @param {FileList} files - List of files to add to the upload queue
     */
    const addFiles = (files) => {
        const newUploads = Array.from(files).map((file) => {
            const validation = validateFile(file);
            
            return {
                id: `${file.name}-${Date.now()}`,
                file,
                progress: 0,
                status: validation.valid ? "pending" : "invalid",
                error: validation.valid ? null : validation.error,
                response: null,
                projectId: 10,
                issueId: 10
            };
        });

        setUploads((prev) => [...prev, ...newUploads]);
        
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    /**
     * Handles file upload to the server using XMLHttpRequest.
     * @param {Object} fileItem - File item from the uploads state
     * @returns {Promise} Promise that resolves when upload completes
     */
    const uploadFile = (fileItem) => {
        return new Promise((resolve, reject) => {
            if (fileItem.status === "invalid") {
                resolve();
                return;
            }

            const formData = new FormData();
            formData.append("file", fileItem.file);
            formData.append("project_id", fileItem.projectId);
            formData.append("issue_id", fileItem.issueId);

            const xhr = new XMLHttpRequest();
            activeXhrRefs.current[fileItem.id] = xhr;
            
            xhr.open("POST", apiEndpoint);

            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percent = Math.round((event.loaded / event.total) * 100);
                    setUploads((prevUploads) =>
                        prevUploads.map((item) =>
                            item.id === fileItem.id ? { ...item, progress: percent } : item
                        )
                    );
                }
            };

            xhr.onload = () => {
                delete activeXhrRefs.current[fileItem.id];
                
                let response = null;
                try {
                    response = JSON.parse(xhr.responseText);
                } catch (e) {
                    response = xhr.responseText || "No response data";
                }

                if (xhr.status >= 200 && xhr.status < 300) {
                    setUploads((prevUploads) =>
                        prevUploads.map((item) =>
                            item.id === fileItem.id ? { 
                                ...item, 
                                status: "uploaded", 
                                progress: 100,
                                response
                            } : item
                        )
                    );
                    resolve(response);
                } else {
                    const errorMsg = response?.message || `Upload failed with status ${xhr.status}`;
                    setUploads((prevUploads) =>
                        prevUploads.map((item) =>
                            item.id === fileItem.id ? { 
                                ...item, 
                                status: "error",
                                error: errorMsg,
                                response 
                            } : item
                        )
                    );
                    reject(new Error(errorMsg));
                }
            };

            xhr.onerror = () => {
                delete activeXhrRefs.current[fileItem.id];
                
                setUploads((prevUploads) =>
                    prevUploads.map((item) =>
                        item.id === fileItem.id ? { 
                            ...item, 
                            status: "error",
                            error: "Network error occurred"
                        } : item
                    )
                );
                reject(new Error("Network error occurred"));
            };

            xhr.onabort = () => {
                delete activeXhrRefs.current[fileItem.id];
                
                setUploads((prevUploads) =>
                    prevUploads.map((item) =>
                        item.id === fileItem.id ? { 
                            ...item, 
                            status: "pending", 
                            progress: 0,
                            error: "Upload cancelled"
                        } : item
                    )
                );
                reject(new Error("Upload aborted"));
            };

            xhr.send(formData);
        });
    };

    /**
     * Deletes a file from the server and updates the uploads state.
     * @param {Object} fileItem - File item to delete
     * @returns {Promise} Promise that resolves when deletion completes
     */
    const deleteFile = (fileItem) => {
        return new Promise((resolve, reject) => {
            setUploads((prevUploads) =>
                prevUploads.map((item) =>
                    item.id === fileItem.id ? { ...item, status: "deleting" } : item
                )
            );

            const deleteUrl = `${deleteEndpoint}/${fileItem.projectId}/${fileItem.issueId}/${encodeURIComponent(fileItem.file.name)}`;
            
            const xhr = new XMLHttpRequest();
            activeXhrRefs.current[fileItem.id] = xhr;
            
            xhr.open("DELETE", deleteUrl);
            
            xhr.onload = () => {
                delete activeXhrRefs.current[fileItem.id];
                
                if (xhr.status >= 200 && xhr.status < 300) {
                    setUploads((prevUploads) =>
                        prevUploads.map((item) =>
                            item.id === fileItem.id ? { 
                                ...item, 
                                status: "deleted",
                                message: "File deleted successfully"
                            } : item
                        )
                    );
                    
                    setTimeout(() => {
                        setUploads((prevUploads) =>
                            prevUploads.filter((item) => item.id !== fileItem.id)
                        );
                    }, 3000);
                    
                    resolve();
                } else {
                    let errorMsg;
                    try {
                        const response = JSON.parse(xhr.responseText);
                        errorMsg = response?.message || `Delete failed with status ${xhr.status}`;
                    } catch (e) {
                        errorMsg = `Delete failed with status ${xhr.status}`;
                    }
                    
                    setUploads((prevUploads) =>
                        prevUploads.map((item) =>
                            item.id === fileItem.id ? { 
                                ...item, 
                                status: "error",
                                error: errorMsg
                            } : item
                        )
                    );
                    reject(new Error(errorMsg));
                }
            };
            
            xhr.onerror = () => {
                delete activeXhrRefs.current[fileItem.id];
                
                setUploads((prevUploads) =>
                    prevUploads.map((item) =>
                        item.id === fileItem.id ? { 
                            ...item, 
                            status: "error",
                            error: "Network error occurred while deleting"
                        } : item
                    )
                );
                reject(new Error("Network error occurred"));
            };
            
            xhr.send();
        });
    };

    /**
     * Handles retry of failed uploads by resetting the file status and progress.
     * @param {string} fileItemId - ID of the file item to retry
     */
    const handleRetryUpload = (fileItemId) => {
        setUploads(prevUploads =>
            prevUploads.map(item =>
                item.id === fileItemId ? { ...item, status: "pending", progress: 0, error: null } : item
            )
        );
    };

    /**
     * Initiates upload of all pending files and manages upload state.
     */
    const handleConfirmUpload = async () => {
        const pendingUploads = uploads.filter(item => item.status === "pending");
        
        if (pendingUploads.length === 0) return;
        
        setIsUploading(true);
        
        setUploads(prevUploads =>
            prevUploads.map(item =>
                item.status === "pending" ? { ...item, status: "uploading" } : item
            )
        );
        
        const uploadPromises = pendingUploads.map(fileItem => {
            return uploadFile(fileItem).catch(error => {
                console.error(`Error uploading ${fileItem.file.name}:`, error);
                return null;
            });
        });
        
        try {
            const results = await Promise.all(uploadPromises);
            console.log("Upload results:", results.filter(Boolean));
        } catch (error) {
            console.error("Fatal upload error:", error);
        } finally {
            setIsUploading(false);
        }
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

    /**
     * Removes a file from the upload queue and cancels any active upload.
     * @param {Object} fileItem - File item to remove
     */
    const handleRemoveFile = async (fileItem) => {
        if (activeXhrRefs.current[fileItem.id]) {
            activeXhrRefs.current[fileItem.id].abort();
            delete activeXhrRefs.current[fileItem.id];
        }
        
        if (fileItem.status === "uploaded") {
            try {
                await deleteFile(fileItem);
            } catch (error) {
                console.error(`Error deleting ${fileItem.file.name}:`, error);
            }
        } else {
            setUploads((prevUploads) =>
                prevUploads.filter((item) => item.id !== fileItem.id)
            );
        }
    };

    /**
     * Formats file size in bytes to human-readable string.
     * @param {number} bytes - File size in bytes
     * @returns {string} Formatted file size string
     */
    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const hasPendingFiles = uploads.some(item => item.status === "pending");

    return (
        <Card>
            <CardContent>
                <input 
                    type="file" 
                    multiple 
                    onChange={handleFileChange} 
                    className="file-input" 
                    id="file-input"
                    ref={fileInputRef}
                    aria-label="File upload"
                />
                <label 
                    htmlFor="file-input" 
                    onDrop={handleDrop} 
                    onDragOver={handleDragOver}
                    onDragEnter={handleDragEnter}
                    onDragLeave={handleDragLeave}
                    className={`upload-label ${dragActive ? 'drag-active' : ''}`}
                    aria-label="Drop files here"
                >
                    <UploadCloud />
                    <span>Attach or Drop Files here</span>
                    <span className="upload-hint">All file types accepted (Max: {maxFileSize}MB)</span>
                </label>

                {uploads.length > 0 && (
                    <div className="upload-list" role="list" aria-label="File upload list">
                        {uploads.map((item) => (
                            <div key={item.id} className="upload-item" role="listitem">
                                <div className="upload-item-header">
                                    <div className="file-info">
                                        <span className="file-name">{item.file.name}</span>
                                        <span className="file-size">{formatFileSize(item.file.size)}</span>
                                    </div>
                                    {item.status !== "uploading" && item.status !== "deleting" && (
                                        <button 
                                            onClick={() => handleRemoveFile(item)} 
                                            className="remove-btn"
                                            aria-label={`Remove ${item.file.name}`}
                                        >
                                            <X size={16} />
                                        </button>
                                    )}
                                </div>
                                
                                {item.status === "uploading" && (
                                    <div className="progress-container" role="progressbar" aria-valuenow={item.progress} aria-valuemin="0" aria-valuemax="100">
                                        <div className="progress-fill" style={{ width: `${item.progress}%` }}></div>
                                        <span className="progress-text">{item.progress}%</span>
                                    </div>
                                )}
                                
                                {item.status === "deleting" && (
                                    <div className="progress-container" role="status">
                                        <div className="progress-fill indeterminate"></div>
                                        <span className="progress-text">Deleting...</span>
                                    </div>
                                )}
                                
                                {item.status === "error" && (
                                    <div className="status-container error">
                                        <AlertCircle size={16} />
                                        <span className="error-msg">{item.error || "Upload failed"}</span>
                                        <button 
                                            onClick={() => handleRetryUpload(item.id)} 
                                            className="retry-btn"
                                            aria-label={`Retry uploading ${item.file.name}`}
                                        >
                                            <RefreshCw size={16} />
                                            <span>Retry</span>
                                        </button>
                                    </div>
                                )}
                                
                                {item.status === "invalid" && (
                                    <div className="status-container error">
                                        <AlertCircle size={16} />
                                        <span className="error-msg">{item.error}</span>
                                    </div>
                                )}
                                
                                {item.status === "pending" && (
                                    <div className="status-container pending">
                                        <span className="pending-msg">Ready to upload</span>
                                    </div>
                                )}
                                
                                {item.status === "uploaded" && (
                                    <div className="status-container success">
                                        <CheckCircle size={16} />
                                        <span className="success-msg">Upload complete</span>
                                    </div>
                                )}
                                
                                {item.status === "deleted" && (
                                    <div className="status-container success">
                                        <CheckCircle size={16} />
                                        <span className="success-msg">{item.message || "File deleted successfully"}</span>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
                
                {hasPendingFiles && (
                    <button 
                        onClick={handleConfirmUpload} 
                        disabled={isUploading} 
                        className="confirm-upload-btn"
                        aria-label="Confirm upload"
                    >
                        <Send size={16} />
                        <span>{isUploading ? "Uploading..." : "Confirm Upload"}</span>
                    </button>
                )}
            </CardContent>
        </Card>
    );
};

export default FileUpload;
