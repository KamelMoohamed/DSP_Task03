import sys
from flask import Flask, jsonify, render_template, request
from processing.processing import Processing

sys.path.append('./processing')
app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')


@app.route('/predict', methods=['GET'])
def predict():
    if request.files['upload']:
        isOpen, person = Processing(request.files['upload'])
        return jsonify({
            "isOpen":isOpen,
            "person":person
        }), 200
    return 400



if __name__ == '__main__':
    app.run(debug=True) 