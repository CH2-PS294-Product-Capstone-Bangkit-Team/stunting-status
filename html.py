from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Ganti path_file_csv dengan path ke file CSV yang berisi data Anda
path_file_csv = 'StuntedAssessmentParameters.csv'
data = pd.read_csv(path_file_csv)

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

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        day = int(request.form['day'])
        height = float(request.form['height'])
        gender = request.form['gender']

        if 0 <= day < len(data):
            stunting_status = determine_stunting_status(day, height, gender)
            return render_template('result.html', day=day, status=stunting_status)
        else:
            error = 'Invalid Day'

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
