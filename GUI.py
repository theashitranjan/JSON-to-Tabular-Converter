import json
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import ttk

ctk.set_appearance_mode("System")  # Light, Dark, or System
ctk.set_default_color_theme("blue")

def load_json():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not file_path:
        return

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        df = pd.json_normalize(data, sep='_')
        show_table(df)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load or process file:\n{e}")

def show_table(df):
    for widget in table_frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(table_frame, columns=list(df.columns), show='headings')
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor='center')

    for _, row in df.iterrows():
        tree.insert('', 'end', values=list(row))

    def save_to_csv():
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path:
            df.to_csv(path, index=False)
            messagebox.showinfo("Success", f"CSV saved to:\n{path}")

    save_btn = ctk.CTkButton(table_frame, text="Save as CSV", command=save_to_csv, fg_color="#4CAF50", hover_color="#45A049")
    save_btn.pack(pady=10)

# GUI setup
root = ctk.CTk()
root.title("JSON to Tabular Converter")
root.geometry("900x600")

main_frame = ctk.CTkFrame(root)
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

load_btn = ctk.CTkButton(main_frame, text="Load JSON File", command=load_json, font=ctk.CTkFont(size=16))
load_btn.pack(pady=15)

table_frame = ctk.CTkFrame(main_frame)
table_frame.pack(expand=True, fill='both')

root.mainloop()
