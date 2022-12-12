import os
import sys
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, request
from processing.processing import Processing

sys.path.append('./processing')
app = Flask(__name__, template_folder="templates")

isHome = False

@app.route('/eposter')
def eposter():
    isHome = False
    return render_template('eposter.html')    

@app.route('/', methods=['GET'])
def index():
    isHome = True
    return render_template('main.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.files['file']:
        f = request.files['file']
        abspath = os.path.dirname(__file__)
        file_path = os.path.join(
            abspath, 'uploads', secure_filename(f.filename))
        file_path += '.wav'
        f.save(file_path)

        processing = Processing()
        sentence, person = processing.predict_pipelines(file_path)
        if(sentence == 'Others'):
            person = 'Others'

        if isHome:
            return jsonify({
                "person": person
            }), 200
        else:
            xAxis1, yAxis1 = processing.getGraph1Data()
            xAxis2, yAxis2 = processing.getGraph2Data()
            f1, t1, Sxx1 = processing.getSpectrogram1(file_path)
            f2, t2, Sxx2 = processing.getSpectrogram2(file_path)

            return jsonify(
                {
                    "graph1" : {
                        'x':xAxis1,
                        'y':yAxis1
                    },
                    "graph2" : {
                        'x':xAxis2,
                        'y':yAxis2
                    },
                    "spectrogram1": {
                        'f': list(f1),
                        't': list(t1),
                        'Sxx': Sxx1.tolist()
                    },
                    "spectrogram2": {
                        'f': list(f2),
                        't': list(t2),
                        'Sxx': Sxx2.tolist()
                    },
                    "person" : person
                }
            ), 200

    return 400


if __name__ == '__main__':
    app.run(debug=True) 