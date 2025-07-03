import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from extractor import extract_text_from_pdf
from transformers import pipeline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Hugging Face pipeline with smaller model
argument_model = pipeline(
    "text2text-generation",
    model="google/flan-t5-small"
)

# Upload a PDF file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})

# List uploaded files
@app.route('/list-files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({'files': files})

# Extract basic raw lines
@app.route('/extract-arguments', methods=['POST'])
def extract_arguments():
    data = request.get_json()
    filename = data.get('filename')

    if not filename:
        return jsonify({'error': 'Filename not provided'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    full_text = extract_text_from_pdf(filepath)
    arguments = [line.strip() for line in full_text.strip().split('\n') if line.strip()][:5]
    return jsonify({'arguments': arguments})

# Generate arguments using flan-t5-small
@app.route('/generate', methods=['POST'])
def generate_arguments():
    data = request.get_json()
    filename = data.get('filename')

    if not filename:
        return jsonify({'error': 'Filename is required'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    full_text = extract_text_from_pdf(filepath)
    input_text = full_text[:1000]  # smaller model = smaller input

    prompt = (
        "Extract the top 5 arguments from the following research paper. "
        "List them clearly as bullet points:\n\n"
        f"{input_text}"
    )

    try:
        print("🔁 Generating with flan-t5-small...")
        output = argument_model(prompt, max_new_tokens=150)[0]["generated_text"]
        return jsonify({"result": output})

    except Exception as e:
        print("🔥 Hugging Face ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
