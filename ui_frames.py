# ui_frames.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import data_manager
import analytics

class WelcomeFrame(ttk.Frame):
    """The first frame the user sees."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Center content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = ttk.Label(self, text="Welcome to our Attendance Management System", style="Title.TLabel")
        label.grid(row=0, column=0, pady=20, sticky="s")
        
        start_button = ttk.Button(self, text="Start",
                                  command=lambda: controller.show_frame("BatchSelectFrame"))
        start_button.grid(row=1, column=0, pady=20, ipadx=20)

class BatchSelectFrame(ttk.Frame):
    """Frame for selecting a batch."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # We will create the buttons when the frame is shown
        # by binding to the <Visibility> event
        self.bind("<Visibility>", self.on_show)
        
    def on_show(self, event):
        # Clear old widgets first
        for widget in self.winfo_children():
            widget.destroy()

        label = ttk.Label(self, text="Please Select a Batch", style="Header.TLabel")
        label.pack(pady=20)

        # Load batches from the data file
        batches = data_manager.load_batches()
        
        # Create a container for the buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        # Create a button for each batch
        row, col = 0, 0
        for batch_name in batches.keys():
            button = ttk.Button(button_frame, text=batch_name, 
                                command=lambda b=batch_name: self.on_batch_select(b))
            button.grid(row=row, column=col, padx=10, pady=10, ipadx=10, ipady=10, sticky="ew")
            
            col += 1
            if col > 2: # Max 3 buttons per row
                col = 0
                row += 1

    def on_batch_select(self, batch_name):
        # 1. Tell the controller which batch is active
        self.controller.current_batch = batch_name
        # 2. Switch to the attendance frame
        self.controller.show_frame("AttendanceFrame")

class AttendanceFrame(ttk.Frame):
    """The main frame for taking attendance."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.student_vars = {} # Dictionary to hold student checkbox variables
        self.current_batch = None
        
        # --- Top Bar (Date and Title) ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=10)
        
        self.title_label = ttk.Label(top_frame, text="Mark Attendance for:", style="Header.TLabel")
        self.title_label.pack(side="left", padx=10)
        
        self.date_entry = ttk.Entry(top_frame, width=12, font=self.controller.label_font)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.date_entry.pack(side="right", padx=10)
        ttk.Label(top_frame, text="Date (YYYY-MM-DD):").pack(side="right")

        # --- Student List Area ---
        # This frame will be populated in refresh_student_list
        self.students_frame = ttk.Frame(self)
        self.students_frame.pack(fill="both", expand=True, padx=10)

        # --- Bottom Bar (Buttons) ---
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill="x", pady=10)

        back_button = ttk.Button(bottom_frame, text="Back to Batches",
                                 command=lambda: controller.show_frame("BatchSelectFrame"))
        back_button.pack(side="left", padx=10)

        analytics_button = ttk.Button(bottom_frame, text="Show Analytics",
                                      command=self.show_analytics)
        analytics_button.pack(side="right", padx=10)

        save_button = ttk.Button(bottom_frame, text="Save Attendance",
                                 command=self.save_attendance)
        save_button.pack(side="right", padx=10)

    def refresh_student_list(self, batch_name):
        """Clears and repopulates the student list for the given batch."""
        self.current_batch = batch_name
        self.title_label.config(text=f"Mark Attendance for: {batch_name}")
        
        # Clear old student widgets
        for widget in self.students_frame.winfo_children():
            widget.destroy()
        
        self.student_vars.clear() # Clear old variables

        # Get students for this batch
        students = data_manager.get_students(batch_name)
        if not students:
            ttk.Label(self.students_frame, text="No students found for this batch.").pack()
            return

        # Add header
        header_frame = ttk.Frame(self.students_frame)
        header_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(header_frame, text="Student Name", style="Header.TLabel").pack(side="left")
        ttk.Label(header_frame, text="Present", style="Header.TLabel").pack(side="right", padx=15)
        
        # ttk.Separator(self.students_frame, orient="horizontal").pack(fill='x', expand=True, pady=5)

        # Create a new entry for each student
        for student_name in students:
            var = tk.IntVar(value=1) # Default to 'Present'
            self.student_vars[student_name] = var
            
            row_frame = ttk.Frame(self.students_frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            
            label = ttk.Label(row_frame, text=student_name)
            label.pack(side="left")
            
            cb = tk.Checkbutton(row_frame, variable=var)
            cb.pack(side="right")

    def save_attendance(self):
        """Gathers data from checkboxes and saves it to the CSV."""
        attendance_date = self.date_entry.get()
        if not self.current_batch:
            messagebox.showerror("Error", "No batch selected.")
            return

        # Prepare records
        records = []
        for student_name, var in self.student_vars.items():
            status = 'Present' if var.get() == 1 else 'Absent'
            records.append({
                'student_name': student_name,
                'status': status
            })
        
        # Call data manager to save
        try:
            success, message = data_manager.save_attendance(attendance_date, self.current_batch, records)
            if success:
                messagebox.showinfo("Success", message)
            else:
                # Ask user if they want to overwrite
                if messagebox.askyesno("Warning", f"{message} Do you want to overwrite it?"):
                    success_ow, msg_ow = data_manager.save_attendance(
                        attendance_date, self.current_batch, records, overwrite=True
                    )
                    if success_ow:
                        messagebox.showinfo("Success", msg_ow)
                    else:
                        messagebox.showerror("Error", msg_ow)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_analytics(self):
        """Opens the analytics window."""
        # We pass the main app window (root) as the parent
        analytics.show_analytics_window(self.controller.root)