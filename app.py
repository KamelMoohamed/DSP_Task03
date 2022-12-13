import os
import sys
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, request
from processing.processing import Processing
from processing.feature_extraction_processing import getSpectrogram

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
            freq1, time1, freqAmp1 = getSpectrogram(file_path)
            freq2, time2, freqAmp2 = getSpectrogram(processing.getSpectrogramFilePath())

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
                        'f': list(freq1),
                        't': list(time1),
                        'Sxx': freqAmp1.tolist()
                    },
                    "spectrogram2": {
                        'f': list(freq2),
                        't': list(freq2),
                        'Sxx': freqAmp2.tolist()
                    },
                    "prediction" : prediction
                }
            ), 200

    # Case of File Not Uploaded
    return 400


if __name__ == '__main__':
    app.run(debug=True) 