import React, { useState } from "react";
import { UploadCloud, X } from "lucide-react";

export const Card = ({ children, className = "" }) => {
  return (
    <div className={`bg-white shadow-lg rounded-2xl p-4 ${className}`}>
      {children}
    </div>
  );
};

export const CardContent = ({ children, className = "" }) => {
  return <div className={`p-2 ${className}`}>{children}</div>;
};

const FileUpload = () => {
  // Each upload is an object with a unique id, the file itself, progress, and status.
  // status: 'uploading' | 'uploaded' | 'error'
  const [uploads, setUploads] = useState([]);

  // Adds files to the state and immediately starts uploading them.
  const addFiles = (files) => {
    const newUploads = files.map((file) => ({
      id: `${file.name}-${Date.now()}-${Math.random()}`, // simple unique id
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
    xhr.open("POST", "http://localhost:8000/upload");

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
            item.id === fileItem.id
              ? { ...item, status: "uploaded", progress: 100 }
              : item
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

  // Remove the file from the state. You could also call a backend delete endpoint here if needed.
  const handleRemoveFile = (id) => {
    setUploads((prevUploads) =>
      prevUploads.filter((fileItem) => fileItem.id !== id)
    );
  };

  return (
    <Card className="p-4 w-full max-w-lg mx-auto mt-5">
      <CardContent>
        {/* Hidden file input */}
        <input
          type="file"
          multiple
          onChange={handleFileChange}
          className="hidden"
          id="file-input"
        />
        {/* Label acts as both a click-to-upload and a drop area */}
        <label
          htmlFor="file-input"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          className="cursor-pointer flex items-center space-x-2 border p-2 rounded-lg bg-gray-100 hover:bg-gray-200"
        >
          <UploadCloud />
          <span>Attach Files and Images (Drag & Drop Supported)</span>
        </label>

        {/* List of files with progress bars and removal buttons */}
        <div className="mt-4 space-y-2">
          {uploads.map((item) => (
            <div key={item.id} className="border p-2 rounded-lg">
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm text-gray-700">{item.file.name}</span>
                {/* Only show the removal (X) button when not uploading */}
                {item.status !== "uploading" && (
                  <button
                    onClick={() => handleRemoveFile(item.id)}
                    className="text-red-500"
                  >
                    <X size={16} />
                  </button>
                )}
              </div>
              {item.status === "uploading" && (
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-500 h-2 rounded-full"
                    style={{ width: `${item.progress}%` }}
                  ></div>
                </div>
              )}
              {item.status === "error" && (
                <span className="text-xs text-red-500">Upload failed</span>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default FileUpload;
