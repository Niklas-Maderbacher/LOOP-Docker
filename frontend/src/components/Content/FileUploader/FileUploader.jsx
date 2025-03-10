import React, { useState } from "react";
import { UploadCloud, X, Send } from "lucide-react";
import './FileUploader.modules.css';

export const Card = ({ children, className = "" }) => {
    return <div className={`card ${className}`}>{children}</div>;
};

export const CardContent = ({ children, className = "" }) => {
    return <div className={`card-content ${className}`}>{children}</div>;
};

const FileUpload = () => {
    // Each upload is an object with a unique id, the file itself, progress, and status.
    // status: 'pending' | 'uploading' | 'uploaded' | 'error'
    const [uploads, setUploads] = useState([]);
    const [isUploading, setIsUploading] = useState(false);

    const addFiles = (files) => {
        const newUploads = files.map((file) => ({
            id: `${file.name}-${Date.now()}`,
            file,
            progress: 0,
            status: "pending",
        }));
        setUploads((prev) => [...prev, ...newUploads]);
    };

    // Uses XMLHttpRequest to upload a single file and update its progress.
    const uploadFile = (fileItem) => {
        return new Promise((resolve, reject) => {
            const formData = new FormData();
            formData.append("files", fileItem.file);

            const xhr = new XMLHttpRequest();
            xhr.open("POST", "http://localhost:5000/image");

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
                if (xhr.status === 200) {
                    setUploads((prevUploads) =>
                        prevUploads.map((item) =>
                            item.id === fileItem.id ? { ...item, status: "uploaded", progress: 100 } : item
                        )
                    );
                    resolve();
                } else {
                    setUploads((prevUploads) =>
                        prevUploads.map((item) =>
                            item.id === fileItem.id ? { ...item, status: "error" } : item
                        )
                    );
                    reject(new Error(`Upload failed with status ${xhr.status}`));
                }
            };

            xhr.onerror = () => {
                setUploads((prevUploads) =>
                    prevUploads.map((item) =>
                        item.id === fileItem.id ? { ...item, status: "error" } : item
                    )
                );
                reject(new Error("Network error occurred"));
            };

            xhr.send(formData);
        });
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
            return uploadFile(fileItem);
        });

        try {
            await Promise.all(uploadPromises);
        } catch (error) {
            console.error("Some uploads failed:", error);
        } finally {
            setIsUploading(false);
        }
    };

    // Called when files are selected using the file input.
    const handleFileChange = (event) => {
        const files = Array.from(event.target.files);
        addFiles(files);
    };

    // Called when files are dropped onto the drop area.
    const handleDrop = (event) => {
        event.preventDefault();
        const files = Array.from(event.dataTransfer.files);
        addFiles(files);
    };

    const handleDragOver = (event) => {
        event.preventDefault();
    };

    // Remove the file from the state.
    const handleRemoveFile = (id) => {
        setUploads((prevUploads) =>
            prevUploads.filter((fileItem) => fileItem.id !== id)
        );
    };

    // Check if there are any pending files to upload
    const hasPendingFiles = uploads.some(item => item.status === "pending");

    return (
        <Card>
            <CardContent>
                <input type="file" multiple onChange={handleFileChange} className="file-input" id="file-input"/>
                <label htmlFor="file-input" onDrop={handleDrop} onDragOver={handleDragOver} className="upload-label">
                    <UploadCloud />
                    <span>Attach or Drop Files here</span>
                </label>

                <div className="upload-list">
                    {uploads.map((item) => (
                        <div key={item.id} className="upload-item">
                            <div className="upload-item-header">
                                <span className="file-name">{item.file.name}</span>
                                {item.status !== "uploading" && (
                                    <button onClick={() => handleRemoveFile(item.id)} className="remove-btn">
                                        <X size={16} />
                                    </button>
                                )}
                            </div>
                            {item.status === "uploading" && (
                                <div className="progress-container">
                                    <div className="progress-fill" style={{ width: `${item.progress}%` }}></div>
                                </div>
                            )}
                            {item.status === "error" && (
                                <span className="error-msg">Upload failed</span>
                            )}
                            {item.status === "pending" && (
                                <span className="pending-msg">Ready to upload</span>
                            )}
                        </div>
                    ))}
                </div>
                
                {/* Confirm button */}
                {hasPendingFiles && (
                    <button 
                        onClick={handleConfirmUpload} 
                        disabled={isUploading} 
                        className="confirm-upload-btn"
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
