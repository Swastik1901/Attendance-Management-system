import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import data_manager

# Requires 'pip install matplotlib'
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def show_analytics_window(parent, batch_name):
    """
    Spacious, easy-to-read grouped bar chart for attendance (Present vs Absent).
    - Wider figure that adapts to number of students
    - Reduced bar width and extra margins for breathing room
    - Legend placed above the plot to keep the plotting area clean
    """
    import numpy as np
    from matplotlib import ticker

    df, msg = data_manager.get_report_data(batch_name)
    if df is None:
        messagebox.showinfo("Analytics", msg, parent=parent)
        return

    # Create window
    win = tk.Toplevel(parent)
    win.title(f"Analytics Charts for {batch_name}")
    # Make window larger to display the roomy chart
    win.geometry("1200x850")

    try:
        # Ensure numeric columns
        df['Present'] = pd.to_numeric(df['Present'], errors='coerce').fillna(0).astype(int)
        df['Absent']  = pd.to_numeric(df['Absent'],  errors='coerce').fillna(0).astype(int)

        # Create combined Student label
        df['Roll No.'] = df.get('Roll No.', df.index).astype(str)
        df['Student'] = df['Roll No.'].astype(str) + " - " + df['Name'].astype(str)

        n = len(df)
        # Figure size: widen when many students
        fig_w = max(12, n * 0.9)   # base width 12, add width per student
        fig_h = 9                   # taller for more vertical space
        fig = Figure(figsize=(fig_w, fig_h), dpi=140)
        ax = fig.add_subplot(111)

        indices = np.arange(n)
        bar_width = 0.28  # slightly narrower so bars don't touch

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
        label_fontsize = 9 if n <= 10 else 7   # smaller when many students
        rotation = 30 if n <= 12 else 60
        ax.set_xticklabels(df['Student'], rotation=rotation, ha='right', fontsize=label_fontsize)

        # Y ticks readability
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.tick_params(axis='y', labelsize=12)
        ax.tick_params(axis='x', labelsize=label_fontsize)

        # Provide extra space at left/right of bars so they don't touch axis edges
        ax.set_xlim(-0.6, n - 0.4)
        ax.margins(x=0.02)

        # Gridlines
        ax.grid(axis='y', linestyle='--', alpha=0.45)

        # Put legend above the chart (keeps plotting area spacious)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=2, fontsize=12, frameon=False)

        # Increase the margins around the plot area so labels & legend have room
        fig.subplots_adjust(left=0.07, right=0.97, top=0.86, bottom=0.24)

        # Embed in Tk window
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=14, pady=14)

    except Exception as e:
        win.destroy()
        messagebox.showerror("Error", f"Could not generate chart: {e}", parent=parent)




def show_detailed_report_window(parent, batch_name):
    """
    Shows the NEW detailed report window (from your screenshot).
    """
    df, msg = data_manager.get_report_data(batch_name)
    
    if df is None:
        messagebox.showinfo("Attendance Report", msg, parent=parent)
        return

    win = tk.Toplevel(parent)
    win.title(f"Attendance Report (Detailed) - {batch_name}")
    win.geometry("900x500")

    main_frame = ttk.Frame(win)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Try to find the max total days, default to 'N/A' if it fails
    try:
        total_days = df['Total'].max()
        title_text = f"Attendance Report ({total_days} days)"
    except Exception:
        title_text = "Attendance Report"

    title_label = ttk.Label(main_frame, text=title_text, font=("-weight bold", 16))
    title_label.pack(pady=10)

    tree_frame = ttk.Frame(main_frame)
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
                messagebox.showinfo("Success", f"Report saved to {filename}", parent=win)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}", parent=win)

    export_button = ttk.Button(main_frame, text="Export CSV", command=export_to_csv)
    export_button.pack(pady=10)