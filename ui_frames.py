import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import data_manager
import analytics
import sys

class WelcomeFrame(ttk.Frame):
    """The first frame the user sees."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        
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
        self.bind("<Visibility>", self.on_show)
        
    def on_show(self, event):
        for widget in self.winfo_children():
            widget.destroy()

        label = ttk.Label(self, text="Please Select a Batch", style="Header.TLabel")
        label.pack(pady=20)

        batches = data_manager.load_batches()
        
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        row, col = 0, 0
        batch_keys = batches.keys() if isinstance(batches, dict) else batches
        
        for batch_name in batch_keys:
            button = ttk.Button(button_frame, text=batch_name, 
                                command=lambda b=batch_name: self.on_batch_select(b))
            button.grid(row=row, column=col, padx=10, pady=10, ipadx=10, ipady=10, sticky="ew")
            
            col += 1
            if col > 2:
                col = 0
                row += 1

    def on_batch_select(self, batch_name):
        self.controller.current_batch = batch_name
        self.controller.show_frame("AttendanceFrame")

class AttendanceFrame(ttk.Frame):
    """The main frame for taking attendance."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.student_vars = {} # {roll_no: {'name': name, 'var': var}}
        self.current_batch = None
        
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=10)
        
        self.title_label = ttk.Label(top_frame, text="Mark Attendance for:", style="Header.TLabel")
        self.title_label.pack(side="left", padx=10)
        
        self.date_entry = ttk.Entry(top_frame, width=12, font=self.controller.label_font)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.date_entry.pack(side="right", padx=10)
        ttk.Label(top_frame, text="Date (YYYY-MM-DD):").pack(side="right")

        # --- Setup for Scrollable Frame ---
        
        self.students_frame_container = ttk.Frame(self)
        self.students_frame_container.pack(fill="both", expand=True, padx=10)

        self.canvas = tk.Canvas(self.students_frame_container, background="#f0f0f0", highlightthickness=0)
        
        self.scrollbar = ttk.Scrollbar(self.students_frame_container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Binding 1: Jab bhi inner frame ka size badle, scroll region update karo
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # scrollable_frame ko canvas ke andar daalo
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # --- YEH SCROLLBAR KO FIX KAREGA ---
        # Binding 2: Jab bhi canvas ka size badle (jaise window resize),
        # inner frame ki width ko canvas ki width ke barabar kar do.
        def on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        
        self.canvas.bind("<Configure>", on_canvas_configure)
        # --- END OF SCROLLBAR FIX ---

        # Touchpad/Mouse wheel scrolling
        self.canvas.bind('<Enter>', self._bind_mousewheel)
        self.canvas.bind('<Leave>', self._unbind_mousewheel)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        

        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill="x", pady=10, side="bottom")

        back_button = ttk.Button(bottom_frame, text="Back to Batches",
                                 command=lambda: controller.show_frame("BatchSelectFrame"))
        back_button.pack(side="left", padx=10)

        analytics_button = ttk.Button(bottom_frame, text="Show Charts",
                                      command=self.show_analytics)
        analytics_button.pack(side="right", padx=10)

        report_button = ttk.Button(bottom_frame, text="View Report",
                                     command=self.show_report)
        report_button.pack(side="right", padx=10)

        save_button = ttk.Button(bottom_frame, text="Save Attendance",
                                 command=self.save_attendance)
        save_button.pack(side="right", padx=10)

    def refresh_student_list(self, batch_name):
        self.current_batch = batch_name
        self.title_label.config(text=f"Mark Attendance for: {batch_name}")
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.student_vars.clear()

        students = data_manager.get_students(batch_name)
        if not students:
            ttk.Label(self.scrollable_frame, text="No students found for this batch.").pack()
            return

        # --- SPACIOUS LAYOUT ---
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.pack(fill='x', padx=10, pady=5) # Padding badha di
        ttk.Label(header_frame, text="Roll No.", style="Header.TLabel", width=15).pack(side="left", padx=5)
        ttk.Label(header_frame, text="Student Name", style="Header.TLabel").pack(side="left", padx=5) # Padding add ki
        ttk.Label(header_frame, text="Present", style="Header.TLabel").pack(side="right", padx=20) # Padding badha di
        
        for student in students:
            roll_no = student['roll']
            name = student['name']
            
            var = tk.IntVar(value=0)
            self.student_vars[roll_no] = {'name': name, 'var': var}
            
            # --- SPACIOUS LAYOUT ---
            row_frame = ttk.Frame(self.scrollable_frame)
            row_frame.pack(fill="x", padx=10, pady=5) # Padding badha di
            
            label_roll = ttk.Label(row_frame, text=roll_no, width=15)
            label_roll.pack(side="left", padx=5)
            label_name = ttk.Label(row_frame, text=name)
            label_name.pack(side="left", padx=5) # Padding add ki
            
            # ... (refresh_student_list ka baaki code) ...
            cb = tk.Checkbutton(row_frame, variable=var)
            cb.pack(side="right", padx=15) # <-- Is line ko aise theek karein

    # YAHAN SE UNINDENT KAREIN (refresh_student_list ke level par)
    def save_attendance(self):
        # ... (Yeh function poora same hai, koi change nahi) ...
        attendance_date = self.date_entry.get()
        try:
            datetime.strptime(attendance_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", 
                                 "Invalid date format.\nPlease use YYYY-MM-DD.")
            return

        if not self.current_batch:
            messagebox.showerror("Error", "No batch selected.")
            return

        records = []
        for roll_no, data in self.student_vars.items():
            status = 'Present' if data['var'].get() == 1 else 'Absent'
            records.append({
                'roll_no': roll_no,
                'student_name': data['name'],
                'status': status
            })
        
        try:
            success, message = data_manager.save_attendance(attendance_date, self.current_batch, records)
            if success:
                messagebox.showinfo("Success", message)
            else:
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

    def show_report(self):
        # ... (Yeh function poora same hai, koi change nahi) ...
        if not self.current_batch:
            messagebox.showerror("Error", "No batch selected.")
            return
        analytics.show_detailed_report_window(self.controller, self.current_batch)

    def show_analytics(self):
        # ... (Yeh function poora same hai, koi change nahi) ...
        if not self.current_batch:
             messagebox.showerror("Error", "No batch selected.")
             return
        analytics.show_analytics_window(self.controller, self.current_batch)

    # --- YEH NAYA SCROLL FUNCTION HAI (ERROR FIXED) ---
    
    def _on_mousewheel(self, event):
        """Cross-platform mouse wheel scroll"""
        try:
            # --- Windows and macOS ---
            if sys.platform == "darwin": # macOS
                scroll_val = -1 * event.delta
            else: # Windows
                scroll_val = -1 * (event.delta // 120)
                
            self.canvas.yview_scroll(scroll_val, "units")
            
        except AttributeError:
            # --- Linux ---
            if event.num == 4: # Scroll up
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5: # Scroll down
                self.canvas.yview_scroll(1, "units")

    def _bind_mousewheel(self, event):
        """Bind mouse wheel events when mouse enters canvas."""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        """Unbind mouse wheel events when mouse leaves canvas."""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")