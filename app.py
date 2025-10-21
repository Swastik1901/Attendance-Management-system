# app.py
import tkinter as tk
from tkinter import ttk, font
import ui_frames

class AttendanceApp:
    """
    The main application controller. It manages the root window
    and switches between different frames (pages).
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("700x550")
        
        # --- Theme and Style ---
        self.style = ttk.Style()
        self.style.theme_use('clam') # A clean, modern theme

        # Define custom fonts
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=11)
        self.button_font = font.Font(family="Helvetica", size=10, weight="bold")

        # Configure styles
        self.style.configure("TLabel", font=self.label_font)
        self.style.configure("Title.TLabel", font=self.title_font, padding=(0, 10, 0, 10))
        self.style.configure("TButton", font=self.button_font, padding=10)
        self.style.configure("Header.TLabel", font=font.Font(family="Helvetica", size=12, weight="bold"))

        # This variable will store which batch is currently selected
        self.current_batch = None

        # --- Frame Container ---
        # This container will hold all the different pages
        container = ttk.Frame(root)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Loop through all the page classes from ui_frames
        for F in (ui_frames.WelcomeFrame, ui_frames.BatchSelectFrame, ui_frames.AttendanceFrame):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame
            # Place all frames in the same grid cell; only the one
            # on top (raised) will be visible.
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial welcome frame
        self.show_frame("WelcomeFrame")

    def show_frame(self, frame_name):
        """Raises the specified frame to the top, making it visible."""
        
        # --- SPECIAL LOGIC ---
        # Before showing the AttendanceFrame, we MUST tell it to
        # refresh its student list based on the currently selected batch.
        if frame_name == "AttendanceFrame":
            if self.current_batch:
                self.frames[frame_name].refresh_student_list(self.current_batch)
            else:
                # Failsafe, should not happen in normal flow
                self.show_frame("BatchSelectFrame")
                return
        
        # Raise the new frame to the top
        frame = self.frames[frame_name]
        frame.tkraise()