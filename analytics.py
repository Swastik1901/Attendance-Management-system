import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import data_manager

# Requires:
# pip install matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_analytics_chart(parent_frame, batch_name):
    """
    Creates and embeds a grouped bar chart for attendance into a given parent frame.
    """
    import numpy as np
    from matplotlib import ticker

    # Clear any previous widgets in the frame
    for widget in parent_frame.winfo_children():
        widget.destroy()

    df, msg = data_manager.get_report_data(batch_name)
    if df is None or df.empty:
        ttk.Label(parent_frame, text=msg, style="Header.TLabel").pack(pady=50)
        return

    try:
        # Ensure numeric columns
        df['Present'] = pd.to_numeric(df['Present'], errors='coerce').fillna(0).astype(int)
        df['Absent']  = pd.to_numeric(df['Absent'],  errors='coerce').fillna(0).astype(int)

        # Ensure 'Roll No.' column exists and is a string for label creation
        df['Student'] = df['Roll No.'].astype(str) + " - " + df['Name'].astype(str)

        n = len(df)
        # Figure size: widen when many students
        fig_w = max(12, n * 1.2)   # Increased multiplier for more space per student
        fig_h = 9                   # taller for more vertical space
        fig = Figure(figsize=(fig_w, fig_h), dpi=140)
        ax = fig.add_subplot(111)

        indices = np.arange(n)
        bar_width = 0.25  # Slightly reduced bar width for more space between bars

        # Bars with solid edge so each bar stands out
        present_bars = ax.bar(indices - bar_width/2, df['Present'],
                              width=bar_width, label='Present',
                              color='#2B8CFF', edgecolor='black', linewidth=0.6)
        absent_bars  = ax.bar(indices + bar_width/2, df['Absent'],
                              width=bar_width, label='Absent',
                              color='#FF4D4D', edgecolor='black', linewidth=0.6)

        # Title & labels (slightly larger)
        ax.set_title('Overall Attendance Summary', fontsize=20, fontweight='bold', pad=16)
        ax.set_xlabel('Students', fontsize=15, labelpad=12)
        ax.set_ylabel('Number of Days', fontsize=15, labelpad=12)

        # X ticks and smaller student name font
        ax.set_xticks(indices)
        # Use full student name for labels
        label_fontsize = 9 if n <= 15 else 7   # smaller when many students
        rotation = 30 if n <= 12 else 60
        ax.set_xticklabels(df['Student'], rotation=rotation, ha='right', fontsize=label_fontsize)

        # Y ticks readability
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=label_fontsize)

        # Provide extra space at left/right of bars so they don't touch axis edges
        ax.set_xlim(-0.7, n - 0.3) # Adjusted limits for more padding
        ax.margins(x=0.02)

        # Gridlines
        ax.grid(axis='y', linestyle='--', alpha=0.45)

        # Put legend above the chart (keeps plotting area spacious)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.09), ncol=2, fontsize=12, frameon=False) # Slightly higher legend

        # Increase the margins around the plot area so labels & legend have room
        fig.subplots_adjust(left=0.06, right=0.98, top=0.88, bottom=0.26) # Adjusted margins

        # Embed in Tk window
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=20, pady=20) # Increased padding

    except Exception as e:
        messagebox.showerror("Chart Error", f"Could not generate chart: {e}", parent=parent_frame)


def create_detailed_report(parent_frame, batch_name):
    """
    Creates and embeds a detailed report Treeview into a given parent frame.
    """
    # Clear any previous widgets in the frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
        
    df, msg = data_manager.get_report_data(batch_name)
    if df is None or df.empty:
        ttk.Label(parent_frame, text=msg, style="Header.TLabel").pack(pady=50)
        return

    # Try to find the max total days, default to 'N/A' if it fails
    try:
        total_days = df['Total'].max()
        title_text = f"Attendance Report ({total_days} days)"
    except Exception:
        title_text = "Attendance Report"

    title_label = ttk.Label(parent_frame, text=title_text, font=("-weight bold", 16))
    title_label.pack(pady=10)

    tree_frame = ttk.Frame(parent_frame)
    tree_frame.pack(fill="both", expand=True)

    scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
    scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
    
    tree = ttk.Treeview(tree_frame, 
                        yscrollcommand=scroll_y.set, 
                        xscrollcommand=scroll_x.set,
                        height=15)
    
    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # This part is dynamic, so it already includes 'Roll No.'
    all_cols = list(df.columns)
    tree["columns"] = all_cols
    tree["show"] = "headings"

    for col in all_cols:
        tree.heading(col, text=col)
        
        # Added a specific rule for the new 'Roll No.' column
        if col == "Name":
            tree.column(col, width=150, anchor="w")
        elif col == "Roll No.":
            tree.column(col, width=110, anchor="w")
        elif col in ['Present', 'Absent', 'Total', 'Percent']:
            tree.column(col, width=60, anchor="center") # Summary cols
        else:
            tree.column(col, width=80, anchor="center") # Date cols

    # This is also dynamic and works perfectly
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    def export_to_csv():
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                # --- THIS LINE IS NOW FIXED ---
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Report As...",
                initialfile=f"{batch_name}_report.csv"
            )
            if filename:
                df.to_csv(filename, index=False)
                messagebox.showinfo("Success", f"Report saved to {filename}", parent=parent_frame)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}", parent=parent_frame)

    export_button = ttk.Button(parent_frame, text="Export CSV", command=export_to_csv)
    export_button.pack(pady=10)
