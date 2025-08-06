import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
from threading import Thread

def import_sql_command():
    """Handles the SQL import process."""
    db_name = db_name_input.get()  # Get the database name from the input field
    file_path = selected_file.get()  # Get the selected file path

    if not db_name:
        messagebox.showerror("Error", "Database name is required.")
        return
    
    if not file_path:
        messagebox.showerror("Error", "SQL file must be selected.")
        return
    
    # Disable the "Start Import" button during the import process
    start_import_button.config(state=tk.DISABLED)
    result_text.insert(tk.END, "Import started...\n")
    result_text.update()  # Update the text widget to display "Import started..."
    
    # Show loading message
    loading_label.config(text="Loading... Please wait.")
    loading_label.grid(row=5, column=0, columnspan=2)

    # Run the import process in a separate thread to avoid blocking the UI
    import_thread = Thread(target=run_import, args=(db_name, file_path))
    import_thread.start()

def run_import(db_name, file_path):
    """Run the MySQL import in a separate thread to avoid blocking the UI."""
    # Default values for MySQL credentials
    user = "root"
    password = ""  # Adjust this if necessary

    try:
        # Build the MySQL command using the user, password, and database dynamically
        command = (
            f"D:\\xampp\\mysql\\bin\\mysql -u {user} -p{password} "
            f"{db_name} < {file_path}"
        )

        # Run the command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Update the UI with the result
        if process.returncode == 0:
            result_text.insert(tk.END, f"Import successful into database '{db_name}':\n{stdout.decode()}\n")
        else:
            result_text.insert(tk.END, f"Error during import into database '{db_name}':\n{stderr.decode()}\n")
    except Exception as e:
        result_text.insert(tk.END, f"An unexpected error occurred: {e}\n")

    # Hide loading message and re-enable the import button
    loading_label.grid_forget()
    start_import_button.config(state=tk.NORMAL)
    result_text.insert(tk.END, "Import completed.\n")

def select_file():
    """Opens the file dialog and returns the file path."""
    file_path = filedialog.askopenfilename(filetypes=[("SQL Files", "*.sql")])
    if file_path:
        selected_file.set(file_path)
        file_path_label.config(text=file_path)  # Display the selected file path in the label
    return file_path

# GUI Setup
root = tk.Tk()
root.title("SQL Import Application")

# Components
tk.Label(root, text="Database Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
db_name_input = tk.StringVar()
tk.Entry(root, textvariable=db_name_input, width=40).grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Select SQL File:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
selected_file = tk.StringVar()
file_button = tk.Button(root, text="Browse", command=select_file, bg="lightblue", fg="black")
file_button.grid(row=1, column=1, padx=10, pady=10)

# File path label to display the chosen file
file_path_label = tk.Label(root, text="", width=80, height=1, anchor="w")  # Adjusted width for larger file paths
file_path_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Start Import button
start_import_button = tk.Button(root, text="Start Import", command=import_sql_command, bg="green", fg="white")
start_import_button.grid(row=3, column=0, columnspan=2, pady=20)

# Loading label (this will show a loading message while import is in progress)
loading_label = tk.Label(root, text="", fg="red")

# Messages section
tk.Label(root, text="Messages:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
result_text = tk.Text(root, height=10, width=60)
result_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Initialize file handler (if needed, can be expanded for validation)
# file_handler = FileHandler() # If you have a separate file handler, uncomment this

root.mainloop()