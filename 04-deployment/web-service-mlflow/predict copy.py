import pickle
from flask import Flask, jsonify, request

with open('xgb_model.bin', 'rb') as f_in:
    dv, xgb_model = pickle.load(f_in)


def prepare_features(ride: dict):
    features = {}
    features['PU_DO'] = str(ride['PULocationID']) + '_' + str(ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    
    return features

def predict(features):
    X = dv.transform(features)

    prediction = xgb_model.predict(X)

    return float(prediction[0])


app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    prediction = predict(features)

    result = {
        'duration': prediction
    }

    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)