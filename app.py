# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello from Koyeb'


# if __name__ == "__main__":
#     app.run()


from flask import Flask, request, jsonify, make_response
# from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
# CORS(app)

# Load the pre-trained model
regr_energy = joblib.load('./solar_energy_model.joblib')

@app.route('/data', methods=['POST', 'GET'])
def handle_data():
    try:
        if request.method == 'GET':
            # Get parameters from query string
            temp = float(request.args.get('temp'))
            pressure = float(request.args.get('pressure'))
            humidity = float(request.args.get('humidity'))
            wind_speed = float(request.args.get('wind_speed'))
            rain_1h = float(request.args.get('rain_1h'))
            snow_1h = float(request.args.get('snow_1h'))
            clouds_all = float(request.args.get('clouds_all'))
            isSun = float(request.args.get('isSun'))
            sunlightTime = float(request.args.get('sunlightTime'))
            dayLength = float(request.args.get('dayLength'))
            SunlightTime_daylength = float(request.args.get('SunlightTime/daylength'))
            weather_type = float(request.args.get('weather_type'))
            hour = float(request.args.get('hour'))
            month = float(request.args.get('month'))

            # Create DataFrame with the received data
            input_data = {
                "temp": temp,
                "pressure": pressure,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "rain_1h": rain_1h,
                "snow_1h": snow_1h,
                "clouds_all": clouds_all,
                "isSun": isSun,
                "sunlightTime": sunlightTime,
                "dayLength": dayLength,
                "SunlightTime/daylength": SunlightTime_daylength,
                "weather_type": weather_type,
                "hour": hour,
                "month": month
            }
            input_df = pd.DataFrame([input_data])

            # Make predictions
            predicted_energy = regr_energy.predict(input_df)
            predicted_energy = predicted_energy.tolist()

            # Create response with CORS headers
            response = make_response(jsonify({'predicted_energy': predicted_energy[0]}))
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST'

            return response

        else:
            return jsonify({'error': 'Only GET requests are supported.'}), 405

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()

