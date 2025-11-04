# Attendance-Management-System

A simple desktop application built with Python and Tkinter to help teachers and administrators take, manage, and track student attendance.

## 🌟 Features

* **Batch Management:** Organize students into different batches (e.g., "CSE(AIML)", "ECE-Section A").
* **Take Attendance:** Easily mark students as "Present" or "Absent" for the current date.
* **Overwrite Protection:** Prevents accidentally overwriting existing attendance for a date (but allows it if you confirm).
* **Detailed Reports:** View a complete grid report showing all students, all attendance dates, and a summary (Present, Absent, Total, Percent).
* **Data Analytics:** Generate a clean, grouped bar chart to visualize overall "Present" vs. "Absent" stats for a batch.
* **Export to CSV:** Save the detailed report as a `.csv` file for use in Excel or other programs.
* **Auto-Setup:** Automatically creates `students.json` and `attendance.csv` with dummy data on first run.

## 💻 Technology Stack

* **Python 3:** The core programming language.
* **Tkinter:** Python's built-in library for the graphical user interface (GUI).
* **Pandas:** Used for powerful data manipulation and generating report tables.
* **Matplotlib:** Used to create and embed the analytics bar chart.

## ⚙️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install pandas matplotlib
    ```

## ▶️ How to Run

1.  **Run the application:**
    ```bash
    python main.py
    ```
2.  **First Run:** The app will automatically create `students.json` and `attendance.csv`.
3.  **Customize:** You can now close the app and edit `students.json` to add your own batches and student lists before using it.

## 🗂️ File Structure

    .
    ├── app.py              # Main application entry point (controller)
    ├── ui_frames.py        # Contains all GUI frames (pages)
    ├── data_manager.py     # Handles all file I/O (JSON, CSV)
    ├── reports.py          # Logic for the detailed report & analytics windows
    ├── students.json       # Stores batch and student data
    ├── attendance.csv      # Stores all attendance records
    ├── .gitignore          # Tells Git to ignore data files
    └── README.md           # This file
