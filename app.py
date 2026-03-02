"""
JanSahayak Flask Web Application
Beautiful UI for Multi-Agent Government Intelligence System
"""

from flask import Flask, render_template, request, jsonify, session, send_file
import json
import os
from datetime import datetime
from graph.workflow import run_workflow
import uuid
import io
import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Store active sessions
sessions = {}


def format_markdown(text):
    """Convert markdown-style text to HTML"""
    if not text or not isinstance(text, str):
        return text
    
    import re
    
    # Convert headers (### heading)
    text = re.sub(r'###\s+(.+?)(?=\n|$)', r'<h4>\1</h4>', text)
    text = re.sub(r'##\s+(.+?)(?=\n|$)', r'<h3>\1</h3>', text)
    
    # Convert bold (**text**)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert italic (*text*)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    
    # Convert bullet points (- item or * item)
    text = re.sub(r'^[\-\*]\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', text, flags=re.DOTALL)
    text = text.replace('</ul>\n<ul>', '\n')  # Merge consecutive lists
    
    # Convert line breaks
    text = text.replace('\n\n', '</p><p>')
    text = text.replace('\n', '<br>')
    
    # Wrap in paragraph if not starting with a tag
    if not text.startswith('<'):
        text = f'<p>{text}</p>'
    
    return text


# Register Jinja filter
app.jinja_env.filters['format_markdown'] = format_markdown


@app.route('/')
def index():
    """Landing page with input form"""
    return render_template('index.html')


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Process user input and run workflow"""
    try:
        # Get user input
        user_input = request.json.get('user_input', '')
        structured_data = request.json.get('structured_data', None)
        
        if not user_input.strip():
            return jsonify({
                'success': False,
                'error': 'Please provide your details'
            }), 400
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Store in session (including structured data if available)
        sessions[session_id] = {
            'status': 'processing',
            'input': user_input,
            'structured_data': structured_data,
            'started_at': datetime.now().isoformat()
        }
        
        # Extract user interests from structured data
        user_interests = structured_data.get('interests', ['schemes', 'exams']) if structured_data else ['schemes', 'exams']
        
        # Prepare structured profile if available
        structured_profile = None
        if structured_data:
            structured_profile = {
                'name': structured_data.get('name', 'Not Provided'),
                'age': structured_data.get('age', 'Not Provided'),
                'gender': structured_data.get('gender', 'Not Provided'),
                'state': structured_data.get('state', 'Not Provided'),
                'education': structured_data.get('education', 'Not Provided'),
                'employment_status': structured_data.get('employment', 'Not Provided'),
                'income': structured_data.get('income', 'Not Provided'),
                'caste': structured_data.get('category', 'Not Provided'),
                'specialization': structured_data.get('specialization', 'Not Provided'),
                'career_interest': structured_data.get('career_interest', 'Not Provided'),
                'interests': structured_data.get('interests', [])
            }
        
        # Run workflow with interests and structured profile
        result = run_workflow(user_input, user_interests, structured_profile)
        
        # Ensure user_profile key exists in result
        if 'user_profile' not in result and 'profile' in result:
            result['user_profile'] = result['profile']
        
        # Update session
        sessions[session_id]['status'] = 'completed'
        sessions[session_id]['result'] = result
        sessions[session_id]['completed_at'] = datetime.now().isoformat()
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/results_{timestamp}.json"
        os.makedirs('outputs', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'result': result,
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/result/<session_id>')
def result(session_id):
    """Display results page"""
    if session_id not in sessions:
        return render_template('error.html', 
                             error='Session not found'), 404
    
    session_data = sessions[session_id]
    
    if session_data['status'] != 'completed':
        return render_template('error.html', 
                             error='Analysis still in progress'), 400
    
    return render_template('results.html', 
                         session_id=session_id,
                         session_data=session_data,
                         result=session_data['result'])


@app.route('/api/status/<session_id>')
def status(session_id):
    """Check analysis status"""
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify(sessions[session_id])


@app.route('/history')
def history():
    """View analysis history"""
    output_files = []
    
    if os.path.exists('outputs'):
        files = [f for f in os.listdir('outputs') if f.endswith('.json')]
        files.sort(reverse=True)
        
        for filename in files[:10]:  # Show last 10
            filepath = os.path.join('outputs', filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                output_files.append({
                    'filename': filename,
                    'timestamp': filename.replace('results_', '').replace('.json', ''),
                    'profile': data.get('user_profile', {}),
                    'errors': data.get('errors', [])
                })
    
    return render_template('history.html', files=output_files)


@app.route('/api/file/<filename>')
def get_file(filename):
    """Download result file"""
    try:
        filepath = os.path.join('outputs', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/download/pdf/<session_id>')
def download_pdf(session_id):
    """Generate and download PDF report"""
    try:
        if session_id not in sessions:
            return jsonify({'error': 'Session not found'}), 404
        
        session_data = sessions[session_id]
        result = session_data.get('result', {})
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for PDF elements
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#5B21B6'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#7C3AED'),
            spaceAfter=12,
            spaceBefore=12
        )
        normal_style = styles['BodyText']
        normal_style.alignment = TA_JUSTIFY
        
        # Title
        elements.append(Paragraph("JanSahayak", title_style))
        elements.append(Paragraph("Government Benefits Analysis Report", styles['Heading3']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Timestamp
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        elements.append(Paragraph(f"<i>Generated: {timestamp}</i>", styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        # User Profile Section
        elements.append(Paragraph("Your Profile", heading_style))
        profile = result.get('user_profile', {})
        
        if profile:
            profile_data = []
            for key, value in profile.items():
                if key not in ['raw_profile', 'user_input'] and value != 'Not Provided':
                    label = key.replace('_', ' ').title()
                    profile_data.append([Paragraph(f"<b>{label}:</b>", normal_style), 
                                       Paragraph(str(value), normal_style)])
            
            if profile_data:
                profile_table = Table(profile_data, colWidths=[2.5*inch, 4*inch])
                profile_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F3F4F6')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]))
                elements.append(profile_table)
        
        elements.append(Spacer(1, 0.4*inch))
        
        # Helper function to clean text
        def clean_text(text):
            if not text or not isinstance(text, str):
                return "No information available"
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            # Remove excessive markdown
            text = re.sub(r'###\s+', '\n', text)
            text = re.sub(r'\*\*', '', text)
            return text.strip()
        
        # Government Schemes Section
        elements.append(Paragraph("Government Schemes for You", heading_style))
        schemes_text = clean_text(result.get('scheme_recommendations', 'No recommendations available'))
        for para in schemes_text.split('\n\n'):
            if para.strip():
                elements.append(Paragraph(para.strip(), normal_style))
                elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Competitive Exams Section
        elements.append(Paragraph("Competitive Exams for You", heading_style))
        exams_text = clean_text(result.get('exam_recommendations', 'No recommendations available'))
        for para in exams_text.split('\n\n'):
            if para.strip():
                elements.append(Paragraph(para.strip(), normal_style))
                elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Missed Benefits Section
        elements.append(Paragraph("Missed Benefits Analysis", heading_style))
        benefits_text = clean_text(result.get('missed_benefits_analysis', 'No analysis available'))
        for para in benefits_text.split('\n\n'):
            if para.strip():
                elements.append(Paragraph(para.strip(), normal_style))
                elements.append(Spacer(1, 0.1*inch))
        
        # Errors (if any)
        errors = result.get('errors', [])
        if errors:
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph("Notices", heading_style))
            for error in errors:
                elements.append(Paragraph(f"• {error}", normal_style))
        
        # Footer
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("<i>For more information, visit your local government office or relevant ministry website.</i>", 
                                 styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        
        # Prepare response
        buffer.seek(0)
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'JanSahayak_Report_{timestamp_str}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Get port from environment variable (for deployment platforms)
    port = int(os.environ.get('PORT', 5000))
    
    # Check if running in production
    is_production = os.environ.get('FLASK_ENV') != 'development'
    
    print("\n" + "="*70)
    print("🙏 JANSAHAYAK - Starting Web Server")
    print("="*70)
    print(f"\n📱 Access the application at: http://localhost:{port}")
    print(f"🌍 Environment: {'Production' if is_production else 'Development'}")
    print("🛑 Press CTRL+C to stop the server\n")
    
    app.run(debug=not is_production, host='0.0.0.0', port=port)
