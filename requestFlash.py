import joblib
import numpy as np
import pandas as pd
import time

# Load model
model = joblib.load('colab/xgboost_model.pkl')

# Load dữ liệu từ file CSV
file_path = 'data/processed/cleaned_test_data.csv'
data = pd.read_csv(file_path)

# Chuyển đổi ngày tháng và thời gian từ CSV (fix UserWarning)
data['Date_of_Journey'] = pd.to_datetime(data['Date_of_Journey'], format='%d/%m/%Y')
data['Journey_Day'] = data['Date_of_Journey'].dt.day
data['Journey_Month'] = data['Date_of_Journey'].dt.month

# Xử lý thời gian (chỉ lấy giờ phút, bỏ phần ngày)
data['Dep_Time'] = pd.to_datetime(data['Dep_Time'].str.split().str[0], format='%H:%M')
data['Dep_Hour'] = data['Dep_Time'].dt.hour
data['Dep_Minute'] = data['Dep_Time'].dt.minute

data['Arrival_Time'] = pd.to_datetime(data['Arrival_Time'].str.split().str[0], format='%H:%M')
data['Arrival_Hour'] = data['Arrival_Time'].dt.hour
data['Arrival_Minute'] = data['Arrival_Time'].dt.minute

# Xử lý Total_Stops (convert text to number)
def convert_stops(stops):
    if 'non-stop' in stops.lower():
        return 0
    return int(stops.split()[0])  # Lấy số từ chuỗi (ví dụ: '1 stop' -> 1)

data['Total_Stops'] = data['Total_Stops'].apply(convert_stops)

# Các cột cần thiết cho model
feature_columns = [
    'Total_Stops', 'Journey_Day', 'Journey_Month', 'Dep_Hour', 'Dep_Minute',
    'Arrival_Hour', 'Arrival_Minute', 'Duration_Hours', 'Duration_Minutes',
    'Total_Duration_Minutes', 'Air_India', 'GoAir', 'IndiGo', 'Jet_Airways',
    'Jet_Airways_Business', 'Multiple_carriers', 
    'Multiple_carriers_Premium_economy', 'SpiceJet', 'Trujet', 'Vistara',
    'Vistara_Premium_economy', 'Chennai', 'Delhi', 'Kolkata', 'Mumbai',
    'Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi'
]

# Hàm xử lý dữ liệu trước khi dự đoán (fix lỗi Duration)
def preprocess_csv_input(df):
    processed_data = []
    rows = []

    for _, row in df.iterrows():
        try:
            # Xử lý Duration (giờ và phút)
            duration = row['Duration']
            if 'h' in duration and 'm' in duration:
                hours = int(duration.split('h')[0])
                minutes = int(duration.split('h')[1].split('m')[0])
            elif 'h' in duration:
                hours = int(duration.split('h')[0])
                minutes = 0
            elif 'm' in duration:
                hours = 0
                minutes = int(duration.split('m')[0])
            else:
                hours = 0
                minutes = 0  # Trường hợp không có thông tin, mặc định là 0

            features = {
                'Total_Stops': row['Total_Stops'],
                'Journey_Day': row['Journey_Day'],
                'Journey_Month': row['Journey_Month'],
                'Dep_Hour': row['Dep_Hour'],
                'Dep_Minute': row['Dep_Minute'],
                'Arrival_Hour': row['Arrival_Hour'],
                'Arrival_Minute': row['Arrival_Minute'],
                'Duration_Hours': hours,
                'Duration_Minutes': minutes,
                'Total_Duration_Minutes': hours * 60 + minutes
            }
            
            # One-hot encode airline, source, destination
            for col in feature_columns:
                if col not in features:
                    features[col] = 0

            if row['Airline'] in feature_columns:
                features[row['Airline']] = 1
            if row['Source'] in feature_columns:
                features[row['Source']] = 1
            if row['Destination'] in feature_columns:
                features[row['Destination']] = 1
            
            input_array = [features.get(column, 0) for column in feature_columns]
            processed_data.append(input_array)
            rows.append(row)

        except Exception as e:
            print(f"Lỗi ở dòng {_ + 1}: {str(e)} - Ghi log lỗi.")
            rows.append(row)  # Thêm dòng bị lỗi để vẫn dự đoán
            processed_data.append([0] * len(feature_columns))  # Thêm giá trị 0 cho dòng lỗi
    
    return np.array(processed_data).astype('float32'), rows

# Tiền xử lý dữ liệu
input_data, raw_rows = preprocess_csv_input(data)

# Dự đoán giá vé
predictions = model.predict(input_data)

# In và lưu kết quả
results = []
for i, row in enumerate(raw_rows):
    predicted_price = predictions[i]
    
    # Điều chỉnh giá theo hạng ghế
    if 'premium' in row['Additional_Info'].lower():
        predicted_price *= 1.3
    elif 'business' in row['Additional_Info'].lower():
        predicted_price *= 1.5

    formatted_price = "{:,.2f}".format(predicted_price)
    
    # Lưu vào list kết quả
    results.append({
        'Source': row['Source'],
        'Destination': row['Destination'],
        'Airline': row['Airline'],
        'Predicted_Price': formatted_price,
        'Departure_Date': row['Date_of_Journey'].strftime('%Y-%m-%d'),
        'Arrival_Time': row['Arrival_Time'].strftime('%H:%M'),
        'Total_Stops': row['Total_Stops'],
        'Duration': row['Duration'],
        'Class': row['Additional_Info']
    })

    # In từng dòng với hiệu ứng delay
    print(f"{row['Source']:>8} -> {row['Destination']:<12} | "
          f"{row['Airline']:<20} | Giá: {formatted_price} | "
          f"Ngày: {row['Date_of_Journey'].strftime('%Y-%m-%d')} | "
          f"Dừng: {row['Total_Stops']} | Thời gian bay: {row['Duration']}")
    
    time.sleep(0.01)  # Delay 10ms giữa các dòng

# Lưu vào file CSV
results_df = pd.DataFrame(results)
results_df.to_csv('data/results/predicted_results.csv', index=False)
print("\nKết quả dự đoán từ tệp test đã được lưu vào 'predicted_results.csv'")
