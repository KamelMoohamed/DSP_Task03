import os
import sys
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, request
from processing.processing import Processing
from processing.feature_extraction_processing import getGraph3Data, getGraph4Data
from processing.peaks_features import fingerprint

sys.path.append('./processing')
app = Flask(__name__, template_folder="templates")

isHome = False

@app.route('/', methods=['GET'])
def index():
    isHome = True
    return render_template('main.html')


@app.route('/poster')
def poster():
    isHome = False
    return render_template('poster.html')    


@app.route('/predict', methods=['POST'])
def predict():
    if request.files['file']:
        # File Saving
        file = request.files['file']
        abspath = os.path.dirname(__file__)
        file_path = os.path.join(
            abspath, 'uploads', secure_filename(file.filename))
        file_path += '.wav'
        file.save(file_path)

        # Predication
        processing = Processing()
        sentence, person = processing.prediction_pipelines(file_path)

        if(sentence == 'Others'):
            prediction = 'Others'
        else:
            prediction = person

        if isHome:
            # Output for Home Page (just prediction)
            return jsonify({
                "prediction": prediction
            }), 200
        else:
            # Output for the e-poster page (prediction with diagrams)
            xAxis1, yAxis1 = processing.getGraph1Data()
            xAxis2, yAxis2 = processing.getGraph2Data()

            x1, y1, color1 = getGraph3Data(file_path)
            x2, y2, color2 = getGraph4Data(file_path)

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
                    "graph3":{
                        'x':list(x1),
                        'y':list(y1),
                        'color':list(color1)
                    },
                    "graph4":{
                        'x':list(x2),
                        'y':list(y2),
                        'color':list(color2)
                    },
                    "prediction" : prediction
                }
            ), 200

    # Case of File Not Uploaded
    return 400

if __name__ == '__main__':
    app.run(debug=True) 