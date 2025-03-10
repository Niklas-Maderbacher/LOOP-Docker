// Registration.jsx
import React, { useState } from 'react';
import './Registration.css';

function Registration() {
  const [formData, setFormData] = useState({ name: '', email: '', password: '' });
  const [errors, setErrors] = useState({});

  const validate = () => {
    let tempErrors = {};
    if (!formData.name) tempErrors.name = "Name is required";
    if (!formData.email.match(/^[^@\s]+@[^@\s]+\.[^@\s]+$/)) tempErrors.email = "Invalid email format";
    if (formData.password.length < 6) tempErrors.password = "Password must be at least 6 characters";
    setErrors(tempErrors);
    return Object.keys(tempErrors).length === 0;
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      console.log("Form submitted", formData);
    }
  };

  return (
    <div className="registration-container">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} />
        {errors.name && <span className="error">{errors.name}</span>}
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} />
        {errors.email && <span className="error">{errors.email}</span>}
        <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} />
        {errors.password && <span className="error">{errors.password}</span>}
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Registration;