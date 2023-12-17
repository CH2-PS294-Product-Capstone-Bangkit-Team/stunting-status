from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import pandas as pd
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

# Ganti dengan nama file CSV dan path yang sesuai
growth_path = 'data/ChildGrowthAssessmentParameters.csv'
wasted_path = 'data/WastedAssessmentParameters.xlsx'

# Baca data dari CSV
data = pd.read_csv(growth_path)
wasdata = pd.read_excel(wasted_path)

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
            return {
                'message': "Stunting Akut",
                'category': "success",
                'status': 200,
                'description': "Tinggi badan anak sangat rendah untuk usianya, memerlukan perhatian medis dan nutrisi tambahan.",
                'recommendation': "Segera berkonsultasi dengan dokter atau ahli gizi untuk perencanaan nutrisi yang tepat."
            }
        elif min_mod_stunted < height <= max_mod_stunted:
            return {
                'message': "Stunting",
                'category': "success",
                'status': 200,
                'description': "Tinggi badan anak di bawah rata-rata, perlu perhatian terhadap pola makan dan nutrisi sehari-hari.",
                'recommendation': "Pertimbangkan untuk meningkatkan asupan gizi dan konsultasikan dengan dokter anak."
            }
        elif height > normal_height:
            return {
                'message': "Tinggi Normal",
                'category': "success",
                'status': 200,
                'description': "Tinggi badan anak normal sesuai dengan usianya.",
                'recommendation': "Tetap pertahankan pola makan sehat dan rutin memantau pertumbuhan anak."
            }
        else:
            return {
                'message': "Tidak ada kategori",
                'category': "success",
                'status': 204,
                'description': "",
                'recommendation': ""
            }
    else:
        return {
            'message': "Data tidak ditemukan",
            'category': "error",
            'status': 404,
            'description': "",
            'recommendation': ""
        }

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
            return {
                'message': "Kurus Akut",
                'category': "success",
                'status': 200,
                'description': "Berat badan anak sangat rendah, perlu penanganan segera untuk meningkatkan asupan kalori dan nutrisi.",
                'recommendation': "Konsultasikan dengan ahli gizi atau dokter untuk perencanaan nutrisi yang sesuai."
            }
        elif min_mod_under < weight <= max_mod_under:
            return {
                'message': "Kurus",
                'category': "success",
                'status': 200,
                'description': "Berat badan anak di bawah rata-rata, diperlukan peningkatan asupan gizi untuk meningkatkan berat badan.",
                'recommendation': "Evaluasi pola makan dan konsultasikan dengan ahli gizi."
            }
        elif weight > normal_weight:
            return {
                'message': "Berat Normal",
                'category': "success",
                'status': 200,
                'description': "Berat badan anak normal sesuai dengan usianya.",
                'recommendation': "Pertahankan pola makan sehat dan rutin pantau pertumbuhan anak."
            }
        else:
            return {
                'message': "Tidak ada kategori",
                'category': "success",
                'status': 204,
                'description': "",
                'recommendation': ""
            }
    else:
        return {
            'message': "Data tidak ditemukan",
            'category': "error",
            'status': 404,
            'description': "",
            'recommendation': ""
        }

def determine_status_wasted(gender, height, weight):
    selected_wasted_data = wasdata[(wasdata['Gender'] == gender) & (wasdata['Height'] == height)]

    if not selected_wasted_data.empty:
        sam_min = selected_wasted_data['SAM min'].iloc[0]
        mam_min = selected_wasted_data['MAM min'].iloc[0]
        mam_max = selected_wasted_data['MAM max'].iloc[0]
        normal_min = selected_wasted_data['Normal min'].iloc[0]
        normal_max = selected_wasted_data['Normal max'].iloc[0]
        overweight_min = selected_wasted_data['Overweight min'].iloc[0]
        overweight_max = selected_wasted_data['Overweight max'].iloc[0]
        obese_max = selected_wasted_data['Obese'].iloc[0]

        # Tentukan status wasted berdasarkan berat badan
        if weight <= sam_min:
            return {
                'message': "SAM",
                'category': "success",
                'status': 200,
                'description': "Kondisi gizi akut berat, memerlukan perawatan medis dan nutrisi khusus.",
                'recommendation': "Segera hubungi layanan kesehatan anak untuk penanganan lebih lanjut."
            }
        elif mam_min < weight <= mam_max:
            return {
                'message': "MAM",
                'category': "success",
                'status': 200,
                'description': "Kondisi gizi akut sedang, memerlukan peningkatan asupan kalori dan nutrisi.",
                'recommendation': "Konsultasikan dengan dokter atau ahli gizi untuk perencanaan nutrisi."
            }
        elif normal_min < weight <= normal_max:
            return {
                'message': "Gizi Normal",
                'category': "success",
                'status': 200,
                'description': "Status gizi normal, anak dalam kondisi sehat.",
                'recommendation': "Lanjutkan dengan pola makan sehat dan rutin pemeriksaan kesehatan."
            }
        elif overweight_min < weight <= overweight_max:
            return {
                'message': "Kelebihan Berat",
                'category': "success",
                'status': 200,
                'description': "Kelebihan berat badan, memerlukan perubahan pola makan dan gaya hidup.",
                'recommendation': "Konsultasikan dengan ahli gizi untuk rencana diet seimbang."
            }
        elif weight > obese_max:
            return {
                'message': "Obesitas",
                'category': "success",
                'status': 200,
                'description': "Obesitas, kondisi gizi yang dapat menyebabkan masalah kesehatan serius.",
                'recommendation': "Segera konsultasikan dengan dokter atau ahli gizi untuk pengelolaan berat badan yang aman."
            }
        else:
            return {
                'message': "Tidak ada kategori",
                'category': "success",
                'status': 204,
                'description': "",
                'recommendation': ""
            }
    else:
        return {
            'message': "Data tidak ditemukan",
            'category': "error",
            'status': 404,
            'description': "",
            'recommendation': ""
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assessment', methods=['POST'])
def assessment():
    try:
        # Use request.form to get form data from the request body
        day = int(request.form['day'])
        gender = request.form['gender']
        
        # Parse height as a float
        height_str = request.form['height']
        height = float(height_str)
        weight = float(request.form['weight'])


        # Menentukan Status Stunting berdasarkan data yang dimasukkan
        stunting_status = determine_status_stunting(day, gender, height)

        # Menentukan Status Underweight berdasarkan data yang dimasukkan
        underweight_status = determine_status_underweight(day, gender, weight)
        
        # Menentukan Status Wasted berdasarkan data yang dimasukkan
        wasted_status = determine_status_wasted(gender, height, weight)

        response_data = {
            'stunting': {
                'message': stunting_status['message'],
                'category': stunting_status['category'],
                'status': stunting_status['status'],
                'description': stunting_status['description'],
                'recommendation': stunting_status['recommendation']
            },
            'underweight': {
                'message': underweight_status['message'],
                'category': underweight_status['category'],
                'status': underweight_status['status'],
                'description': underweight_status['description'],
                'recommendation': underweight_status['recommendation']
            },
            'wasted': {
                'message': wasted_status['message'],
                'category': wasted_status['category'],
                'status': wasted_status['status'],
                'description': wasted_status['description'],
                'recommendation': wasted_status['recommendation']
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
