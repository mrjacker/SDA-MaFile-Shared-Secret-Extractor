import os
import json
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def select_input_folder():
    """Opens a dialog to select the folder containing the .mafiles."""
    folder_selected = filedialog.askdirectory(title="Select Folder with .mafiles")
    if folder_selected:
        input_folder_var.set(folder_selected)

def select_output_file():
    """Opens a dialog to choose where to save the output text file."""
    file_selected = filedialog.asksaveasfilename(
        title="Select Output File",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_selected:
        output_file_var.set(file_selected)

def process_files():
    """Processes all .mafiles in the selected directory and writes to the output file."""
    input_folder = input_folder_var.get()
    output_file = output_file_var.get()

    if not input_folder or not output_file:
        messagebox.showwarning("Missing Information", "Please select both an input folder and an output file destination.")
        return

    try:
        # Find all files ending with .mafile
        mafiles = [f for f in os.listdir(input_folder) if f.lower().endswith('.mafile')]
        
        if not mafiles:
            messagebox.showinfo("No Files Found", "No .mafile files were found in the selected directory.")
            return

        processed_count = 0

        with open(output_file, 'w', encoding='utf-8') as out_f:
            for filename in mafiles:
                file_path = os.path.join(input_folder, filename)
                base_name = os.path.splitext(filename)[0] # Extracts the name without the .mafile extension
                shared_secret = None
                
                try:
                    # Attempt to parse as standard JSON first
                    with open(file_path, 'r', encoding='utf-8') as in_f:
                        data = json.load(in_f)
                        shared_secret = data.get("shared_secret")
                except json.JSONDecodeError:
                    # Fallback: If the file is malformed JSON, use Regular Expressions to find the string
                    with open(file_path, 'r', encoding='utf-8') as in_f:
                        content = in_f.read()
                        match = re.search(r'"shared_secret"\s*:\s*"([^"]+)"', content)
                        if match:
                            shared_secret = match.group(1)
                
                # If a shared_secret was successfully found, write it to the file
                if shared_secret:
                    out_f.write(f"{base_name}:{shared_secret}\n")
                    processed_count += 1

        messagebox.showinfo("Success", f"Successfully extracted secrets from {processed_count} out of {len(mafiles)} files.\n\nResults saved to:\n{output_file}")
        
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")

# --- UI Setup ---
root = tk.Tk()
root.title("MAFile Secret Extractor")
root.geometry("500x250")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center') # Center the window

# Variables to store file paths
input_folder_var = tk.StringVar()
output_file_var = tk.StringVar()

# --- UI Layout ---
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

# Input Folder Section
tk.Label(frame, text="1. Select Folder containing .mafiles:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
input_frame = tk.Frame(frame)
input_frame.pack(fill=tk.X, pady=(0, 15))
tk.Entry(input_frame, textvariable=input_folder_var, state="readonly", width=45).pack(side=tk.LEFT, padx=(0, 10))
tk.Button(input_frame, text="Browse...", command=select_input_folder).pack(side=tk.LEFT)

# Output File Section
tk.Label(frame, text="2. Select Output Text File destination:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 5))
output_frame = tk.Frame(frame)
output_frame.pack(fill=tk.X, pady=(0, 20))
tk.Entry(output_frame, textvariable=output_file_var, state="readonly", width=45).pack(side=tk.LEFT, padx=(0, 10))
tk.Button(output_frame, text="Browse...", command=select_output_file).pack(side=tk.LEFT)

# Execute Button
execute_btn = tk.Button(frame, text="Extract Secrets", command=process_files, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), pady=5)
execute_btn.pack(fill=tk.X)

# Start the application
root.mainloop()