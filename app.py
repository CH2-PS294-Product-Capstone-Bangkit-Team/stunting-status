from flask import Flask, render_template, request
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')


# Ganti dengan nama file CSV dan path yang sesuai
growth_path = 'data/ChildGrowthAssessmentParameters.csv'
wasted_path = 'data/WastedAssessmentParameters.csv'

# Baca data dari CSV
data = pd.read_csv(growth_path)
wasted_data = pd.read_csv(wasted_path)

# status stunting
def determine_status_stunting(day, gender, height):
    selected_data = data[(data['Day'] == day) & (data['Gender'] == gender)]

    if not selected_data.empty:
        sev_stunted = selected_data['Severly Stunted'].iloc[0]
        min_mod_stunted = selected_data['Moderately Stunted min'].iloc[0]
        max_mod_stunted = selected_data['Moderately Stunted max'].iloc[0]
        normal_height = selected_data['Normal Height'].iloc[0]

        # Tentukan logika untuk menentukan status stunting 
        if height < sev_stunted:
            return jsonify(
                    message="Severely Stunted",
                    category="success",
                    status=200
                )
        elif min_mod_stunted < height <= max_mod_stunted:
            return jsonify(
                    message="Moderately Stunted",
                    category="success",
                    status=200
                )
        elif height > normal_height:
            return jsonify(
                    message="Normal Height",
                    category="success",
                    status=200
                )
        else:
            return jsonify(
                    message="Has no categories",
                    category="success",
                    status=204
                )
    else:
        return jsonify(
                    message="Data not found",
                    category="error",
                    status=404
                )

# status underweight
   
def determine_status_underweight(day, gender, weight):
    selected_data = data[(data['Day'] == day) & (data['Gender'] == gender)]

    if not selected_data.empty:
        sev_under = selected_data['Severly Underweight'].iloc[0]
        min_mod_under = selected_data['Moderately Underweight min'].iloc[0]
        max_mod_under = selected_data['Moderately Underweight max'].iloc[0]
        normal_weight = selected_data['Normal Weight'].iloc[0]

        # Tentukan logika untuk menentukan status underweight 
        if weight < sev_under:
            return jsonify(
                    message="Severely Underweight",
                    category="success",
                    status=200
                )
        elif min_mod_under < weight <= max_mod_under:
            return jsonify(
                    message="Moderately Underweight",
                    category="success",
                    status=200
                )
        elif weight > normal_weight:
            return jsonify(
                    message="Normal Weight",
                    category="success",
                    status=200
                )
        else:
            return jsonify(
                    message="Has no categories",
                    category="success",
                    status=204
                )
    else:
        return jsonify(
                    message="Data not found",
                    category="error",
                    status=404
                )
    
def determine_status_wasted(gender, height, weight):
    selected_data = wasted_data[(wasted_data['Gender'] == gender) & (wasted_data['Height'] == height)]

    if not selected_data.empty:
        sam_min = selected_data['SAM min'].iloc[0]
        mam_min = selected_data['MAM min'].iloc[0]
        mam_max = selected_data['MAM max'].iloc[0]
        normal_min = selected_data['Normal min'].iloc[0]
        normal_max = selected_data['Normal max'].iloc[0]
        over_min = selected_data['Overweight min'].iloc[0]
        over_max = selected_data['Overweight max'].iloc[0]
        obsese = selected_data['Obsese'].iloc[0]

        # Tentukan status wasted berdasarkan berat badan
        if weight <= sam_min:
            return jsonify(
                    message="SAM (Severe Acute Malnutrition)",
                    category="success",
                    status=200
                )
        elif mam_min < weight <= mam_max:
            return jsonify(
                    message="MAM (Moderate Acute Malnutrition)",
                    category="success",
                    status=200
                )
        elif normal_min < weight <= normal_max:
            return jsonify(
                    message="Normal Nutrition",
                    category="success",
                    status=200
                )
        elif over_min < weight <= over_max:
            return jsonify(
                    message="Overweight",
                    category="success",
                    status=200
                )
        elif weight > obsese:
            return jsonify(
                    message="Obese",
                    category="success",
                    status=200
                )
        else:
            return jsonify(
                    message="Has no categories",
                    category="success",
                    status=204
                )
    else:
        return jsonify(
                    message="Data not found",
                    category="error",
                    status=404
                )

from flask import request, jsonify

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assessment', methods=['POST'])
def assessment():
    try:
        day = int(request.form['day'])
        gender = request.form['gender']
        height = float(request.form['height'])
        weight = float(request.form['weight'])

        # Menentukan Status Stunting berdasarkan data yang dimasukkan
        stunting_status = determine_status_stunting(day, gender, height)

        # Menentukan Status Underweight berdasarkan data yang dimasukkan
        underweight_status = determine_status_underweight(day, gender, weight)
        
        # Menentukan Status Wasted berdasarkan data yang dimasukkan
        wasted_status = determine_status_wasted(gender, height, weight)

        response_data = {
            'stunting': {
                'message': stunting_status.json['message'],
                'category': stunting_status.json['category'],
                'status': stunting_status.json['status']
            },
            'underweight': {
                'message': underweight_status.json['message'],
                'category': underweight_status.json['category'],
                'status': underweight_status.json['status']
            },
            'wasted': {
                'message': wasted_status.json['message'],
                'category': wasted_status.json['category'],
                'status': wasted_status.json['status']
            }
        }

        return jsonify(response_data)
    except Exception as e:
        error_data = {
            'error': str(e)
        }
        return jsonify(error_data), 500

if __name__ == '__main__':
    app.run()
