import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from extractor import extract_text_from_pdf
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})

@app.route('/list-files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({'files': files})

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
    input_text = full_text[:5000]  # Flash handles this well

    prompt = (
        "Extract the top 5–7 core arguments made by the authors in this research paper. "
        "Each argument should be a clear, standalone point supported by reasoning or evidence. Present them as bullet points.\n\n"
        f"{input_text}"
    )

    try:
        print("📤 Sending to Gemini Flash...")
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        chat = model.start_chat()
        response = chat.send_message(prompt)
        return jsonify({"result": response.text})

    except Exception as e:
        print("🔥 Gemini Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
