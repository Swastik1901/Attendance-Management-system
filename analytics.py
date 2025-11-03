import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import data_manager

# Requires 'pip install matplotlib'
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_analytics_window(parent, batch_name):
    """
    Shows the analytics CHARTS window.
    """
    df, msg = data_manager.get_report_data(batch_name)
    
    if df is None:
        messagebox.showinfo("Analytics", msg, parent=parent)
        return

    win = tk.Toplevel(parent)
    win.title(f"Analytics Charts for {batch_name}")
    win.geometry("800x600") # Made window a bit wider for clearer labels

    try:
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        # --- FIX 1: Clean data for PLOTTING (Y-axis) ---
        # (This is still good practice, so we'll keep it)
        df['Present'] = pd.to_numeric(df['Present'], errors='coerce').fillna(0)
        df['Absent'] = pd.to_numeric(df['Absent'], errors='coerce').fillna(0)
        
        # --- FIX 2: Correct the 'add' error for LABELS (X-axis) ---
        # Convert 'Roll No.' to string BEFORE adding it to 'Name'
        df['Student'] = df['Roll No.'].astype(str) + " - " + df['Name']
        # --- END OF FIXES ---

        df.plot(
            kind='bar', 
            x='Student',  # Use the new 'Student' column
            y=['Present', 'Absent'], 
            ax=ax, 
            title='Overall Attendance Summary'
        )
        # This makes labels readable if there are many students
        fig.tight_layout() 
        
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=10)

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