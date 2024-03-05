from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import os
import librosa
import numpy as np

app = Flask(__name__)
model = load_model('Models/LSTM_Model.h5')

def extract_features(file_path, segment_length):
    try:
        y, sr = librosa.load(file_path)
        features = []
        num_segments = int(np.ceil(len(y) / float(segment_length * sr)))


        for i in range(num_segments):
            start_frame = i * segment_length * sr
            end_frame = min(len(y), (i + 1) * segment_length * sr)

            y_segment = y[start_frame:end_frame]

            chroma_stft = np.mean(librosa.feature.chroma_stft(y=y_segment, sr=sr))
            rms = np.mean(librosa.feature.rms(y=y_segment))
            spec_cent = np.mean(librosa.feature.spectral_centroid(y=y_segment, sr=sr))
            spec_bw = np.mean(librosa.feature.spectral_bandwidth(y=y_segment, sr=sr))
            rolloff = np.mean(librosa.feature.spectral_rolloff(y=y_segment, sr=sr))
            zcr = np.mean(librosa.feature.zero_crossing_rate(y_segment))
            mfccs = librosa.feature.mfcc(y=y_segment, sr=sr)
            mfccs_mean = np.mean(mfccs, axis=1)

            features.append([chroma_stft, rms, spec_cent, spec_bw, rolloff, zcr, *mfccs_mean])


        return np.array(features)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        uploaded_file = request.files['audio']

        temp_path = 'temp_audio.wav'
        uploaded_file.save(temp_path)

        audio_dir_list = [temp_path]
        features = np.empty((0,26))
        for audio_dir in audio_dir_list:
            features = extract_features(audio_dir, segment_length=1)

        os.remove(temp_path)

        test_set = np.zeros((features.shape[0], 17, 10))

        for i in range(17):
            test_set[:, i, :] = features[:, i:i + 10]

        features = test_set

        if features is not None:
            prediction_result = make_prediction(features)

            return jsonify({"result": prediction_result})
        else:
            return jsonify({"error": "Error processing the audio file"})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})
    
def make_prediction(features):
    output = model.predict(features)
    return [1 if value >= 0.5 else 0 for value in output]



if __name__ == "__main__":
    app.run(debug=True)
