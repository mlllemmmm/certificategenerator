from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import json
from datetime import datetime
import uuid
from certificate_templates import create_advanced_certificate, create_minimal_certificate

app = Flask(__name__)
CORS(app)

# Create directories if they don't exist
os.makedirs('certificates', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Certificate templates
CERTIFICATE_TEMPLATES = {
    'volunteer': {
        'title': 'Certificate of Appreciation',
        'subtitle': 'Volunteer Service',
        'background_color': colors.lightblue,
        'border_color': colors.darkblue,
        'text_color': colors.black
    },
    'achievement': {
        'title': 'Certificate of Achievement',
        'subtitle': 'Outstanding Performance',
        'background_color': colors.lightyellow,
        'border_color': colors.darkgoldenrod,
        'text_color': colors.black
    },
    'participation': {
        'title': 'Certificate of Participation',
        'subtitle': 'Event Participation',
        'background_color': colors.lightgreen,
        'border_color': colors.darkgreen,
        'text_color': colors.black
    }
}

def generate_certificate_pdf(user_data, template_type='volunteer', style='advanced'):
    """Generate a PDF certificate based on user data and template"""
    
    if style == 'advanced':
        return create_advanced_certificate(user_data, template_type)
    elif style == 'minimal':
        return create_minimal_certificate(user_data, template_type)
    else:
        # Fallback to original simple certificate
        return generate_simple_certificate(user_data, template_type)

def generate_simple_certificate(user_data, template_type='volunteer'):
    """Generate a simple PDF certificate (original implementation)"""
    
    # Generate unique filename
    filename = f"certificates/certificate_{uuid.uuid4().hex[:8]}.pdf"
    
    # Get template
    template = CERTIFICATE_TEMPLATES.get(template_type, CERTIFICATE_TEMPLATES['volunteer'])
    
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=template['text_color'],
        alignment=1,  # Center alignment
        spaceAfter=30
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=template['text_color'],
        alignment=1,
        spaceAfter=20
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=14,
        textColor=template['text_color'],
        alignment=1,
        spaceAfter=15
    )
    
    # Add content
    story.append(Paragraph(template['title'], title_style))
    story.append(Paragraph(template['subtitle'], subtitle_style))
    story.append(Spacer(1, 40))
    
    # Certificate text
    certificate_text = f"""
    This is to certify that <b>{user_data['name']}</b> has successfully completed 
    {user_data['duration']} hours of volunteer service.
    """
    
    if user_data.get('organization'):
        certificate_text += f"<br/>Organization: {user_data['organization']}"
    
    if user_data.get('project'):
        certificate_text += f"<br/>Project: {user_data['project']}"
    
    certificate_text += f"""
    <br/><br/>
    Date: {datetime.now().strftime('%B %d, %Y')}
    <br/>
    Certificate ID: {uuid.uuid4().hex[:8].upper()}
    """
    
    story.append(Paragraph(certificate_text, body_style))
    
    # Build PDF
    doc.build(story)
    
    return filename

@app.route('/api/generate-certificate', methods=['POST'])
def generate_certificate():
    """API endpoint to generate certificate"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'duration']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get template type and style
        template_type = data.get('template_type', 'volunteer')
        style = data.get('style', 'advanced')  # New parameter for certificate style
        
        # Generate certificate
        filename = generate_certificate_pdf(data, template_type, style)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'Certificate generated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-certificate/<filename>')
def download_certificate(filename):
    """Download generated certificate"""
    try:
        file_path = f"certificates/{filename}"
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'Certificate not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available certificate templates"""
    return jsonify({
        'templates': list(CERTIFICATE_TEMPLATES.keys()),
        'template_details': CERTIFICATE_TEMPLATES,
        'styles': ['advanced', 'minimal', 'simple']
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Certificate Generator API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 