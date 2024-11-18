
from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the preprocessed weather dataset
weather_data = pd.read_csv('cleanWeatherData.xls', index_col='DATE')
weather_data.index = pd.to_datetime(weather_data.index)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input from user
        year = int(request.form.get('year'))
        month = int(request.form.get('month'))
        
        # Filter data based on user input
        filtered_data = weather_data[(weather_data.index.year == year) & (weather_data.index.month == month)]
        
        if filtered_data.empty:
            return jsonify({'error': 'No data available for the given year and month.'})
        
        # Generate some stats as output
        avg_temp = filtered_data['BASEL_temp_min'].mean()
        avg_humidity = filtered_data['BASEL_humidity'].mean()
        
        # Return the predictions as JSON
        return jsonify({
            'average_temperature': avg_temp,
            'average_humidity': avg_humidity,
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
