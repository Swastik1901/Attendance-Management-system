# main.py
import tkinter as tk
from app import AttendanceApp
import data_manager

if __name__ == "__main__":
    # 1. Set up the necessary data files and folders
    data_manager.setup_files()
    
    # 2. Create the main application window
    root = tk.Tk()
    
    # 3. Start the application logic
    app = AttendanceApp(root)
    
    # 4. Run the main loop
    root.mainloop()