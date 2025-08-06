import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import subprocess
import os
import json

# ---------- CONFIG LOADER ----------
CONFIG_FILE = "config.json"

def get_mysql_bin_path():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                saved_path = config.get("mysql_bin_path", "").rstrip("\\")
                if os.path.exists(saved_path):
                    return saved_path
        except Exception as e:
            print(f"Error reading config: {e}")

    popup = tk.Toplevel()
    popup.title("MySQL Bin Path Setup")
    popup.geometry("600x180")
    popup.grab_set()

    tk.Label(popup, text="Please select the MySQL bin folder path (e.g., D:\\xampp\\mysql\\bin):", font=("Arial", 11)).pack(pady=(15, 5))
    path_var = tk.StringVar()
    path_label = tk.Label(popup, text="No path selected", fg="red", wraplength=550)
    path_label.pack(pady=5)

    def browse_path():
        selected = filedialog.askdirectory(title="Select MySQL bin folder")
        if selected:
            path_var.set(selected.rstrip("\\"))
            path_label.config(text=selected, fg="green")

    def on_continue():
        selected_path = path_var.get()
        if not selected_path:
            messagebox.showerror("Error", "Please select a folder before continuing.")
            return
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({"mysql_bin_path": selected_path}, f)
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save path: {e}")

    tk.Button(popup, text="Browse", command=browse_path, bg="lightblue").pack(pady=5)
    tk.Button(popup, text="Continue", command=on_continue, bg="green", fg="white").pack(pady=(10, 0))
    root.wait_window(popup)

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        return config.get("mysql_bin_path", "").rstrip("\\")

def get_database_list():
    try:
        result = subprocess.run(
            [f"{bin_path}\\mysql", "-u", "root", "-e", "SHOW DATABASES;"],
            capture_output=True, text=True, shell=True
        )
        lines = result.stdout.splitlines()
        return [
            db for db in lines[1:]
            if db not in ("information_schema", "mysql", "performance_schema", "sys")
        ]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch databases: {e}")
        return []

# ---------- GUI SETUP ----------
root = tk.Tk()
root.withdraw()
bin_path = get_mysql_bin_path()
root.deiconify()
root.title("SQL Management Application")

# ---------- VARIABLES ----------
db_name_input = tk.StringVar()
table_name_input = tk.StringVar()
selected_file = tk.StringVar()

# ---------- GUI ----------
tk.Label(root, text="Database Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
db_dropdown = ttk.Combobox(root, textvariable=db_name_input, width=37)
db_dropdown['values'] = get_database_list()
db_dropdown.grid(row=0, column=1, padx=10, pady=10)

create_db_button = tk.Button(root, text="Create DB", command=lambda: create_db(), bg="orange", fg="white")
create_db_button.grid(row=0, column=2, padx=10, pady=10)

drop_db_button = tk.Button(root, text="Drop DB", command=lambda: drop_db(), bg="red", fg="white")
drop_db_button.grid(row=0, column=3, padx=10, pady=10)

export_button = tk.Button(root, text="Export DB", command=lambda: export_table(), bg="blue", fg="white")
export_button.grid(row=0, column=4, padx=10, pady=10)

# tk.Label(root, text="Table Name:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
# tk.Entry(root, textvariable=table_name_input, width=40).grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Select SQL File:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
file_button = tk.Button(root, text="Browse", command=lambda: select_file(), bg="lightblue", fg="black")
file_button.grid(row=2, column=1, padx=10, pady=10)

file_path_label = tk.Label(root, text="", width=80, height=1, anchor="w")
file_path_label.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

start_import_button = tk.Button(root, text="Start Import", command=lambda: import_sql_command(), bg="green", fg="white")
start_import_button.grid(row=4, column=3, padx=10, pady=10)

tk.Label(root, text="Messages:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
result_text = tk.Text(root, height=10, width=80)
result_text.grid(row=7, column=0, columnspan=5, padx=10, pady=10)

# ---------- FUNCTIONS ----------
def import_sql_command():
    db_name = db_name_input.get()
    file_path = selected_file.get()

    if not db_name:
        messagebox.showerror("Error", "Database name is required.")
        return

    if not file_path:
        messagebox.showerror("Error", "SQL file must be selected.")
        return

    start_import_button.config(state=tk.DISABLED)
    result_text.insert(tk.END, "Import started...\n")
    result_text.update()

    try:
        command = f'"{bin_path}\\mysql" -u root {db_name} < "{file_path}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            result_text.insert(tk.END, f"Import successful into database '{db_name}':\n{stdout.decode()}\n")
        else:
            result_text.insert(tk.END, f"Error during import:\n{stderr.decode()}\n")

    except Exception as e:
        result_text.insert(tk.END, f"Unexpected error: {e}\n")

    start_import_button.config(state=tk.NORMAL)
    result_text.insert(tk.END, "Import completed.\n")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("SQL Files", "*.sql")])
    if file_path:
        selected_file.set(file_path)
        file_path_label.config(text=file_path)
    return file_path

def create_db():
    db_name = db_name_input.get()
    if not db_name:
        messagebox.showerror("Error", "Database name is required.")
        return

    try:
        command = f'"{bin_path}\\mysql" -u root -e "CREATE DATABASE IF NOT EXISTS {db_name};"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            result_text.insert(tk.END, f"Database '{db_name}' created successfully!\n")
            db_dropdown['values'] = get_database_list()
        else:
            result_text.insert(tk.END, f"Error during database creation:\n{stderr.decode()}\n")
    except Exception as e:
        result_text.insert(tk.END, f"Error: {e}\n")

def drop_db():
    db_name = db_name_input.get()
    if not db_name:
        messagebox.showerror("Error", "Database name is required.")
        return

    try:
        command = f'"{bin_path}\\mysql" -u root -e "DROP DATABASE IF EXISTS {db_name};"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            result_text.insert(tk.END, f"Database '{db_name}' dropped successfully!\n")
            db_dropdown['values'] = get_database_list()
        else:
            result_text.insert(tk.END, f"Error during database drop:\n{stderr.decode()}\n")
    except Exception as e:
        result_text.insert(tk.END, f"Error: {e}\n")

def export_table():
    db_name = db_name_input.get()
    table_name = table_name_input.get()

    if not db_name:
        messagebox.showerror("Error", "Database name is required.")
        return

    save_folder = filedialog.askdirectory(title="Select Folder to Save Export")
    if not save_folder:
        messagebox.showerror("Error", "You must select a folder to save the file.")
        return

    if table_name:
        save_path = f"{save_folder}\\{db_name}_{table_name}.sql"
        command = f'"{bin_path}\\mysqldump" -u root {db_name} {table_name} > "{save_path}"'
        success_message = f"Table '{table_name}' exported successfully to '{save_path}'!"
    else:
        save_path = f"{save_folder}\\{db_name}.sql"
        command = f'"{bin_path}\\mysqldump" -u root {db_name} > "{save_path}"'
        success_message = f"Database '{db_name}' exported successfully to '{save_path}'!"

    execute_command(command, success_message)

def execute_command(command, success_message):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            result_text.insert(tk.END, success_message + "\n")
        else:
            result_text.insert(tk.END, f"Error:\n{stderr.decode()}\n")
    except Exception as e:
        result_text.insert(tk.END, f"Unexpected error: {e}\n")

root.mainloop()
