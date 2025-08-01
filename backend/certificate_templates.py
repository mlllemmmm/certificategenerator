from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import uuid

def create_advanced_certificate(user_data, template_type='volunteer'):
    """Create an advanced certificate with modern styling matching the provided design"""
    
    # Template configurations - Updated to match the provided design
    templates = {
        'volunteer': {
            'title': 'CERTIFICATE OF APPRECIATION',
            'subtitle': 'Volunteer Service Recognition',
            'border_color': colors.darkblue,
            'accent_color': colors.lightblue,
            'text_color': colors.black,
            'background_color': colors.white
        },
        'achievement': {
            'title': 'CERTIFICATE OF ACHIEVEMENT',
            'subtitle': 'Outstanding Performance Award',
            'border_color': colors.darkblue,
            'accent_color': colors.lightblue,
            'text_color': colors.black,
            'background_color': colors.white
        },
        'participation': {
            'title': 'CERTIFICATE OF PARTICIPATION',
            'subtitle': 'Event Participation Recognition',
            'border_color': colors.darkblue,
            'accent_color': colors.lightblue,
            'text_color': colors.black,
            'background_color': colors.white
        }
    }
    
    template = templates.get(template_type, templates['volunteer'])
    
    # Generate filename
    filename = f"certificates/advanced_certificate_{uuid.uuid4().hex[:8]}.pdf"
    
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles matching the provided design
    title_style = ParagraphStyle(
        'CertificateTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.darkblue,
        alignment=TA_CENTER,
        spaceAfter=30,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CertificateBody',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica',
        leading=20
    )
    
    metadata_style = ParagraphStyle(
        'Metadata',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=TA_LEFT,
        spaceAfter=5,
        fontName='Helvetica'
    )
    
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=10,
        fontName='Helvetica'
    )
    
    # Create border table with blue border design
    border_data = [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ]
    
    border_table = Table(border_data, colWidths=[0.3*inch, 7.4*inch, 0.3*inch], rowHeights=[0.3*inch, 10.4*inch, 0.3*inch])
    border_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 3, colors.darkblue),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
    ]))
    
    # Add content matching the provided design
    story.append(Spacer(1, 50))
    story.append(Paragraph(template['title'], title_style))
    story.append(Spacer(1, 40))
    
    # Certificate text matching the design
    certificate_text = f"""
    This is to certify that <b>{user_data['name']}</b> has successfully completed 
    <b>{user_data['duration']} hours</b> of dedicated volunteer service.
    """
    
    # Use Akshar Paul NGO Pune as the organization
    organization = user_data.get('organization', 'Akshar Paul NGO Pune')
    certificate_text += f"<br/><br/>Organization: <b>{organization}</b>"
    
    if user_data.get('project'):
        certificate_text += f"<br/>Project: <b>{user_data['project']}</b>"
    
    story.append(Paragraph(certificate_text, body_style))
    story.append(Spacer(1, 60))
    
    # Date and certificate ID in top-right corner style
    date_text = f"Date: {datetime.now().strftime('%B %d, %Y')}"
    cert_id = f"Certificate ID: {uuid.uuid4().hex[:8].upper()}"
    
    story.append(Paragraph(date_text, signature_style))
    story.append(Paragraph(cert_id, signature_style))
    story.append(Spacer(1, 40))
    
    # Signature line
    signature_text = "_________________________<br/>Authorized Signature"
    story.append(Paragraph(signature_text, signature_style))
    
    # Build PDF
    doc.build(story)
    
    return filename

def create_minimal_certificate(user_data, template_type='volunteer'):
    """Create a minimal, clean certificate design"""
    
    filename = f"certificates/minimal_certificate_{uuid.uuid4().hex[:8]}.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Minimal styles
    title_style = ParagraphStyle(
        'MinimalTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=30,
        fontName='Helvetica'
    )
    
    body_style = ParagraphStyle(
        'MinimalBody',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=15,
        fontName='Helvetica',
        leading=20
    )
    
    # Content
    story.append(Spacer(1, 100))
    story.append(Paragraph('Certificate of Completion', title_style))
    story.append(Spacer(1, 50))
    
    certificate_text = f"""
    This certifies that <b>{user_data['name']}</b> has completed 
    {user_data['duration']} hours of volunteer service.
    """
    
    if user_data.get('organization'):
        certificate_text += f"<br/><br/>Organization: {user_data['organization']}"
    
    certificate_text += f"<br/><br/>Date: {datetime.now().strftime('%B %d, %Y')}"
    
    story.append(Paragraph(certificate_text, body_style))
    
    doc.build(story)
    
    return filename 