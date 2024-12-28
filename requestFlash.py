import joblib
import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

# Load model
model = joblib.load('colab/xgboost_model.pkl')

# Danh sách các thông tin mô phỏng
airlines = ['Air_India', 'GoAir', 'IndiGo', 'Jet_Airways', 'Multiple_carriers', 'SpiceJet', 'Vistara', 'Trujet']
sources = ['Delhi', 'Mumbai', 'Kolkata', 'Chennai']
destinations = ['Cochin', 'Hyderabad', 'New Delhi', 'Delhi']
flight_classes = ['economy', 'premium_economy', 'business']
stopages = ['0', '1', '2', '3']

# Các cột feature mà model yêu cầu
feature_columns = [
    'Total_Stops', 'Journey_Day', 'Journey_Month', 'Dep_Hour', 'Dep_Minute',
    'Arrival_Hour', 'Arrival_Minute', 'Duration_Hours', 'Duration_Minutes',
    'Total_Duration_Minutes', 'Air_India', 'GoAir', 'IndiGo', 'Jet_Airways',
    'Jet_Airways_Business', 'Multiple_carriers', 
    'Multiple_carriers_Premium_economy', 'SpiceJet', 'Trujet', 'Vistara',
    'Vistara_Premium_economy', 'Chennai', 'Delhi', 'Kolkata', 'Mumbai',
    'Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi'
]

# Hàm tạo dữ liệu mô phỏng
def generate_random_data():
    departure_date = datetime.now() + timedelta(days=random.randint(1, 30))
    arrival_date = departure_date + timedelta(hours=random.randint(1, 12))
    
    data = {
        'dep_date': departure_date,
        'arr_date': arrival_date,
        'source': random.choice(sources),
        'destination': random.choice(destinations),
        'airline': random.choice(airlines),
        'stopage': random.randint(0, 3),
        'duration_hours': random.randint(1, 12),
        'duration_minutes': random.randint(0, 59),
        'flight_class': random.choice(flight_classes)
    }
    return data

# Hàm tiền xử lý dữ liệu đầu vào
def preprocess_input(data):
    dep_date = data['dep_date']
    arr_date = data['arr_date']

    features = {
        'Journey_Day': dep_date.day,
        'Journey_Month': dep_date.month,
        'Dep_Hour': dep_date.hour,
        'Dep_Minute': dep_date.minute,
        'Arrival_Hour': arr_date.hour,
        'Arrival_Minute': arr_date.minute,
        'Total_Stops': data['stopage'],
        'Duration_Hours': data['duration_hours'],
        'Duration_Minutes': data['duration_minutes'],
        'Total_Duration_Minutes': (data['duration_hours'] * 60 + data['duration_minutes'])
    }

    # Encode airline
    for airline in airlines:
        features[airline] = 1 if data['airline'] == airline else 0

    # Encode source
    for source in sources:
        features[source] = 1 if data['source'] == source else 0

    # Encode destination
    for dest in destinations:
        features[dest] = 1 if data['destination'] == dest else 0

    # Chuẩn hóa đầu vào để khớp với các cột của model
    input_array = [features.get(column, 0) for column in feature_columns]

    return np.array([input_array]).astype('float32')

# Hàm chạy nhiều dự đoán
def run_predictions(n=10):
    for i in range(n):
        data = generate_random_data()
        if data['source'] == data['destination']:
            continue  # Bỏ qua nếu source và destination trùng nhau
        
        # Tiền xử lý
        input_data = preprocess_input(data)
        
        # Dự đoán
        prediction = model.predict(input_data)
        
        # Điều chỉnh giá theo hạng ghế
        if data['flight_class'] == 'premium_economy':
            prediction *= 1.3
        elif data['flight_class'] == 'business':
            prediction *= 1.5
        
        formatted_price = "{:,.2f}".format(prediction[0])
        
        # Hiển thị dữ liệu đầu vào và giá dự đoán
        print(f"[{i+1}] Dự đoán giá vé: {formatted_price}₹ INR")
        print(f"  - Ngày đi: {data['dep_date'].strftime('%Y-%m-%d %H:%M')}")
        print(f"  - Ngày đến: {data['arr_date'].strftime('%Y-%m-%d %H:%M')}")
        print(f"  - Điểm đi: {data['source']}")
        print(f"  - Điểm đến: {data['destination']}")
        print(f"  - Hãng bay: {data['airline']}")
        print(f"  - Điểm dừng: {data['stopage']}")
        print(f"  - Thời lượng bay: {data['duration_hours']} giờ {data['duration_minutes']} phút")
        print(f"  - Hạng ghế: {data['flight_class'].replace('_', ' ').capitalize()}")
        print("---------------------------------------------------")

# Chạy 20 dự đoán
run_predictions(20)
