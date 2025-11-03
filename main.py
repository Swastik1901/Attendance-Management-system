import tkinter as tk
from tkinter import ttk, font
import ui_frames
import data_manager

class AttendanceApp(tk.Tk):
    """Main application controller."""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        data_manager.setup_files()
        
        self.title("Attendance Management System")
        self.geometry("800x600")

        # --- Configure Styles ---
        self.style = ttk.Style(self)
        self.style.theme_use("clam") # Feel free to change this

        # Define fonts
        self.title_font = font.Font(family='Helvetica', size=20, weight='bold')
        self.header_font = font.Font(family='Helvetica', size=14, weight='bold')
        self.label_font = font.Font(family='Helvetica', size=12)

        # Configure styles
        self.style.configure("Title.TLabel", font=self.title_font, padding=20)
        self.style.configure("Header.TLabel", font=self.header_font, padding=10)
        self.style.configure("TLabel", font=self.label_font, padding=5)
        self.style.configure("TButton", font=self.label_font, padding=10)
        self.style.configure("TFrame", background="#f0f0f0") # Light gray bg
        self.configure(background="#f0f0f0")

        # --- Frame Management ---
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.current_batch = None # Store the active batch
        self.frames = {} # Dictionary to hold all frames

        # Load all frames
        for F in (ui_frames.WelcomeFrame, ui_frames.BatchSelectFrame, ui_frames.AttendanceFrame):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start by showing the Welcome frame
        self.show_frame("WelcomeFrame")

    def show_frame(self, frame_name):
        """Raises the selected frame to the top."""
        frame = self.frames[frame_name]
        
        # If we are showing AttendanceFrame, we MUST refresh its list
        if frame_name == "AttendanceFrame":
            if self.current_batch:
                frame.refresh_student_list(self.current_batch)
            else:
                # This shouldn't happen, but as a fallback:
                self.show_frame("BatchSelectFrame")
                return
                
        frame.tkraise()

if __name__ == "__main__":
    # --- THIS IS THE FIX ---
    # Run the setup function *before* starting the app
    data_manager.setup_files()
    
    app = AttendanceApp()
    app.mainloop()