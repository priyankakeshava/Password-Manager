import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DPS@2023",  
        database="passwords"
    )
    cursor = db.cursor()
except mysql.connector.Error as e:
    print(f"Database connection error: {e}")
    exit()

# Function to refresh the table
def refresh_table():
    for row in table.get_children():
        table.delete(row)
    cursor.execute("SELECT id, username FROM passwords")
    rows = cursor.fetchall()
    for i, row in enumerate(rows):
        tag = 'oddrow' if i % 2 == 0 else 'evenrow'
        table.insert("", "end", values=(row[0], row[1]), tags=(tag,))

# Function to clear the output frame and restore default UI
def reset_output_frame():
    for widget in output_frame.winfo_children():
        widget.destroy()
    display_buttons()

# Functionality to add a password
def add_password():
    reset_output_frame()
    tk.Label(output_frame, text="Add New Password", font=("Arial", 14, "bold"), bg="#E1FFC2", fg="#2E7D32").pack(pady=5)
    tk.Label(output_frame, text="Username:", bg="#E1FFC2").pack(pady=2)
    username_entry = tk.Entry(output_frame)
    username_entry.pack(pady=2)
    tk.Label(output_frame, text="Password:", bg="#E1FFC2").pack(pady=2)
    password_entry = tk.Entry(output_frame, show="*")
    password_entry.pack(pady=2)

    def toggle_password_visibility():
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
        else:
            password_entry.config(show='*')

    show_password_var = tk.BooleanVar()
    tk.Checkbutton(output_frame, text="Show Password", variable=show_password_var, bg="#E1FFC2", command=toggle_password_visibility).pack(pady=2)

    def save_password():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            try:
                cursor.execute("INSERT INTO passwords (username, password) VALUES (%s, %s)", (username, password))
                db.commit()
                refresh_table()
                tk.Label(output_frame, text="Password added successfully!", fg="green", bg="#E1FFC2").pack(pady=5)
            except Exception as e:
                tk.Label(output_frame, text=f"Error: {e}", fg="red", bg="#E1FFC2").pack(pady=5)
        else:
            tk.Label(output_frame, text="Please fill out all fields.", fg="red", bg="#E1FFC2").pack(pady=5)
        output_frame.after(2000, reset_output_frame)

    tk.Button(output_frame, text="Save", command=save_password, bg="#4CAF50", fg="white").pack(pady=5)

# Functionality to view password
def view_password():
    reset_output_frame()
    selected_item = table.selection()
    if selected_item:
        item = table.item(selected_item[0])
        id_value = item['values'][0]
        cursor.execute("SELECT password FROM passwords WHERE id = %s", (id_value,))
        result = cursor.fetchone()
        if result:
            tk.Label(output_frame, text=f"ID: {id_value}", font=("Arial", 12, "bold"), bg="#D9F1FF", fg="#1565C0").pack(pady=2)
            tk.Label(output_frame, text=f"Password: {result[0]}", font=("Arial", 12), bg="#D9F1FF").pack(pady=2)
        else:
            tk.Label(output_frame, text="Password not found.", fg="red", bg="#D9F1FF").pack(pady=2)
        output_frame.after(2000, reset_output_frame)
    else:
        tk.Label(output_frame, text="No row selected.", fg="red", bg="#D9F1FF").pack(pady=2)
        output_frame.after(2000, reset_output_frame)

# Functionality to update password
def update_password():
    reset_output_frame()
    selected_item = table.selection()
    if selected_item:
        item = table.item(selected_item[0])
        id_value = item['values'][0]
        tk.Label(output_frame, text=f"Update Password for ID: {id_value}", font=("Arial", 14, "bold"), bg="#FFE5B4", fg="#E65100").pack(pady=5)
        new_password_entry = tk.Entry(output_frame, show="*")
        new_password_entry.pack(pady=5)

        def toggle_password_visibility():
            if new_password_entry.cget('show') == '*':
                new_password_entry.config(show='')
            else:
                new_password_entry.config(show='*')

        show_password_var = tk.BooleanVar()
        tk.Checkbutton(output_frame, text="Show Password", variable=show_password_var, bg="#FFE5B4", command=toggle_password_visibility).pack(pady=2)

        def save_update():
            new_password = new_password_entry.get()
            if new_password:
                cursor.execute("UPDATE passwords SET password = %s WHERE id = %s", (new_password, id_value))
                db.commit()
                refresh_table()
                tk.Label(output_frame, text="Password updated successfully!", fg="green", bg="#FFE5B4").pack(pady=5)
            else:
                tk.Label(output_frame, text="Please enter a new password.", fg="red", bg="#FFE5B4").pack(pady=5)
            output_frame.after(2000, reset_output_frame)

        tk.Button(output_frame, text="Save", command=save_update, bg="#FF9800", fg="white").pack(pady=5)
    else:
        tk.Label(output_frame, text="No row selected.", fg="red", bg="#FFE5B4").pack(pady=5)
        output_frame.after(2000, reset_output_frame)

# Functionality to delete password
def delete_password():
    reset_output_frame()
    selected_item = table.selection()
    if selected_item:
        confirm=messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected password(s)?")
        if confirm:
            for selected_items in selected_item:
                item = table.item(selected_items)
                id_value = item['values'][0]
                cursor.execute("DELETE FROM passwords WHERE id = %s", (id_value,))
        db.commit()
        refresh_table()
        tk.Label(output_frame, text="Password deleted successfully!", fg="green", bg="#FFCDD2").pack(pady=5)
        output_frame.after(2000, reset_output_frame)
    else:
        tk.Label(output_frame, text="No row selected.", fg="red", bg="#FFCDD2").pack(pady=5)
        output_frame.after(2000, reset_output_frame)

# GUI Setup
root = tk.Tk()
root.title("Password Manager")
root.geometry("1000x700")

# Title
tk.Label(root, text="Password Manager", font=("Arial", 22, "bold"), bg="#FFB74D", fg="#000").pack(fill=tk.X)

# Table
columns = ("ID", "Username")
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12,selectmode="extended")

table.heading("ID", text="ID", anchor="center")
table.heading("Username", text="Username", anchor="center")

table.column("ID", anchor="center", width=100)
table.column("Username", anchor="center", width=200)

table.pack(side="left", fill=tk.BOTH, expand=True)

# Scrollbar for table
scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side="right", fill="y")
table.configure(yscrollcommand=scrollbar.set)

# Style
style = ttk.Style()
style.configure("Treeview", rowheight=30, font=("Arial", 12))
style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
table.tag_configure('oddrow', background="#f9f9f9")
table.tag_configure('evenrow', background="#e0f7fa")

# Output Frame
output_frame = tk.Frame(root, bg="#f7f7f7", bd=2, relief="ridge")
output_frame.pack(fill=tk.X, pady=10, padx=10)

# Functionality to add buttons back in the output frame
def display_buttons():
    tk.Button(output_frame, text="Add Password", command=add_password, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=15).pack(side="left", padx=10)
    tk.Button(output_frame, text="View Password", command=view_password, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=15).pack(side="left", padx=10)
    tk.Button(output_frame, text="Update Password", command=update_password, bg="#FF9800", fg="white", font=("Arial", 12, "bold"), width=15).pack(side="left", padx=10)
    tk.Button(output_frame, text="Delete Password", command=delete_password, bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=15).pack(side="left", padx=10)

display_buttons()
refresh_table()

root.mainloop()
