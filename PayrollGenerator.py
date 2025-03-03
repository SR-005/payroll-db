import customtkinter as ctk
from tkinter import StringVar, messagebox
import sqlite3
from datetime import datetime

# SQLite Database Configuration
DATABASE_NAME = 'payslips.db'

# Function to initialize the database (create table if not exists)
def init_db():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS payslips (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            emp_id TEXT,
                            department TEXT,
                            designation TEXT,
                            doj TEXT,
                            dob TEXT,
                            uan TEXT,
                            pf_no TEXT,
                            esi_no TEXT,
                            basic_salary REAL,
                            conveyance REAL,
                            special_allowance REAL,
                            pf_deduction REAL,
                            esi_deduction REAL,
                            pt_deduction REAL,
                            total_earnings REAL,
                            total_deductions REAL,
                            net_pay REAL,
                            created_at TEXT
                        )''')
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as err:
        messagebox.showerror("Database Error", f"Error initializing database: {err}")

# Function to generate the payslip
def generate_payslip():
    # Check if any field is empty
    fields = [
        (name_var, "Employee Name"),
        (emp_id_var, "Employee ID"),
        (department_var, "Department"),
        (designation_var, "Designation"),
        (doj_var, "Date of Joining"),
        (dob_var, "Date of Birth"),
        (uan_var, "UAN"),
        (pf_no_var, "PF No"),
        (esi_no_var, "ESI No"),
        (basic_var, "Basic Salary"),
        (conveyance_var, "Conveyance"),
        (special_var, "Special Allowance"),
        (pf_deduction_var, "PF Deduction"),
        (esi_deduction_var, "ESI Deduction"),
        (pt_deduction_var, "PT Deduction"),
    ]

    empty_fields = []
    for var, field_name in fields:
        if not var.get().strip():  # Check if the field is empty or contains only whitespace
            empty_fields.append(field_name)

    if empty_fields:
        # Show warning message if any field is empty
        messagebox.showwarning(
            "Empty Fields",
            f"The following fields are empty:\n{', '.join(empty_fields)}\nPlease fill all fields before generating the payslip.",
        )
        return  # Stop further execution

    # Calculate Totals
    total_earnings = sum(float(var.get()) for var in [basic_var, conveyance_var, special_var] if var.get())
    total_deductions = sum(float(var.get()) for var in [pf_deduction_var, esi_deduction_var, pt_deduction_var] if var.get())
    net_pay = total_earnings - total_deductions

    # Store the payslip in the database
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO payslips (
                            name, emp_id, department, designation, doj, dob, uan, pf_no, esi_no,
                            basic_salary, conveyance, special_allowance, pf_deduction, esi_deduction, pt_deduction,
                            total_earnings, total_deductions, net_pay, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (name_var.get(), emp_id_var.get(), department_var.get(), designation_var.get(), doj_var.get(), dob_var.get(), uan_var.get(), pf_no_var.get(), esi_no_var.get(),
                         float(basic_var.get()), float(conveyance_var.get()), float(special_var.get()), float(pf_deduction_var.get()), float(esi_deduction_var.get()), float(pt_deduction_var.get()),
                         total_earnings, total_deductions, net_pay, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Payslip generated and stored successfully!")
    except sqlite3.Error as err:
        messagebox.showerror("Database Error", f"Error storing payslip: {err}")

    # Display the payslip in a new window
    show_payslip(total_earnings, total_deductions, net_pay)

    # Clear the input fields for the next entry
    clear_fields()

# Function to display the payslip in a new window
def show_payslip(total_earnings, total_deductions, net_pay):
    payslip_window = ctk.CTkToplevel(app)
    payslip_window.title("Generated Payslip")
    payslip_window.geometry("600x500")

    # Payslip Header
    ctk.CTkLabel(payslip_window, text="ALBERTIAN INSTITUTE OF SCIENCE AND TECHNOLOGY", font=("Arial", 20, "bold")).pack(pady=10)
    ctk.CTkLabel(payslip_window, text="Kalamassery, Ernakulam", font=("Arial", 14)).pack()
    ctk.CTkLabel(payslip_window, text="Payslip for the Month", font=("Arial", 16, "bold")).pack(pady=10)

    # Employee Details Section
    details_frame = ctk.CTkFrame(payslip_window)
    details_frame.pack(fill="x", padx=20, pady=10)

    details = {
        "Employee Name": name_var.get(),
        "Employee ID": emp_id_var.get(),
        "Department": department_var.get(),
        "Designation": designation_var.get(),
        "Date of Joining": doj_var.get(),
        "Date of Birth": dob_var.get(),
        "UAN": uan_var.get(),
        "PF No": pf_no_var.get(),
        "ESI No": esi_no_var.get(),
    }

    for key, value in details.items():
        row = ctk.CTkFrame(details_frame)
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text=f"{key}:", font=("Arial", 12, "bold"), width=150, anchor="w").pack(side="left")
        ctk.CTkLabel(row, text=value, font=("Arial", 12)).pack(side="left")

    # Earnings and Deductions Section
    earnings_deductions_frame = ctk.CTkFrame(payslip_window)
    earnings_deductions_frame.pack(fill="x", padx=20, pady=10)

    # Earnings
    earnings_frame = ctk.CTkFrame(earnings_deductions_frame)
    earnings_frame.pack(side="left", fill="both", expand=True, padx=10)

    ctk.CTkLabel(earnings_frame, text="Earnings", font=("Arial", 14, "bold")).pack(pady=5)

    earnings = {
        "Basic Salary": basic_var.get(),
        "Conveyance": conveyance_var.get(),
        "Special Allowance": special_var.get(),
    }

    for key, value in earnings.items():
        row = ctk.CTkFrame(earnings_frame)
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text=key, font=("Arial", 12), width=150, anchor="w").pack(side="left")
        ctk.CTkLabel(row, text=value, font=("Arial", 12)).pack(side="right")

    # Deductions
    deductions_frame = ctk.CTkFrame(earnings_deductions_frame)
    deductions_frame.pack(side="right", fill="both", expand=True, padx=10)

    ctk.CTkLabel(deductions_frame, text="Deductions", font=("Arial", 14, "bold")).pack(pady=5)

    deductions = {
        "PF Deduction": pf_deduction_var.get(),
        "ESI Deduction": esi_deduction_var.get(),
        "PT Deduction": pt_deduction_var.get(),
    }

    for key, value in deductions.items():
        row = ctk.CTkFrame(deductions_frame)
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text=key, font=("Arial", 12), width=150, anchor="w").pack(side="left")
        ctk.CTkLabel(row, text=value, font=("Arial", 12)).pack(side="right")

    # Totals Section
    totals_frame = ctk.CTkFrame(payslip_window)
    totals_frame.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(totals_frame, text="Total Earnings", font=("Arial", 12, "bold")).pack(side="left", padx=10)
    ctk.CTkLabel(totals_frame, text=f"{total_earnings:.2f}", font=("Arial", 12)).pack(side="right", padx=10)

    ctk.CTkLabel(totals_frame, text="Total Deductions", font=("Arial", 12, "bold")).pack(side="left", padx=10)
    ctk.CTkLabel(totals_frame, text=f"{total_deductions:.2f}", font=("Arial", 12)).pack(side="right", padx=10)

    ctk.CTkLabel(totals_frame, text="Net Pay", font=("Arial", 14, "bold")).pack(side="left", padx=10)
    ctk.CTkLabel(totals_frame, text=f"{net_pay:.2f}", font=("Arial", 14, "bold")).pack(side="right", padx=10)

    # Close Button
    ctk.CTkButton(payslip_window, text="Close", command=payslip_window.destroy).pack(pady=20)

# Function to clear input fields
def clear_fields():
    name_var.set("")
    emp_id_var.set("")
    department_var.set("")
    designation_var.set("")
    doj_var.set("")
    dob_var.set("")
    uan_var.set("")
    pf_no_var.set("")
    esi_no_var.set("")
    basic_var.set("")
    conveyance_var.set("")
    special_var.set("")
    pf_deduction_var.set("")
    esi_deduction_var.set("")
    pt_deduction_var.set("")

# Function to delete a payslip by Employee ID
def delete_payslip():
    emp_id = emp_id_var.get().strip()
    if not emp_id:
        messagebox.showwarning("Input Error", "Please enter Employee ID to delete payslip.")
        return

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM payslips WHERE emp_id = ?", (emp_id,))
        conn.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", f"Payslip for Employee ID {emp_id} deleted successfully!")
        else:
            messagebox.showwarning("Not Found", f"No payslip found for Employee ID {emp_id}.")
        cursor.close()
        conn.close()
    except sqlite3.Error as err:
        messagebox.showerror("Database Error", f"Error deleting payslip: {err}")

# Main Application Window
app = ctk.CTk()
app.title("Employee Salary Input")
app.geometry("960x740")  # Set display size to 960x740

# Variables
name_var = StringVar()
emp_id_var = StringVar()
pf_no_var = StringVar()
esi_no_var = StringVar()
department_var = StringVar()
designation_var = StringVar()
doj_var = StringVar()
dob_var = StringVar()
uan_var = StringVar()

basic_var = StringVar()
conveyance_var = StringVar()
special_var = StringVar()
pf_deduction_var = StringVar()
esi_deduction_var = StringVar()
pt_deduction_var = StringVar()

# Input Fields in 3 Columns
input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Column 1: Employee Details
col1 = ctk.CTkFrame(input_frame)
col1.pack(side="left", fill="both", expand=True, padx=10)

ctk.CTkLabel(col1, text="Employee Details", font=("Arial", 16, "bold")).pack(pady=10)

fields_col1 = [
    ("Employee Name", name_var),
    ("Employee ID", emp_id_var),
    ("Department", department_var),
    ("Designation", designation_var),
    ("Date of Joining", doj_var),
    ("Date of Birth", dob_var),
    ("UAN", uan_var),
    ("PF No", pf_no_var),
    ("ESI No", esi_no_var),
]

for label, var in fields_col1:
    ctk.CTkLabel(col1, text=label).pack(anchor="w")
    ctk.CTkEntry(col1, textvariable=var).pack(fill="x", pady=5)

# Column 2: Earnings
col2 = ctk.CTkFrame(input_frame)
col2.pack(side="left", fill="both", expand=True, padx=10)

ctk.CTkLabel(col2, text="Earnings", font=("Arial", 16, "bold")).pack(pady=10)

fields_col2 = [
    ("Basic Salary", basic_var),
    ("Conveyance", conveyance_var),
    ("Special Allowance", special_var),
]

for label, var in fields_col2:
    ctk.CTkLabel(col2, text=label).pack(anchor="w")
    ctk.CTkEntry(col2, textvariable=var).pack(fill="x", pady=5)

# Column 3: Deductions
col3 = ctk.CTkFrame(input_frame)
col3.pack(side="left", fill="both", expand=True, padx=10)

ctk.CTkLabel(col3, text="Deductions", font=("Arial", 16, "bold")).pack(pady=10)

fields_col3 = [
    ("PF Deduction", pf_deduction_var),
    ("ESI Deduction", esi_deduction_var),
    ("PT Deduction", pt_deduction_var),
]

for label, var in fields_col3:
    ctk.CTkLabel(col3, text=label).pack(anchor="w")
    ctk.CTkEntry(col3, textvariable=var).pack(fill="x", pady=5)

# Buttons at the Bottom
button_frame = ctk.CTkFrame(app)
button_frame.pack(side="bottom", fill="x", padx=20, pady=10)

ctk.CTkButton(button_frame, text="Generate Payslip", command=generate_payslip).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="Delete Payslip", command=delete_payslip).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="Exit", command=app.quit).pack(side="right", padx=10)

# Initialize the database
init_db()

# Run the application
app.mainloop()