// LOOP-124
import './EditIssueForm.modules.css';
import React, { useState, useEffect } from "react";
import axios from "axios";

const EditIssueForm = ({ issueId, onClose }) => {
  const [issue, setIssue] = useState(null);
  const [options, setOptions] = useState({
    categories: [],
    sprints: [],
    states: [],
    users: [],
    priorities: [],
  });

  const handleSave = async () => {
    try {
      const cleanedIssue = Object.fromEntries(
        Object.entries(issue).map(([key, value]) => [
          key,
          value === "" ? null : value,
        ])
      );

      await axios.put(`http://localhost:8000/api/v1/issues/${issueId}`, cleanedIssue);
      console.log("Issue updated successfully!");
      onClose(); 
    } catch (error) {
      console.error("Error updating issue:", error);
      alert("Failed to update the issue.");
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [{ data: issueData }, categories, sprints, states, users, priorities] = await Promise.all([
          axios.get(`http://localhost:8000/api/v1/issues/${issueId}`),
          axios.get("http://localhost:8000/api/v1/categories"),
          axios.get("http://localhost:8000/api/v1/sprints"),
          axios.get("http://localhost:8000/api/v1/states"),
          axios.get("http://localhost:8000/api/v1/users/get_all_users"),
          axios.get("http://localhost:8000/api/v1/priorities"),
        ]);

        setIssue(issueData);
        setOptions({
          categories: categories.data,
          sprints: sprints.data,
          states: states.data,
          users: users.data,
          priorities: priorities.data,
        });
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [issueId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setIssue((prev) => ({ ...prev, [name]: value }));
  };

  if (!issue) return <p>Loading...</p>;

  return (
    <div className="modal-container">
      <div className="modal">
        <h2 className="modal-title">Edit Issue</h2>

        <form className="form">
          <div className="form-sections">
            {/* Grunddaten */}
            <div className="form-section">
              <h3 className="section-title">Grunddaten</h3>
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="name">Issue Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={issue.name}
                    onChange={handleChange}
                    placeholder="Issue Name"
                    className="form-input"
                  />
              </div>
              <div className="form-group">
                <label htmlFor="story_points">Story Points</label>
                <input
                  type="number"
                  id="story_points"
                  name="story_points"
                  value={issue.story_points ?? ""}
                  onChange={handleChange}
                  placeholder="Story Points"
                  className="form-input"
                />
              </div>

              <div className="form-group form-full-width">
                <label htmlFor="description">Description</label>
                <textarea
                  id="description"
                  name="description"
                  value={issue.description || ""}
                  onChange={handleChange}
                  placeholder="Description"
                  className="form-input"
                  rows={4}
                />
              </div>

              <div className="form-group form-full-width">
                <label htmlFor="repository_link">Repository Link</label>
                <input
                  type="text"
                  id="repository_link"
                  name="repository_link"
                  value={issue.repository_link || ""}
                  onChange={handleChange}
                  placeholder="Repository Link"
                  className="form-input"
                />
              </div>
            </div>
            </div>
          

          {/* Zuordnungen */}
          <div className="form-section">
            <h3 className="section-title">Zuordnungen</h3>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="category_id">Category</label>
                <select
                  id="category_id"
                  name="category_id"
                  value={issue.category_id || ""}
                  onChange={handleChange}
                  className="form-input"
                >
                  <option value="">-- None --</option> 
                  {options.categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="sprint_id">Sprint</label>
                <select
                  id="sprint_id"
                  name="sprint_id"
                  value={issue.sprint_id || ""}
                  onChange={handleChange}
                  className="form-input"
                >
                  <option value="">-- None --</option> 
                  {options.sprints.map((sprint) => (
                    <option key={sprint.id} value={sprint.id}>
                      {sprint.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="state_id">State</label>
                <select
                  id="state_id"
                  name="state_id"
                  value={issue.state_id || ""}
                  onChange={handleChange}
                  className="form-input"
                >
                  <option value="">-- None --</option> 
                  {options.states.map((state) => (
                    <option key={state.id} value={state.id}>
                      {state.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="priority_id">Priority</label>
                <select
                  id="priority_id"
                  name="priority_id"
                  value={issue.priority_id || ""}
                  onChange={handleChange}
                  className="form-input"
                >
                  <option value="">-- None --</option> 
                  {options.priorities.map((priority) => (
                    <option key={priority.id} value={priority.id}>
                      {priority.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group form-full-width">
                <label htmlFor="responsible_user_id">Responsible User</label>
                <select
                  id="responsible_user_id"
                  name="responsible_user_id"
                  value={issue.responsible_user_id || ""}
                  onChange={handleChange}
                  className="form-input"
                >
                  <option value="">-- None --</option>
                  {options.users.map((user) => (
                    <option key={user.id} value={user.id}>
                      {user.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
          </div>
          {/* Aktionen */}
          <div className="form-actions">
            <button type="button" className="btn btn-close" onClick={onClose}>
              Close
            </button>
            <button type="button" className="btn btn-save" onClick={handleSave}>
              Save Changes
            </button>
          </div>
        </form>

      </div>
    </div>
  );
};

export default EditIssueForm;
