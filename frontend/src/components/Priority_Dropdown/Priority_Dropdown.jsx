import './Priorities.modules.css';
import React, { useState, useEffect } from 'react';
 
function Priorities() {
  const [priorities, setPriorities] = useState([]);
  const [selectedPriority, setSelectedPriority] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newPriority, setNewPriority] = useState({ name: '', level: '' });
 
  // API-Daten abrufen
  useEffect(() => {
    async function fetchPriorities() {
      try {
        const response = await fetch('http://localhost:'); // API-URL anpassen
        if (!response.ok) throw new Error('Fehler beim Abrufen der Prioritäten');
        const data = await response.json();
        setPriorities(data);
      } catch (error) {
        console.error(error);
      }
    }
 
    fetchPriorities();
  }, []);
 
  // Modal öffnen und schließen
  function handleOpenModal() {
    setIsModalOpen(true);
  }
 
  function handleCloseModal() {
    setIsModalOpen(false);
    setNewPriority({ name: '', level: '' });
  }
 
  // Eingaben aktualisieren
  function handleInputChange(event) {
setNewPriority({ ...newPriority, [event.target.name]: event.target.value });
  }
 
  // Neue Priorität speichern
  function handleSubmit() {
    setPriorities([...priorities, newPriority]);
    handleCloseModal();
  }
 
  return (
    <div className="priorities">
      <h1>Priorities</h1>
 
      {/* Dropdown */}
      <div className="dropdown-container">
        <label htmlFor="priority">Select Priority:</label>
        <select id="priority" value={selectedPriority} onChange={(e) => setSelectedPriority(e.target.value)}>
          <option value="">-- Choose a Priority --</option>
          {priorities.map((priority, index) => (
            <option key={index} value={priority.name}>
                {priority.name}
            </option>
          ))}
        </select>
      </div>
 
      {/* Modal öffnen */}
      <button className="add-priority-btn" onClick={handleOpenModal}>
        Add Priority
      </button>
 
      {/* Prioritätenliste */}
      <div className="priority-list">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Level</th>
            </tr>
          </thead>
          <tbody>
            {priorities.map((priority, index) => (
              <tr key={index}>
                <td>{priority.name}</td>
                <td>{priority.level}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
 
      {/* Modal für neue Priorität */}
      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <h2>Add a New Priority</h2>
            <input
              type="text"
              name="name"
              placeholder="Priority Name"
value={newPriority.name}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="level"
              placeholder="Priority Level"
              value={newPriority.level}
              onChange={handleInputChange}
            />
            <div className="modal-buttons">
              <button onClick={handleSubmit}>Submit</button>
              <button onClick={handleCloseModal}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
 
export default Priorities;
hat Kontextmenü

