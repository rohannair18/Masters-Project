import pandas as pd
import numpy as np
import time
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

# Load the dataset
def load_dataset(filename):
    
    dataset = pd.read_csv(filename)
    dataset['timestamp'] = pd.to_datetime(dataset['timestamp'])
    
    # Extract time-based features
    dataset['hour'] = dataset['timestamp'].dt.hour
    dataset['day_of_week'] = dataset['timestamp'].dt.dayofweek
    
    # Categorized activity that are high-risk based on 2024 landscape 
    high_risk_activities = [
        "Data Exfiltration Attempt", "Ransomware Execution", "Zero-Day Exploit Detected",
        "Unauthorized File Access", "Phishing Email Sent", "Cloud Instance Terminated",
        "Unusual API Call", "Command and Control Traffic Detected", "Dark Web Activity Detected"
    ]
    dataset['is_high_risk'] = dataset['activity'].apply(lambda x: 1 if x in high_risk_activities else 0)
    
    # Encoded activity types
    dataset['activity_code'] = dataset['activity'].astype('category').cat.codes
    
    return dataset

# Preprocess data for Isolation Forest
def preprocess_data(dataset):
    
    user_features = dataset.groupby('user_id').agg({
        'hour': ['mean', 'std'],
        'day_of_week': ['mean', 'std'],
        'is_high_risk': 'sum',
        'activity_code': ['nunique', 'count']
    }).fillna(0)

    user_features.columns = ['_'.join(col) for col in user_features.columns]
    user_features.reset_index(inplace=True)
    
    # Normalized features
    scaler = MinMaxScaler()
    feature_columns = [col for col in user_features.columns if col != 'user_id']
    user_features[feature_columns] = scaler.fit_transform(user_features[feature_columns])
    
    return user_features

# Detect anomalies using Isolation Forest
def detect_anomalies(data, contamination=0.01):
    
    # Initialize the Isolation Forest
    model = IsolationForest(n_estimators=300, contamination=contamination, random_state=42)
    
    # Select feature columns
    feature_columns = [col for col in data.columns if col != 'user_id']
    
    # Fit the model and predict anomalies
    data['anomaly'] = model.fit_predict(data[feature_columns])
    return data

# Secondary validation of anomalies
def validate_anomalies(data, original_dataset):
    validated_anomalies = []
    anomalies = data[data['anomaly'] == -1]
    
    for _, row in anomalies.iterrows():
        user_id = row['user_id']
        user_records = original_dataset[original_dataset['user_id'] == user_id]
        
        # Rule-based validation: Check for multiple high-risk activities
        if user_records['is_high_risk'].sum() > 1:  # Customize threshold if needed
            validated_anomalies.append(user_id)
    
    return validated_anomalies

# Display anomalies with suspicious activities
def display_anomalies(data, original_dataset):
    
    # Filter anomalies (users with 'anomaly' == -1)
    anomalies = data[data['anomaly'] == -1]
    
    if anomalies.empty:
        print("No anomalies detected.")
        return
    
    print(f"Total Anomalous Users Detected Before Validation: {len(anomalies)}\n")
    
    # Display anomalies before validation
    print("=== Anomalies Before Validation ===\n")
    for _, row in anomalies.iterrows():
        user_id = row['user_id']
        print(f"--- Anomalous User ID: {user_id} ---")
        
        # Retrieve the user's data from the original dataset (raw, pre-normalized data)
        user_records = original_dataset[original_dataset['user_id'] == user_id]
        
        # Hour Mean and Standard Deviation (raw values)
        hour_mean_raw = user_records['hour'].mean()
        hour_std_raw = user_records['hour'].std()
        
        # Total High-Risk Activities (raw value)
        high_risk_activities_raw = user_records['is_high_risk'].sum()
        
        # Unique Activities (raw value)
        unique_activities_raw = user_records['activity'].nunique()
        
        # Total Activities Logged (raw value)
        total_activities_raw = len(user_records)
        
        # Display the raw values in a neat format
        print(f"  - Hour Mean: {hour_mean_raw:.2f} hours")
        print(f"  - Hour Standard Deviation: {hour_std_raw:.2f} hours")
        print(f"  - Total High-Risk Activities: {high_risk_activities_raw}")
        print(f"  - Unique Activities: {unique_activities_raw}")
        print(f"  - Total Activities Logged: {total_activities_raw}")
        
        # Display suspicious activities related to the user
        suspicious_activities = user_records[user_records['is_high_risk'] == 1]['activity'].tolist()
        if suspicious_activities:
            print(f"  - Suspicious Activities: {', '.join(suspicious_activities)}")
        else:
            print("  - Suspicious Activities: None detected.")
        
        # Extra space between users for readability
        print("\n" + "="*40 + "\n")
    
    # Now we apply the secondary validation step 
    validated_anomalies = validate_anomalies(data, original_dataset)
    
    if validated_anomalies:
        print(f"Total Validated Anomalous Users: {len(validated_anomalies)}\n")
        print("=== Anomalies After Validation ===\n")
        
        # Display anomalies after validation
        for user_id in validated_anomalies:
            print(f"--- Validated Anomalous User ID: {user_id} ---")
            
            # Retrieve the user's data from the original dataset (raw, pre-normalized data)
            user_records = original_dataset[original_dataset['user_id'] == user_id]
            
            # Hour Mean and Standard Deviation (raw values)
            hour_mean_raw = user_records['hour'].mean()
            hour_std_raw = user_records['hour'].std()
            
            # Total High-Risk Activities (raw value)
            high_risk_activities_raw = user_records['is_high_risk'].sum()
            
            # Unique Activities (raw value)
            unique_activities_raw = user_records['activity'].nunique()
            
            # Total Activities Logged (raw value)
            total_activities_raw = len(user_records)
            
            # Display the raw values in a neat format
            print(f"  - Hour Mean: {hour_mean_raw:.2f} hours")
            print(f"  - Hour Standard Deviation: {hour_std_raw:.2f} hours")
            print(f"  - Total High-Risk Activities: {high_risk_activities_raw}")
            print(f"  - Unique Activities: {unique_activities_raw}")
            print(f"  - Total Activities Logged: {total_activities_raw}")
            
            # Display suspicious activities related to the user
            suspicious_activities = user_records[user_records['is_high_risk'] == 1]['activity'].tolist()
            if suspicious_activities:
                print(f"  - Suspicious Activities: {', '.join(suspicious_activities)}")
            else:
                print("  - Suspicious Activities: None detected.")
            
            # Extra space between users for readability
            print("\n" + "="*40 + "\n")
    else:
        print("No validated anomalies detected after applying the validation criteria.")
        
def main():
    # Load and preprocess the dataset
    dataset_filename = "user_behavior_dataset.csv"
    dataset = load_dataset(dataset_filename)
    
    # Preprocess for Isolation Forest
    processed_data = preprocess_data(dataset)
    
    # Detect anomalies
    contamination_rate = 0.01  # Lower contamination rate to minimize false positives
    results = detect_anomalies(processed_data, contamination=contamination_rate)
        
    # Display validated anomalies
    display_anomalies(results, dataset)

start = time.time()
main()
end = time.time()
print("The time of execution of the above program is:", (end - start) * 10**3, "ms")
