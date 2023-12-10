from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

# Ganti dengan nama file CSV dan path yang sesuai
growth_path = 'ChildGrowthAssessmentParameters.csv'
wasted_path = 'WastedAssessmentParameters.csv'

# Baca data dari CSV
data = pd.read_csv(growth_path)
wasted_data = pd.read_csv(wasted_path)

def determine_status_stunting(day, gender, height):
    selected_data = data[(data['Day'] == day) & (data['Gender'] == gender)]

    if not selected_data.empty:
        sev_stunted = selected_data['Severly Stunted'].iloc[0]
        min_mod_stunted = selected_data['Moderately Stunted min'].iloc[0]
        max_mod_stunted = selected_data['Moderately Stunted max'].iloc[0]
        normal_height = selected_data['Normal Height'].iloc[0]

        # Tentukan logika untuk menentukan status stunting 
        if height < sev_stunted:
            return "Severely Stunted"
        elif min_mod_stunted < height <= max_mod_stunted:
            return "Moderately Stunted"
        elif height > normal_height:
            return "Normal Height"
        else:
            return "Has no categories"
    else:
        return "Data not found"
    
def determine_status_underweight(day, gender, weight):
    selected_data = data[(data['Day'] == day) & (data['Gender'] == gender)]

    if not selected_data.empty:
        sev_under = selected_data['Severly Underweight'].iloc[0]
        min_mod_under = selected_data['Moderately Underweight min'].iloc[0]
        max_mod_under = selected_data['Moderately Underweight max'].iloc[0]
        normal_weight = selected_data['Normal Weight'].iloc[0]

        # Tentukan logika untuk menentukan status underweight 
        if weight < sev_under:
            return "Severely Underweight"
        elif min_mod_under < weight <= max_mod_under:
            return "Moderately Underweight"
        elif weight > normal_weight:
            return "Normal Weight"
        else:
            return "Has no categories"
    else:
        return "Data not found"
    
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
            return "SAM (Severe Acute Malnutrition)"
        elif mam_min < weight <= mam_max:
            return "MAM (Moderate Acute Malnutrition)"
        elif normal_min < weight <= normal_max:
            return "Normal Nutrition"
        elif over_min < weight <= over_max:
            return "Overweight"
        elif weight > obsese:
            return "Obese"
        else:
            return "Has no categories"
    else:
        return "Data not found"

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

        return render_template('result.html', stunting=stunting_status, underweight=underweight_status, wasted=wasted_status)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
