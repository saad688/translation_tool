import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from backend import TranslationBackend
import tempfile

app = Flask(__name__)

# CORS Configuration - Allow requests from Cloudflare frontend
# In production, replace '*' with your actual Cloudflare Pages domain
CORS(app, resources={
    r"/api/*": {
        "origins": os.environ.get("ALLOWED_ORIGINS", "*").split(","),
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render deployment monitoring."""
    return jsonify({'status': 'healthy', 'service': 'urdu-translation-api'})


@app.route('/api/process', methods=['POST'])
def process_file():
    """Process a DOCX file and translate English words to Urdu."""
    # Get API key from environment
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return jsonify({'error': 'Server configuration error: API key not set'}), 500
    
    # Get translation type from request
    translation_type = request.form.get('translation_type', 'basic')
    
    # Check if file is provided
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only .docx files are allowed'}), 400
    
    try:
        # Save input file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Create output path
        base, ext = os.path.splitext(filename)
        output_filename = f"{base}_translated{ext}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Process the file
        backend = TranslationBackend(api_key, translation_type)
        if not backend.client:
            return jsonify({'error': 'Failed to initialize Gemini client. Check server configuration.'}), 500
        
        success, message = backend.process_docx(input_path, output_path)
        
        # Clean up input file
        os.remove(input_path)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'filename': output_filename
            })
        else:
            return jsonify({'error': message}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download a translated file."""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        response = send_file(file_path, as_attachment=True)
        
        # Schedule file deletion after sending
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass
        
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 404


# Keep legacy routes for backward compatibility (optional)
@app.route('/')
def index():
    """Redirect or serve info for API."""
    return jsonify({
        'service': 'Urdu Translation API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'process': '/api/process (POST)',
            'download': '/api/download/<filename>'
        }
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
