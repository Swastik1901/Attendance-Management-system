import pandas as pd
import os
import json
from tkinter import messagebox

# --- Define filenames ---
STUDENTS_FILE = 'students.json'
ATTENDANCE_FILE = 'attendance.csv'

# --- NEW FUNCTION ---
def setup_files():
    """Checks for data files and creates them if they don't exist."""
    
    # 1. Check for students.json
    if not os.path.exists(STUDENTS_FILE):
        # --- CHANGED ---
        # Data structure now includes roll numbers
        dummy_students = {
            "CSE(AIML)": [
                {"roll": "2461001", "name": "Aditya Aman"},
                {"roll": "2461002", "name": "Adarsha Ghosh"},
                {"roll": "2461003", "name": "Indranil Chongdar"},
                {"roll": "2461004", "name": "Arya Biswas"},
                {"roll": "2461005", "name": "Soumyadip Mitra"},
                {"roll": "2461006", "name": "Abhishek Saha"},
                {"roll": "2461008", "name": "Rakesh Adak"},
                {"roll": "2461010", "name": "Prity Kumari"},
                {"roll": "2461011", "name": "Koushik Ghosh"},
                {"roll": "2461012", "name": "Bikram Mondal"},
                {"roll": "2461013", "name": "Md. Farhan Akhtar"},
                {"roll": "2461015", "name": "Shivam Kumar Gupta"},
                {"roll": "2461016", "name": "Himanshu Ranjan"},
                {"roll": "2461017", "name": "Golu Kumar"},
                {"roll": "2461018", "name": "Eric Wilson Tirkey"},
                {"roll": "2461019", "name": "Kannkanaa Sanyal"},
                {"roll": "2461021", "name": "Arijit Sarkar"},
                {"roll": "2461022", "name": "Satyam Raj"},
                {"roll": "2461023", "name": "Tapomay Bandyopadhyay"},
                {"roll": "2461024", "name": "Sayan Biswas"},
                {"roll": "2461026", "name": "Baibhab Nag"},
                {"roll": "2461027", "name": "Soha Alam Mondal"},
                {"roll": "2461028", "name": "Ritamvar Sen"},
                # {"roll": "2461029", "name": "Debasish Sarkar"},
                # {"roll": "2461030", "name": "Shaurya Veer Singh"},
                # {"roll": "2461031", "name": "Mohikshit Ghorai"},
                # {"roll": "2461032", "name": "Jiya Singh"},
                # {"roll": "2461033", "name": "Yash Aditya"},
                # {"roll": "2461034", "name": "Sambit Sinha"},
                # {"roll": "2461035", "name": "Prakhar Dhangar"},
                # {"roll": "2461036", "name": "Gautam Kumar"},
                # {"roll": "2461038", "name": "Somsubhra Dalui"},
                # {"roll": "2461040", "name": "Tushar Kumar Jha"},
                # {"roll": "2461041", "name": "Goutam Samanta"},
                # {"roll": "2461043", "name": "Anish Khan"},
                # {"roll": "2461045", "name": "Santanu Choudhary"},
                # {"roll": "2461046", "name": "Aarav Kumar"},
                # {"roll": "2461047", "name": "Shekhar Suman"},
                # {"roll": "2461048", "name": "Reetooza Paul"},
                # {"roll": "2461050", "name": "Sadhitra Mondal"},
                # {"roll": "2461051", "name": "K V Rohit"},
                # {"roll": "2461052", "name": "Shruti Kumari"},
                # {"roll": "2461053", "name": "Rahul Kumar "},
                # {"roll": "2461054", "name": "Prayas Mondal"},
                # {"roll": "2461056", "name": "Ashutosh Singh Yadav"},
                # {"roll": "2461057", "name": "Soumyajit Chaudhury"},
                # {"roll": "2461058", "name": "Ashish Kumar Jha"},
                # {"roll": "2461059", "name": " Swastik Kumar"},
                # {"roll": "2461061", "name": "Harsh Vardhan Bhardwaj"},
                # {"roll": "2461062", "name": "Alisha Jaiswal"},
                # {"roll": "2461063", "name": "Anshika Vishwakarma"},
                # {"roll": "2461064", "name": "Ayush Kumar rout"},
                # {"roll": "2461065", "name": "Diganta Parui"},
                # {"roll": "2461066", "name": "Sarthak Choudhuri"},
                # {"roll": "2461069", "name": "Priyanshu Sharma"},
                # {"roll": "2461070", "name": "Ayushi Thakur"},
                # {"roll": "2461071", "name": "Anneshwa Das"},
                # {"roll": "2461073", "name": "PRASANSHA PRIYA"},
                # {"roll": "2461074", "name": "ADRIJA BANERJEE"},
                # {"roll": "2461075", "name": "ANCHAL KUMARI"},
                # {"roll": "2461076", "name": "AASHI KAUR"},
                # {"roll": "2461077", "name": "BHOOMI LADIA"},
                # {"roll": "2461078", "name": "UPASANA MAJUMDER"},
            ],
            "ECE-Section A": [
                {"roll": "ECE/25/001", "name": "Eve"},
                {"roll": "ECE/25/002", "name": "Frank"},
                {"roll": "ECE/25/003", "name": "Grace"},
                {"roll": "ECE/25/004", "name": "Heidi"}
            ],
            "ME": [
                {"roll": "ME/25/001", "name": "Ivan"},
                {"roll": "ME/25/002", "name": "Judy"},
                {"roll": "ME/25/003", "name": "Mallory"},
                {"roll": "ME/25/004", "name": "Niaj"}
            ]
        }
        try:
            with open(STUDENTS_FILE, 'w') as f:
                json.dump(dummy_students, f, indent=4)
        except Exception as e:
            messagebox.showerror("Setup Error", f"Could not create {STUDENTS_FILE}: {e}")

    # 2. Check for attendance.csv
    if not os.path.exists(ATTENDANCE_FILE):
        try:
            # --- CHANGED ---
            # Added 'roll_no' to the headers
            headers = pd.DataFrame(columns=['roll_no', 'student_name', 'status', 'date', 'batch'])
            headers.to_csv(ATTENDANCE_FILE, index=False)
        except Exception as e:
            messagebox.showerror("Setup Error", f"Could not create {ATTENDANCE_FILE}: {e}")

# --- Existing Functions ---

def load_batches():
    """Loads batch names from the students file."""
    try:
        with open(STUDENTS_FILE, 'r') as f:
            data = json.load(f)
            return data # Return the whole dict
    except FileNotFoundError:
        messagebox.showerror("Error", f"{STUDENTS_FILE} not found.")
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"Error loading batches: {e}")
        return {}

def get_students(batch_name):
    """Gets a list of student dicts ({roll, name}) for a batch."""
    try:
        with open(STUDENTS_FILE, 'r') as f:
            data = json.load(f)
            # --- CHANGED ---
            # This now returns the list of dictionaries
            return data.get(batch_name, [])
    except FileNotFoundError:
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Error getting students: {e}")
        return []

def save_attendance(attendance_date, batch_name, records, overwrite=False):
    """
    Saves attendance records to the main CSV file.
    Assumes 'records' is a list of dicts:
    [{'roll_no': 'R1', 'student_name': 'S1', 'status': 'P'}, ...]
    """
    # --- CHANGED ---
    # The DataFrame will now automatically include 'roll_no' if it's in 'records'
    new_df = pd.DataFrame(records)
    new_df['date'] = attendance_date
    new_df['batch'] = batch_name
    
    try:
        if os.path.exists(ATTENDANCE_FILE):
            main_df = pd.read_csv(ATTENDANCE_FILE)
            exists = ((main_df['date'] == attendance_date) & 
                      (main_df['batch'] == batch_name)).any()
            
            if exists:
                if not overwrite:
                    return False, "Attendance for this date and batch already exists."
                main_df = main_df.drop(
                    main_df[(main_df['date'] == attendance_date) & (main_df['batch'] == batch_name)].index
                )
        else:
            # --- CHANGED ---
            # Ensure new DataFrame has the 'roll_no' column
            main_df = pd.DataFrame(columns=['roll_no', 'student_name', 'status', 'date', 'batch'])

        final_df = pd.concat([main_df, new_df], ignore_index=True)
        final_df.to_csv(ATTENDANCE_FILE, index=False)
        return True, "Attendance saved successfully."
    
    except Exception as e:
        return False, f"An error occurred while saving: {e}"

def get_report_data(batch_name):
    """Loads and processes all attendance data for a specific batch."""
    if not os.path.exists(ATTENDANCE_FILE):
        return None, "No attendance data file found."

    try:
        df = pd.read_csv(ATTENDANCE_FILE)
        # --- FIX: Ensure 'roll_no' is always treated as a string ---
        # This prevents dtype mismatch errors during merge.
        df['roll_no'] = df['roll_no'].astype(str)
        # --- FIX: Handle case where attendance file exists but is empty ---
        if df.empty:
            return None, "No attendance data has been recorded yet."
            
        # --- FIX: Ensure all students from the roster are included in the report ---
        # 1. Get the full student roster for the batch
        all_students = get_students(batch_name)
        if not all_students:
            return None, f"No students found in the roster for batch '{batch_name}'."

        # Create a base DataFrame from the full roster
        roster_df = pd.DataFrame(all_students).rename(columns={'roll': 'roll_no', 'name': 'student_name'})
        # Also ensure the roster's roll_no is a string for consistency
        roster_df['roll_no'] = roster_df['roll_no'].astype(str)

        # Filter attendance data for the current batch
        batch_df = df[df['batch'] == batch_name]

        # If attendance data exists, pivot and merge it with the roster
        if batch_df.empty:
            # If no attendance records, the report is just the roster
            report_df = roster_df
        else:
            # Pivot the existing attendance data
            pivot_df = batch_df.pivot_table(
                index=['roll_no', 'student_name'],
                columns='date',
                values='status',
                aggfunc='first'
            )
            # Merge the roster with the pivoted data
            report_df = pd.merge(roster_df, pivot_df, on=['roll_no', 'student_name'], how='left')

        report_df['Present'] = (report_df == 'Present').sum(axis=1)
        report_df['Absent'] = (report_df == 'Absent').sum(axis=1)
        report_df['Total'] = report_df['Present'] + report_df['Absent']
        # Use a safe division to prevent errors when Total is 0
        report_df['Percent'] = (report_df['Present'].div(report_df['Total']).fillna(0) * 100).round(1)

        # --- CHANGED ---
        # Rename columns for better readability
        report_df = report_df.rename(columns={'student_name': 'Name', 'roll_no': 'Roll No.'})
        
        # --- CHANGED ---
        # Reorder columns to be more logical, putting Roll No. first
        date_cols = [col for col in report_df.columns if col not in ['Roll No.', 'Name', 'Present', 'Absent', 'Total', 'Percent']]
        final_cols = ['Roll No.', 'Name'] + date_cols + ['Present', 'Absent', 'Total', 'Percent']
        report_df = report_df[final_cols]
        
        return report_df, "Report generated successfully."

    except Exception as e:
        return None, f"Error generating report: {e}"
