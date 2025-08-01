# Certificate Generator - Setup Guide

This guide will help you set up and run the Certificate Generator application on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed:

### For Backend (Python)
- Python 3.7 or higher
- pip (Python package installer)

### For Frontend (React)
- Node.js 14 or higher
- npm (Node package manager)

## Quick Start

### Option 1: Using Batch Files (Windows)

1. **Start the Backend Server**
   - Double-click `start_backend.bat`
   - This will install dependencies and start the Flask server on port 5000

2. **Start the Frontend Server**
   - Double-click `start_frontend.bat`
   - This will install dependencies and start the React development server on port 3000

3. **Access the Application**
   - Open your browser and go to `http://localhost:3000`

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask server**
   ```bash
   python app.py
   ```

   The backend will be available at `http://localhost:5000`

#### Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the React development server**
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

## Features

### Certificate Templates
- **Volunteer Certificate**: For recognizing volunteer service
- **Achievement Certificate**: For celebrating outstanding performance
- **Participation Certificate**: For acknowledging event participation

### Certificate Styles
- **Advanced Style**: Professional design with borders and enhanced typography
- **Minimal Style**: Clean and simple design for a modern look
- **Simple Style**: Basic design with essential information

### Form Fields
- Full Name (required)
- Duration in hours (required)
- Organization (optional)
- Project/Event (optional)
- Email (optional)
- Phone (optional)

## API Endpoints

### Backend API (Port 5000)

- `GET /api/health` - Health check
- `GET /api/templates` - Get available templates and styles
- `POST /api/generate-certificate` - Generate a new certificate
- `GET /api/download-certificate/<filename>` - Download generated certificate

### Frontend (Port 3000)

- Main application interface
- Form for collecting user details
- Template and style selection
- Certificate generation and download

## File Structure

```
certificate-generator/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── certificate_templates.py  # Advanced certificate templates
│   ├── requirements.txt          # Python dependencies
│   └── certificates/             # Generated certificates (auto-created)
├── frontend/
│   ├── public/
│   │   ├── index.html           # Main HTML file
│   │   └── manifest.json        # Web app manifest
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── App.css             # Component styles
│   │   ├── index.js            # React entry point
│   │   └── index.css           # Global styles
│   └── package.json            # Node.js dependencies
├── start_backend.bat           # Windows batch file for backend
├── start_frontend.bat          # Windows batch file for frontend
├── README.md                   # Project overview
└── SETUP.md                   # This setup guide
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Backend: Change port in `backend/app.py` line 150
   - Frontend: React will automatically suggest an alternative port

2. **Python dependencies not found**
   - Make sure you're using Python 3.7+
   - Try: `pip3 install -r requirements.txt`

3. **Node.js dependencies not found**
   - Make sure you're using Node.js 14+
   - Try: `npm install --force`

4. **CORS errors**
   - The backend includes CORS configuration
   - Make sure both servers are running

5. **Certificate generation fails**
   - Check that the `certificates` directory exists
   - Ensure you have write permissions

### Development

To modify the application:

1. **Backend changes**: Edit files in the `backend/` directory
2. **Frontend changes**: Edit files in the `frontend/src/` directory
3. **Add new templates**: Modify `backend/certificate_templates.py`
4. **Add new styles**: Update the `styles` array in the backend API

## Production Deployment

For production deployment:

1. **Backend**: Use a production WSGI server like Gunicorn
2. **Frontend**: Build the React app with `npm run build`
3. **Database**: Consider adding a database for certificate storage
4. **Security**: Add authentication and input validation
5. **SSL**: Use HTTPS for secure certificate downloads

## Support

If you encounter any issues:

1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure both servers are running
4. Check file permissions for the certificates directory 