from flask import Flask, request, render_template
import os
import easyocr

app = Flask(__name__)

# Create uploads folder if it doesn't exist
if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file part"
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file"

    file_path = os.path.join('static/uploads', file.filename)
    file.save(file_path)

    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])  # Specify the languages you want to support
    results = reader.readtext(file_path)

    # Extracting text from the results
    extracted_text = ' '.join([result[1] for result in results])

    return render_template('index.html', extracted_text=extracted_text)

if __name__ == '__main__':
    app.run(debug=True)
