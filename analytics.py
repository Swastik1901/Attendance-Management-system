# analytics.py
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_manager import load_attendance_data, load_batches

class AnalyticsWindow:
    """A Toplevel window to display attendance analytics."""
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Attendance Analytics")
        self.window.geometry("800x600")

        # --- Load Data ---
        self.full_data = load_attendance_data()
        self.batches = list(load_batches().keys())

        if self.full_data.empty:
            ttk.Label(self.window, text="No attendance data found to analyze.").pack(pady=20)
            return

        # --- Controls Frame ---
        controls_frame = ttk.Frame(self.window, padding=10)
        controls_frame.pack(fill="x")

        ttk.Label(controls_frame, text="Select Batch:").pack(side="left", padx=5)
        self.batch_var = tk.StringVar()
        self.batch_combo = ttk.Combobox(controls_frame, textvariable=self.batch_var,
                                        values=self.batches)
        self.batch_combo.pack(side="left", padx=5)
        self.batch_combo.bind("<<ComboboxSelected>>", self.update_plot)
        
        if self.batches:
            self.batch_combo.current(0) # Select the first batch by default

        # --- Plot Frame ---
        self.plot_frame = ttk.Frame(self.window)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Matplotlib Figure and Axis
        self.fig, self.ax = plt.subplots()
        
        # Create Tkinter canvas to embed the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Initial plot draw
        self.update_plot()

    def update_plot(self, event=None):
        """Clears and redraws the plot based on the selected batch."""
        selected_batch = self.batch_var.get()
        if not selected_batch:
            return
            
        # 1. Clear the old plot
        self.ax.clear()

        # 2. Filter data for the selected batch
        batch_data = self.full_data[self.full_data['batch'] == selected_batch].copy()
        
        if batch_data.empty:
            self.ax.set_title(f"No Data for {selected_batch}")
            self.canvas.draw()
            return

        # 3. Use NumPy to convert 'Present'/'Absent' to numbers
        batch_data['value'] = np.where(batch_data['status'] == 'Present', 1.0, 0.0)
        
        # 4. Use pandas 'pivot_table' to create the heatmap grid
        try:
            heatmap_data = pd.pivot_table(batch_data,
                                          values='value',
                                          index='student_name',
                                          columns='date',
                                          aggfunc=np.mean)
            
            # Sort by date
            heatmap_data = heatmap_data.reindex(sorted(heatmap_data.columns), axis=1)

        except Exception as e:
            self.ax.set_title(f"Could not create plot: {e}")
            self.canvas.draw()
            return
            
        # 5. --- Create the Heatmap ---
        # `imshow` creates the colored grid
        im = self.ax.imshow(heatmap_data, cmap='RdYlGn', aspect='auto') # Red-Yellow-Green colormap

        # 6. --- Configure Ticks and Labels ---
        # Set student names as Y-axis labels
        self.ax.set_yticks(np.arange(len(heatmap_data.index)))
        self.ax.set_yticklabels(heatmap_data.index)
        
        # Set dates as X-axis labels
        self.ax.set_xticks(np.arange(len(heatmap_data.columns)))
        self.ax.set_xticklabels(heatmap_data.columns, rotation=45, ha="right")

        # Add a color bar to show what 0 (Absent) and 1 (Present) mean
        cbar = self.fig.colorbar(im, ax=self.ax, ticks=[0, 1])
        cbar.ax.set_yticklabels(['Absent', 'Present'])

        self.ax.set_title(f"Attendance Heatmap for {selected_batch}")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Student Name")

        # 7. Redraw the canvas
        self.fig.tight_layout() # Adjusts plot to prevent labels from overlapping
        self.canvas.draw()

def show_analytics_window(parent):
    """Public function to create and show the analytics window."""
    AnalyticsWindow(parent)