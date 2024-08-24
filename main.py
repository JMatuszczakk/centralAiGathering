from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from generatePrompt import generatePrompt as get_prompt
from colors import check_color_similarity
from PIL import Image
import random
import shutil
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def move_verified_image(filename):
    source_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    destination_path = os.path.join('verified', filename)
    
    try:
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        # Use shutil.move instead of os.rename for cross-device moves
        shutil.move(source_path, destination_path)
        print(f"Successfully moved {filename} to verified folder.")
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found in the upload folder.")
    except PermissionError:
        print(f"Error: Permission denied when trying to move {filename}.")
    except Exception as e:
        print(f"An unexpected error occurred while moving {filename}: {str(e)}")

@app.route('/prompt', methods=['GET'])
def serve_prompt():
    prompt = get_prompt()  # Get prompt from the imported function
    return jsonify({"prompt": prompt})


def verifyImage(filename):
    #open the image
    img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print(check_color_similarity(img))
    return check_color_similarity(img)


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filename = filename.split('.')[0]+str(random.randint(0, 1000000))+'.'+filename.split('.')[1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        if verifyImage(filename):
            #copy the image to the verified folder
            os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join('verified', filename))
            #remove the image from the uploads folder
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return jsonify({"message": "Image uploaded successfully", "filename": filename}), 200
    if verifyImage(filename):
        #copy the image to the verified folder
        os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join('verified', filename))
        #remove the image from the uploads folder
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)