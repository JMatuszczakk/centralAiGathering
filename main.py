from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from generatePrompt import generatePrompt as get_prompt

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/prompt', methods=['GET'])
def serve_prompt():
    prompt = get_prompt()  # Get prompt from the imported function
    return jsonify({"prompt": prompt})

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "Image uploaded successfully", "filename": filename}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)