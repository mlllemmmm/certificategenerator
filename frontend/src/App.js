import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    duration: '',
    organization: 'Akshar Paul NGO Pune',
    project: '',
    email: '',
    phone: ''
  });
  
  const [selectedTemplate, setSelectedTemplate] = useState('volunteer');
  const [selectedStyle, setSelectedStyle] = useState('advanced');
  const [templates, setTemplates] = useState([]);
  const [styles, setStyles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');
  const [generatedCertificate, setGeneratedCertificate] = useState(null);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await axios.get('/api/templates');
      setTemplates(response.data.templates);
      setStyles(response.data.styles || ['advanced', 'minimal', 'simple']);
    } catch (error) {
      console.error('Error fetching templates:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
  };

  const handleStyleSelect = (style) => {
    setSelectedStyle(style);
  };

  const validateForm = () => {
    if (!formData.name.trim()) {
      setMessage('Name is required');
      setMessageType('error');
      return false;
    }
    if (!formData.duration.trim()) {
      setMessage('Duration is required');
      setMessageType('error');
      return false;
    }
    if (isNaN(formData.duration) || parseInt(formData.duration) <= 0) {
      setMessage('Duration must be a positive number');
      setMessageType('error');
      return false;
    }
    return true;
  };

  const generateCertificate = async () => {
    if (!validateForm()) return;

    setLoading(true);
    setMessage('');

    try {
      const response = await axios.post('/api/generate-certificate', {
        ...formData,
        template_type: selectedTemplate,
        style: selectedStyle
      });

      if (response.data.success) {
        setGeneratedCertificate(response.data.filename);
        setMessage('Certificate generated successfully! Click download to get your certificate.');
        setMessageType('success');
      }
    } catch (error) {
      console.error('Error generating certificate:', error);
      setMessage(error.response?.data?.error || 'Error generating certificate');
      setMessageType('error');
    } finally {
      setLoading(false);
    }
  };

  const downloadCertificate = async () => {
    if (!generatedCertificate) return;

    try {
      const response = await axios.get(`/api/download-certificate/${generatedCertificate.split('/').pop()}`, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `certificate_${formData.name.replace(/\s+/g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading certificate:', error);
      setMessage('Error downloading certificate');
      setMessageType('error');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      duration: '',
      organization: '',
      project: '',
      email: '',
      phone: ''
    });
    setSelectedTemplate('volunteer');
    setSelectedStyle('advanced');
    setGeneratedCertificate(null);
    setMessage('');
    setMessageType('');
  };

  const templateInfo = {
    volunteer: {
      title: 'Volunteer Certificate',
      description: 'Perfect for recognizing volunteer service and community contributions',
      icon: '🤝'
    },
    achievement: {
      title: 'Achievement Certificate',
      description: 'Ideal for celebrating outstanding performance and accomplishments',
      icon: '🏆'
    },
    participation: {
      title: 'Participation Certificate',
      description: 'Great for acknowledging event participation and involvement',
      icon: '🎉'
    }
  };

  const styleInfo = {
    advanced: {
      title: 'Advanced Style',
      description: 'Professional design with borders and enhanced typography',
      icon: '✨'
    },
    minimal: {
      title: 'Minimal Style',
      description: 'Clean and simple design for a modern look',
      icon: '📄'
    },
    simple: {
      title: 'Simple Style',
      description: 'Basic design with essential information',
      icon: '📋'
    }
  };

  return (
    <div className="App">
      <div className="container">
        <div className="header">
          <div className="logo">
            <img src="/akshar-paaul-logo.png" alt="Akshar Paaul Logo" className="logo-image" />
            <div className="logo-text">
              <span className="akshar">AKSHAR</span> <span className="paaul">PAAUL</span>
            </div>
          </div>
          <h1>Certificate Generator</h1>
        </div>

        <div className="card">
          <h2>Volunteer Details</h2>
          <form onSubmit={(e) => e.preventDefault()}>
            <div className="grid">
              <div className="form-group">
                <label htmlFor="name">Full Name *</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Enter full name"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="duration">Duration (Hours) *</label>
                <input
                  type="number"
                  id="duration"
                  name="duration"
                  value={formData.duration}
                  onChange={handleInputChange}
                  placeholder="Enter duration in hours"
                  min="1"
                  required
                />
              </div>
            </div>

            <div className="grid">
              <div className="form-group">
                <label htmlFor="organization">Organization</label>
                <input
                  type="text"
                  id="organization"
                  name="organization"
                  value={formData.organization}
                  onChange={handleInputChange}
                  placeholder="Enter organization name"
                />
              </div>

              <div className="form-group">
                <label htmlFor="project">Project/Event</label>
                <input
                  type="text"
                  id="project"
                  name="project"
                  value={formData.project}
                  onChange={handleInputChange}
                  placeholder="Enter project or event name"
                />
              </div>
            </div>

            <div className="grid">
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="Enter email address"
                />
              </div>

              <div className="form-group">
                <label htmlFor="phone">Phone</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  placeholder="Enter phone number"
                />
              </div>
            </div>

            {message && (
              <div className={`${messageType}-message`}>
                {message}
              </div>
            )}

            <div style={{ textAlign: 'center', marginTop: '30px' }}>
              {loading ? (
                <div className="loading">
                  <div className="spinner"></div>
                  <span style={{ marginLeft: '10px' }}>Generating certificate...</span>
                </div>
              ) : (
                <div className="btn-group">
                  <button
                    className="btn"
                    onClick={generateCertificate}
                    disabled={!formData.name || !formData.duration}
                  >
                    Generate Certificate
                  </button>
                  
                  {generatedCertificate && (
                    <button
                      className="btn btn-success"
                      onClick={downloadCertificate}
                    >
                      Download Certificate
                    </button>
                  )}
                  
                  <button
                    className="btn btn-secondary"
                    onClick={resetForm}
                  >
                    Reset Form
                  </button>
                </div>
              )}
            </div>
          </form>
        </div>

        <div className="card">
          <h2>How It Works</h2>
          <div className="grid">
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '3rem', marginBottom: '15px' }}>📝</div>
              <h3>1. Fill Details</h3>
              <p>Enter the volunteer's information including name, duration, and organization</p>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '3rem', marginBottom: '15px' }}>✨</div>
              <h3>2. Generate Certificate</h3>
              <p>Click generate to create a beautiful certificate with your details</p>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '3rem', marginBottom: '15px' }}>📄</div>
              <h3>3. Download PDF</h3>
              <p>Download your certificate as a professional PDF document</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 