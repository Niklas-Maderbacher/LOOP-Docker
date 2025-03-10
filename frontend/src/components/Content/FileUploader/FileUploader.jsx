import React, { useState, useRef, useEffect } from "react";
import { UploadCloud, X, Send, RefreshCw, CheckCircle, AlertCircle } from "lucide-react";
import './FileUploader.modules.css';

export const Card = ({ children, className = "" }) => {
    return <div className={`card ${className}`}>{children}</div>;
};

export const CardContent = ({ children, className = "" }) => {
    return <div className={`card-content ${className}`}>{children}</div>;
};

const FileUpload = ({ apiEndpoint = "http://172.31.180.49:5000/dump", maxFileSize = 100 }) => {
    // Each upload is an object with a unique id, the file itself, progress, status, and error message.
    // status: 'pending' | 'uploading' | 'uploaded' | 'error' | 'invalid'
    const [uploads, setUploads] = useState([]);
    const [isUploading, setIsUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef(null);
    const activeXhrRefs = useRef({});

    // Convert MB to bytes
    const maxFileSizeBytes = maxFileSize * 1024 * 1024;

    // Clean up any ongoing uploads when component unmounts
    useEffect(() => {
        return () => {
            // Abort all active uploads when component unmounts
            Object.values(activeXhrRefs.current).forEach(xhr => {
                if (xhr) {
                    xhr.abort();
                }
            });
        };
    }, []);

    // Validate files
    const validateFile = (file) => {
        if (file.size > maxFileSizeBytes) {
            return {
                valid: false,
                error: `File exceeds maximum size of ${maxFileSize}MB`
            };
        }
        return { valid: true };
    };

    // Adds files to the state without starting upload
    const addFiles = (files) => {
        const newUploads = Array.from(files).map((file) => {
            const validation = validateFile(file);
            
            return {
                id: `${file.name}-${Date.now()}`,
                file,
                progress: 0,
                status: validation.valid ? "pending" : "invalid",
                error: validation.valid ? null : validation.error,
                response: null
            };
        });

        setUploads((prev) => [...prev, ...newUploads]);
        
        // Reset the file input so the same files can be selected again
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    // Uses XMLHttpRequest to upload a single file and update its progress.
    const uploadFile = (fileItem) => {
        return new Promise((resolve, reject) => {
            // Skip invalid files
            if (fileItem.status === "invalid") {
                resolve();
                return;
            }

            const formData = new FormData();
            formData.append("file", fileItem.file);  // Changed key name to "file"
            formData.append("project_id", 10);       // Add project_id
            formData.append("issue_id", 10);         // Add issue_id

            const xhr = new XMLHttpRequest();

            // Store the xhr reference for cleanup
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
                // Clean up xhr reference
                delete activeXhrRefs.current[fileItem.id];
                
                let response = null;
                try {
                    response = JSON.parse(xhr.responseText);
                } catch (e) {
                    // If it's not JSON, store the raw response
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
                // Clean up xhr reference
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
                // Clean up xhr reference
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

    // Retry a failed upload
    const handleRetryUpload = (fileItemId) => {
        // Reset the file to pending status
        setUploads(prevUploads =>
            prevUploads.map(item =>
                item.id === fileItemId ? { ...item, status: "pending", progress: 0, error: null } : item
            )
        );
    };

    // Triggered when confirm button is clicked
    const handleConfirmUpload = async () => {
        const pendingUploads = uploads.filter(item => item.status === "pending");
        
        if (pendingUploads.length === 0) return;
        
        setIsUploading(true);
        
        // Mark all pending files as uploading
        setUploads(prevUploads =>
            prevUploads.map(item =>
                item.status === "pending" ? { ...item, status: "uploading" } : item
            )
        );
        
        // Upload each file
        const uploadPromises = pendingUploads.map(fileItem => {
            return uploadFile(fileItem).catch(error => {
                console.error(`Error uploading ${fileItem.file.name}:`, error);
                // We're catching errors here so Promise.all continues with other uploads
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

    // Called when files are selected using the file input.
    const handleFileChange = (event) => {
        if (event.target.files && event.target.files.length > 0) {
            addFiles(event.target.files);
        }
    };

    // Drag and drop handlers
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

    // Called when files are dropped onto the drop area.
    const handleDrop = (event) => {
        event.preventDefault();
        setDragActive(false);
        if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
            addFiles(event.dataTransfer.files);
        }
    };

    // Remove the file from the state.
    const handleRemoveFile = (id) => {
        // If there's an active upload, abort it
        if (activeXhrRefs.current[id]) {
            activeXhrRefs.current[id].abort();
            delete activeXhrRefs.current[id];
        }
        
        setUploads((prevUploads) =>
            prevUploads.filter((fileItem) => fileItem.id !== id)
        );
    };

    // Get file size in a human-readable format
    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    // Check if there are any pending files to upload
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
                                    {item.status !== "uploading" && (
                                        <button 
                                            onClick={() => handleRemoveFile(item.id)} 
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
                            </div>
                        ))}
                    </div>
                )}
                
                {/* Confirm button */}
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
