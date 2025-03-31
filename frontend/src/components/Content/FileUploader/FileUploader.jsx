import React, { useState, useRef, useEffect } from "react";
import axios from "axios";  // <-- axios import
import { UploadCloud, X, Send, RefreshCw, CheckCircle, AlertCircle } from "lucide-react";
import './FileUploader.modules.css';

const apiBaseUrl = "http://localhost:8000";
const apiEndpoint = `${apiBaseUrl}/attachments`;
const deleteEndpoint = `${apiBaseUrl}/attachments`;

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
 * and server communication via Axios.
 *
 * @component
 * @param {number} [props.maxFileSize=100] - Maximum allowed file size in megabytes
 * @param {number} props.projectId - ID of the project
 * @param {number} props.issueId - ID of the issue
 * @returns {JSX.Element} FileUpload component
 */
const FileUpload = ({ maxFileSize = 100, projectId, issueId }) => {
  const [uploads, setUploads] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  // Convert MB to bytes
  const maxFileSizeBytes = maxFileSize * 1024 * 1024;

  // Cleanup if component unmounts
  useEffect(() => {
    return () => {
      // Optional: If you had any ongoing axios requests you'd want to cancel them here
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
        error: `File exceeds maximum size of ${maxFileSize}MB`,
      };
    }
    return { valid: true };
  };

  /**
   * Adds files to the upload queue and performs initial validation.
   * @param {FileList|File[]} files - List of files to add
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
        filename: null,
        projectId,
        issueId,
      };
    });

    setUploads((prev) => [...prev, ...newUploads]);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  /**
   * Uploads a single file to the server using Axios.
   * @param {Object} fileItem - File item to upload
   * @returns {Promise<void>}
   */
  const uploadFile = async (fileItem) => {
    if (fileItem.status === "invalid") {
      return;
    }

    // Prepare FormData
    const formData = new FormData();
    formData.append("files", fileItem.file);
    formData.append("project_id", fileItem.projectId.toString());
    formData.append("issue_id", fileItem.issueId.toString());

    try {
      const response = await axios.post(apiEndpoint, formData, {
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
        // If you need a specific header for multipart, but usually this is fine
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.status >= 200 && response.status < 300) {
        // We expect a JSON response with "uploaded_attachments"
        const data = response.data;
        // For multi-file uploads in a single request, pick the correct array item
        // but in your code, "uploaded_attachments" might be an array
        // or something else. Adjust if needed:
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
      } else {
        const errorMsg = response.data?.message || `Upload failed with status ${response.status}`;
        throw new Error(errorMsg);
      }
    } catch (error) {
      console.error("Upload error:", error);
      setUploads((prevUploads) =>
        prevUploads.map((item) =>
          item.id === fileItem.id
            ? {
                ...item,
                status: "error",
                error: error.message || "Upload failed",
              }
            : item
        )
      );
    }
  };

  /**
   * Initiates upload of all pending files.
   */
  const handleConfirmUpload = async () => {
    const pendingUploads = uploads.filter((item) => item.status === "pending");
    if (pendingUploads.length === 0) return;

    setIsUploading(true);
    // Mark all pending files as "uploading"
    setUploads((prevUploads) =>
      prevUploads.map((item) =>
        item.status === "pending" ? { ...item, status: "uploading" } : item
      )
    );

    // Perform uploads in parallel
    await Promise.all(pendingUploads.map(uploadFile));

    setIsUploading(false);
  };

  /**
   * Deletes an uploaded file from the server and the database.
   * @param {Object} fileItem - File item to delete
   */
  const deleteFile = async (fileItem) => {
    try {
      setUploads((prevUploads) =>
        prevUploads.map((item) =>
          item.id === fileItem.id ? { ...item, status: "deleting" } : item
        )
      );

      const encodedFilename = encodeURIComponent(fileItem.filename);
      const deleteUrl = `${deleteEndpoint}/${fileItem.projectId}/${fileItem.issueId}/${encodedFilename}`;

      const response = await axios.delete(deleteUrl);
      if (response.status >= 200 && response.status < 300) {
        // Mark as deleted, remove from list after a short delay
        setUploads((prevUploads) =>
          prevUploads.map((item) =>
            item.id === fileItem.id
              ? {
                  ...item,
                  status: "deleted",
                  message: "File deleted successfully",
                }
              : item
          )
        );
        setTimeout(() => {
          setUploads((prevUploads) =>
            prevUploads.filter((item) => item.id !== fileItem.id)
          );
        }, 3000);
      } else {
        const errorMsg = response.data?.message || `Delete failed with status ${response.status}`;
        throw new Error(errorMsg);
      }
    } catch (error) {
      console.error("Delete error:", error);
      setUploads((prevUploads) =>
        prevUploads.map((item) =>
          item.id === fileItem.id
            ? {
                ...item,
                status: "error",
                error: error.message || "Delete failed",
              }
            : item
        )
      );
    }
  };

  /**
   * Retries a failed upload by resetting status.
   * @param {string} fileItemId - ID of the file item to retry
   */
  const handleRetryUpload = (fileItemId) => {
    setUploads((prevUploads) =>
      prevUploads.map((item) =>
        item.id === fileItemId
          ? { ...item, status: "pending", progress: 0, error: null }
          : item
      )
    );
  };

  /**
   * Removes a file from the queue (if it's uploaded, tries to delete from server first).
   * @param {Object} fileItem - File item to remove
   */
  const handleRemoveFile = async (fileItem) => {
    // If it's only pending or failed, just remove from list
    if (fileItem.status === "uploaded") {
      await deleteFile(fileItem);
    } else {
      // If mid-upload or error, just remove
      setUploads((prevUploads) =>
        prevUploads.filter((item) => item.id !== fileItem.id)
      );
    }
  };

  /**
   * Handles file selection from <input type="file">.
   * @param {Event} event
   */
  const handleFileChange = (event) => {
    if (event.target.files && event.target.files.length > 0) {
      addFiles(event.target.files);
    }
  };

  /**
   * Drag/Drop events
   */
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
   * Helper: Format file size in bytes to a human-readable string.
   * @param {number} bytes
   * @returns {string}
   */
  const formatFileSize = (bytes) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const hasPendingFiles = uploads.some((item) => item.status === "pending");

  return (
    <Card>
      <CardContent>
        {/* File input for selection */}
        <input
          type="file"
          multiple
          onChange={handleFileChange}
          className="file-input"
          id="file-input"
          ref={fileInputRef}
          aria-label="File upload"
        />
        {/* Label serves as drop zone, and also as a clickable area for the input */}
        <label
          htmlFor="file-input"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          className={`upload-label ${dragActive ? "drag-active" : ""}`}
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

                {/* Deleting progress */}
                {item.status === "deleting" && (
                  <div className="progress-container" role="status">
                    <div className="progress-fill indeterminate"></div>
                    <span className="progress-text">Deleting...</span>
                  </div>
                )}

                {/* Error state */}
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

                {/* Deleted */}
                {item.status === "deleted" && (
                  <div className="status-container success">
                    <CheckCircle size={16} />
                    <span className="success-msg">
                      {item.message || "File deleted successfully"}
                    </span>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Button to confirm upload */}
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
