from flask import Flask, request, jsonify
import pandas as pd
from google.cloud import storage

app = Flask(__name__)

# Ganti bucket_name dengan nama bucket GCS Anda
bucket_name = 'stunting_status1'
file_name = 'ChildGrowthAssessmentParameters.csv'

# Fungsi untuk membaca file CSV dari GCS
def read_csv_from_gcs(bucket_name, file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()
    return pd.read_csv(pd.compat.StringIO(content))

# Baca data dari GCS
data = read_csv_from_gcs(bucket_name, file_name)

def determine_stunting_status(day, height, gender):
    # Ambil data sesuai dengan hari lahir dan jenis kelamin
    selected_data = data[(data['Day'] == day) & (data['Gender'] == gender)]

    if not selected_data.empty:
        min_height = selected_data['Severly Stunted'].iloc[0]
        max_height = selected_data['Normal'].iloc[0]

        # Tentukan logika untuk menentukan status stunting berdasarkan tinggi badan
        if height < min_height:
            return "Severely Stunted"
        elif min_height <= height <= max_height:
            return "Moderately Stunted"
        else:
            return "Normal"
    else:
        return "Data not found"

@app.route('/api/stunting', methods=['POST'])
def stunting_api():
    try:
        data_json = request.get_json()
        day = int(data_json['day'])
        height = float(data_json['height'])
        gender = data_json['gender']

        if 0 <= day < len(data):
            stunting_status = determine_stunting_status(day, height, gender)
            return jsonify({'status': stunting_status}), 200
        else:
            return jsonify({'error': 'Invalid Day'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
