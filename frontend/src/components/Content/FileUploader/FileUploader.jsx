import React, { useState } from "react";
import { UploadCloud, X } from "lucide-react";
import './FileUploader.modules.css';

export const Card = ({ children, className = "" }) => {
    return <div className={`card ${className}`}>{children}</div>;
};

export const CardContent = ({ children, className = "" }) => {
    return <div className={`card-content ${className}`}>{children}</div>;
};

const FileUpload = () => {
    // Each upload is an object with a unique id, the file itself, progress, and status.
    // status: 'uploading' | 'uploaded' | 'error'
    const [uploads, setUploads] = useState([]);

    // Adds files to the state and immediately starts uploading them.
    const addFiles = (files) => {
        const newUploads = files.map((file) => ({
            id: `${file.name}-${Date.now()}-${Math.random()}`,
            file,
            progress: 0,
            status: "uploading",
        }));
        setUploads((prev) => [...prev, ...newUploads]);
        newUploads.forEach(uploadFile);
    };

    // Uses XMLHttpRequest to upload a single file and update its progress.
    const uploadFile = (fileItem) => {
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
            } else {
                setUploads((prevUploads) =>
                    prevUploads.map((item) =>
                        item.id === fileItem.id ? { ...item, status: "error" } : item
                    )
                );
            }
        };

        xhr.onerror = () => {
            setUploads((prevUploads) =>
                prevUploads.map((item) =>
                    item.id === fileItem.id ? { ...item, status: "error" } : item
                )
            );
        };

        xhr.send(formData);
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
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
};

export default FileUpload;
