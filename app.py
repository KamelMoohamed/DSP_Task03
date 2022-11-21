import os
import sys
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, request
from processing.processing import Processing

sys.path.append('./processing')
app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.files['file']:
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        file_path += '.wav'
        f.save(file_path)

        processing = Processing()
        isOpen, person = processing.predict_pipelines(file_path)
        return jsonify({
            "person": person,
            "sentence": "Others",
        }), 200
    return 400



if __name__ == '__main__':
    app.run(debug=True) 