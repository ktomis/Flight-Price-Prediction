# app.py
from flask import Flask, request, jsonify, render_template
from flask_wtf.csrf import CSRFProtect
import joblib
import numpy as np
import pandas as pd
import logging
from datetime import datetime

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_KEY' # Chạy createKey.py để tạo key, không cần nếu chạy local (chỉ để demo)
csrf = CSRFProtect(app)

# Khởi tạo model global
model = None

def load_model():
    """Load model khi khởi động application"""
    global model
    try:
        model = joblib.load('colab/xgboost_model.pkl')
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

# Load model trước request đầu tiên
@app.before_request
def initialize():
    if model is None:
        load_model()

feature_columns = [
    'Total_Stops', 'Journey_Day', 'Journey_Month', 'Dep_Hour', 'Dep_Minute',
    'Arrival_Hour', 'Arrival_Minute', 'Duration_Hours', 'Duration_Minutes',
    'Total_Duration_Minutes', 'Air_India', 'GoAir', 'IndiGo', 'Jet_Airways',
    'Jet_Airways_Business', 'Multiple_carriers', 
    'Multiple_carriers_Premium_economy', 'SpiceJet', 'Trujet', 'Vistara',
    'Vistara_Premium_economy', 'Chennai', 'Delhi', 'Kolkata', 'Mumbai',
    'Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi'
]

def validate_input(data):
    """Validate dữ liệu đầu vào"""
    try:
        # Kiểm tra các trường bắt buộc
        required_fields = ['dep_date', 'arr_date', 'source', 'destination', 
                         'airline', 'stopage', 'flight_class']
        if not all(field in data for field in required_fields):
            return False, "Vui lòng điền đầy đủ thông tin"

        dep_date = pd.to_datetime(data['dep_date'])
        arr_date = pd.to_datetime(data['arr_date'])
        
        if dep_date >= arr_date:
            return False, "Thời gian đến phải sau thời gian đi"

        # Kiểm tra giá trị điểm đi và đến 
        if data['source'] == data['destination']:
            return False, "Điểm đi và điểm đến không được trùng nhau"

        # Kiểm tra số điểm dừng
        if not data['stopage'].isdigit() or int(data['stopage']) < 0:
            return False, "Số điểm dừng không hợp lệ"

        return True, None
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return False, "Dữ liệu không hợp lệ"

def preprocess_input(data):
    """Xử lý dữ liệu đầu vào"""
    try:
        # Chuyển đổi dữ liệu 
        dep_date = pd.to_datetime(data['dep_date'])
        arr_date = pd.to_datetime(data['arr_date'])

        # Trích xuất các thông tin thời gian
        features = {
            'Journey_Day': dep_date.day,
            'Journey_Month': dep_date.month,
            'Dep_Hour': dep_date.hour,
            'Dep_Minute': dep_date.minute,
            'Arrival_Hour': arr_date.hour,
            'Arrival_Minute': arr_date.minute,
            'Total_Stops': int(data['stopage']),
            'Duration_Hours': int(data['duration_hours']),
            'Duration_Minutes': int(data['duration_minutes']),
            'Total_Duration_Minutes': (int(data['duration_hours']) * 60 + 
                                     int(data['duration_minutes']))
        }

        airlines = ['Air_India', 'GoAir', 'IndiGo', 'Jet_Airways', 
                   'Jet_Airways_Business', 'Multiple_carriers',
                   'Multiple_carriers_Premium_economy', 'SpiceJet', 'Trujet',
                   'Vistara', 'Vistara_Premium_economy']
        for airline in airlines:
            features[airline] = 1 if data['airline'] == airline else 0

        sources = ['Chennai', 'Delhi', 'Kolkata', 'Mumbai']
        for source in sources:
            features[source] = 1 if data['source'] == source else 0

        # Encode destination
        destinations = ['Cochin', 'Delhi', 'Hyderabad', 'New Delhi']
        for dest in destinations:
            features[dest] = 1 if data['destination'] == dest else 0

        return features
    except Exception as e:
        logger.error(f"Preprocessing error: {str(e)}")
        raise

def format_datetime(datetime_str):
    # Format dữ liệu của thời gian 
    try:
        dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        # Format theo dạng: 28/12/2024 → 15:49
        return dt.strftime('%d/%m/%Y → %H:%M')
    except Exception as e:
        logger.error(f"Error formatting datetime: {str(e)}")
        return datetime_str

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        logger.info(f"Received prediction request with data: {data}")

        is_valid, error_message = validate_input(data)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        # Format hạng ghế 
        flight_class_display = {
            'economy': 'Phổ Thông',
            'premium_economy': 'Phổ Thông Đặc Biệt',
            'business': 'Thương Gia'
        }

        # Format hãng máy bay
        airline_display = {
            'Air_India': 'Air India',
            'GoAir': 'GoAir',
            'IndiGo': 'IndiGo',
            'Jet_Airways': 'Jet Airways',
            'Multiple_carriers': 'Multiple Carriers',
            'SpiceJet': 'SpiceJet',
            'Vistara': 'Vistara',
            'Trujet': 'Trujet'
        }

        # Format điểm dừng 
        stopage_display = {
            '0': 'Bay thẳng',
            '1': '1 điểm dừng',
            '2': '2 điểm dừng',
            '3': '3 điểm dừng'
        }

        # Chuyển đổi dữ liệu thô 
        features = preprocess_input(data)
        
        # Dữ liệu đầu vào 
        input_array = []
        for column in feature_columns:
            input_array.append(features.get(column, 0))
        
        # Chuyển đổi sang mảng NumPy 
        input_array = np.array([input_array]).astype('float32')
        
        prediction = model.predict(input_array)

        if data['flight_class'] == 'premium_economy':
            prediction *= 1.3
        elif data['flight_class'] == 'business':
            prediction *= 1.5

        # Format kết quả
        formatted_price = "{:,.2f}".format(prediction[0])
        
        return render_template(
            'index.html',
            prediction_text=f'Giá vé dự đoán: {formatted_price}₹ INR',
            success=True,
            dep_date=format_datetime(data['dep_date']),
            arr_date=format_datetime(data['arr_date']),
            source=data['source'],
            destination=data['destination'],
            stopage=stopage_display.get(data['stopage'], data['stopage']),
            airline=airline_display.get(data['airline'], data['airline']),
            flight_class=flight_class_display.get(data['flight_class'], data['flight_class'])
        )

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": "Có lỗi xảy ra khi dự đoán giá vé"}), 500

if __name__ == '__main__':
    app.run(debug=True)
