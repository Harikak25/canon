import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import bgImage from './assets/wpi.jpg';

function App() {
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    subject: '',
    message: '',
    urgent: false,
    attachment: null
  });

  const [status, setStatus] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked, files } = e.target;
    if (type === 'checkbox') {
      setForm({ ...form, [name]: checked });
    } else if (name === 'attachment') {
      setForm({ ...form, attachment: files[0] });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('Sending...');

    const formData = new FormData();
    Object.entries(form).forEach(([key, value]) => {
      formData.append(key, value);
    });

    try {
      await axios.post('http://localhost:8000/submit', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setStatus('✅ Message submitted successfully!');
      setForm({
        first_name: '',
        last_name: '',
        email: '',
        subject: '',
        message: '',
        urgent: false,
        attachment: null
      });
      setSubmitted(true);
    } catch (err) {
      console.error(err);
      setStatus('❌ Failed to send message.');
    }
  };

  const handleNewSubmission = () => {
    setSubmitted(false);
    setStatus('');
  };

  return (
    <div
      className="app"
      style={{
        backgroundImage: `url(${bgImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        minHeight: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        className="form-container p-5 rounded-4 shadow-lg"
        style={{
          maxWidth: '800px',
          width: '100%',
          backgroundColor: 'rgba(255, 255, 255, 0.85)',
          backdropFilter: 'blur(5px)',
        }}
      >
        <h2 className="text-center mb-4 fw-bold" style={{ color: '#003366' }}>
          CANON <br /> Contact Center
        </h2>
        
        {submitted ? (
          <div className="text-center">
            <h4>Thanks for reaching out!</h4>
            <button className="btn btn-primary mt-3" onClick={handleNewSubmission}>
              Report Another Issue
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} encType="multipart/form-data">
            <div className="row g-3">
              <div className="col-md-6">
                <input
                  className="form-control"
                  name="first_name"
                  placeholder="Enter your first name"
                  value={form.first_name}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="col-md-6">
                <input
                  className="form-control"
                  name="last_name"
                  placeholder="Enter your last name"
                  value={form.last_name}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="col-md-6">
                <input
                  className="form-control"
                  name="email"
                  type="email"
                  placeholder="Your email"
                  value={form.email}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="col-md-6">
                <input
                  className="form-control"
                  name="subject"
                  placeholder="What do you need help with?"
                  value={form.subject}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="col-12">
                <textarea
                  className="form-control"
                  name="message"
                  rows="3"
                  placeholder="Describe your issue or question in detail..."
                  value={form.message}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="col-12">
                <label className="form-label">
                  <input
                    type="checkbox"
                    name="urgent"
                    checked={form.urgent}
                    onChange={handleChange}
                    style={{ transform: 'scale(0.8)' }}
                  />{' '}
                  Mark as urgent
                </label>
              </div>
              <div className="col-12">
                <label className="form-label">
                  Attach a file (e.g. screenshot of your issue)
                </label>
                <input
                  className="form-control"
                  name="attachment"
                  type="file"
                  onChange={handleChange}
                />
              </div>
              <div className="col-12">
                <button type="submit" className="btn btn-primary w-100">
                  Send Message
                </button>
              </div>
            </div>
          </form>
        )}
        {status && <p className="mt-3 text-center fw-semibold">{status}</p>}
      </div>
    </div>
  );
}

export default App;