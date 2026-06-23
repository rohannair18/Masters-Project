import random
import uuid
import csv
from datetime import datetime, timedelta

# Define activities aligned with the 2024 threat landscape
activities = [
    "Login Success", "Login Failure", "Multiple Failed Login Attempts", "Password Change",
    "MFA Enabled", "MFA Disabled", "Password Reset Request", "File Access", "File Download",
    "File Upload", "File Modification", "Unauthorized File Access", "Data Exfiltration Attempt",
    "Bulk Data Download", "Privilege Escalation Attempt", "Role Change", "New Admin User Created",
    "User Deactivation", "VPN Login", "VPN Login Failure", "Unusual Network Traffic",
    "Access from High-Risk Location", "New Device Connected", "Firewall Policy Update",
    "Anomalous Behavior Detected", "Unusual Time of Activity", "Suspicious File Upload",
    "Malware Detected", "Phishing Email Sent", "Ransomware Execution", "Mass Email Sent",
    "Spam Email Detected", "Email Sent to External Domain", "Unauthorized Email Forwarding Enabled",
    "Application Whitelist Updated", "Application Whitelist Disabled", "Unapproved Application Installed",
    "Unauthorized System Reboot", "Critical System Error", "Cloud Instance Created",
    "Cloud Instance Terminated", "IAM Policy Updated", "Unusual API Call",
    "Resource Misconfiguration Detected", "Unauthorized Cloud Resource Access",
    "Antivirus Disabled", "Antivirus Scan Initiated", "New USB Device Connected", "USB Device Blocked",
    "Data Transfer to USB Device", "Access to Sensitive Data", "Unusual Access to HR Files",
    "Unusual Access to Financial Records", "Sudden Increase in Activity Volume", "DDoS Attack Detected",
    "Command and Control Traffic Detected", "Zero-Day Exploit Detected", "Policy Violation Detected",
    "Brute Force Attack Detected", "Dark Web Activity Detected"
]

# Helper function to generate pseudonymized user ID
def generate_pseudonymized_user(users_pool, num_users=1000):
    
    #To Ensure that some users are repeated in the dataset.
    
    if len(users_pool) < num_users:
        for _ in range(num_users - len(users_pool)):
            users_pool.append(str(uuid.uuid4()))
    return random.choice(users_pool)

# Helper function to generate a random timestamp within the last 30 days
def random_timestamp():
    now = datetime.now()
    start = now - timedelta(days=30)
    random_time = start + (now - start) * random.random()
    return random_time.strftime("%Y-%m-%d %H:%M:%S")

# Generate dataset
def generate_dataset(num_records, num_users=1000):
    dataset = []
    users_pool = []  # Pool of user IDs
    for _ in range(num_records):
        record = {
            "timestamp": random_timestamp(),
            "user_id": generate_pseudonymized_user(users_pool, num_users),
            "activity": random.choice(activities)
        }
        dataset.append(record)
    return dataset

# Write dataset to CSV
def write_to_csv(dataset, filename="user_behavior_dataset.csv"):
    fieldnames = ["timestamp", "user_id", "activity"]
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)

# Main
def main():
    num_records = 10000  # Number of activity records to generate
    num_users = 1000  # Number of unique pseudonymized users
    dataset = generate_dataset(num_records, num_users)
    write_to_csv(dataset)
    print(f"Dataset with {num_records} records written to 'user_behavior_dataset.csv'.")

main()
