# data_manager.py
import os
import json
import pandas as pd
from tkinter import messagebox

# Define file paths
DATA_DIR = "data"
BATCH_FILE = os.path.join(DATA_DIR, "batches.json")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.csv")

def setup_files():
    """Ensures the data directory and necessary files exist."""
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Create sample batch file if it doesn't exist
    if not os.path.exists(BATCH_FILE):
        sample_batches = {
            "CS-101 (Section A)": ["Alice", "Bob", "Charlie", "David"],
            "CS-102 (Section B)": ["Eve", "Frank", "Grace", "Heidi"],
            "MATH-201": ["Ivan", "Judy", "Mallory", "Trent"]
        }
        with open(BATCH_FILE, 'w') as f:
            json.dump(sample_batches, f, indent=4)
            
    # Create empty attendance file if it doesn't exist
    if not os.path.exists(ATTENDANCE_FILE):
        df = pd.DataFrame(columns=["date", "batch", "student_name", "status"])
        df.to_csv(ATTENDANCE_FILE, index=False)

def load_batches():
    """Loads the batch dictionary from the JSON file."""
    try:
        with open(BATCH_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"Could not read {BATCH_FILE}. File may be corrupt.")
        return {}

def get_students(batch_name):
    """Gets the list of students for a specific batch."""
    batches = load_batches()
    return batches.get(batch_name, [])

def load_attendance_data():
    """Loads the entire attendance log into a pandas DataFrame."""
    try:
        return pd.read_csv(ATTENDANCE_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["date", "batch", "student_name", "status"])
    except FileNotFoundError:
        messagebox.showerror("Error", f"{ATTENDANCE_FILE} not found.")
        return pd.DataFrame(columns=["date", "batch", "student_name", "status"])

def save_attendance(date, batch, records, overwrite=False):
    """Saves a new set of attendance records to the CSV."""
    
    # 1. Load existing data
    all_attendance = load_attendance_data()
    
    # 2. Check for duplicates
    date_exists = date in all_attendance['date'].values
    batch_exists = batch in all_attendance[all_attendance['date'] == date]['batch'].values
    
    if date_exists and batch_exists and not overwrite:
        return (False, f"Attendance for {batch} on {date} already exists.")

    # 3. Prepare new records
    new_data = []
    for record in records:
        new_data.append({
            'date': date,
            'batch': batch,
            'student_name': record['student_name'],
            'status': record['status']
        })
    new_df = pd.DataFrame(new_data)
    
    # 4. If overwriting, filter out old data
    if overwrite:
        all_attendance = all_attendance[
            ~((all_attendance['date'] == date) & (all_attendance['batch'] == batch))
        ]
        
    # 5. Append new data and save
    final_df = pd.concat([all_attendance, new_df], ignore_index=True)
    final_df.to_csv(ATTENDANCE_FILE, index=False)
    
    if overwrite:
        return (True, f"Attendance for {batch} on {date} has been overwritten.")
    else:
        return (True, f"Attendance for {batch} on {date} has been saved.")