import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import csv
import os
import re

valid_courses = {
        "BSCS": "Bachelor of Science in Computer Science",
        "BSCA": "Bachelor of Science in Computer Applications",
        "BSIT": "Bachelor of Science in Information Technology",
        "BSIS": "Bachelor of Science in Information Systems",
        "BSPSYCH": "Bachelor of Science in Psychology",
        "BAPSYCH": "Bachelor of Arts in Psychology",
        "BAELS": "Bachelor of Arts in English Language Studies",
        "BALCS": "Bachelor of Arts in Language and Culture Studies",
        "BSSOCIO": "Bachelor of Arts in Sociology",
        "BAHIS": "Bachelor of Arts in History",
        "BAFIL": "Batsilyer ng Sining sa Filipino",
        "BAPAN": "Batsilyer ng Sining sa Panitikan",
        "BAPOLSCI": "Bachelor in Arts in Political Science",
        "BSCE": "Bachelor of Science in Civil Engineering",
        "BSCerE": "Bachelor of Science in Ceramic Engineering",
        "BSCoE": "Bachelor of Science in Computer Engineering",
        "BSECE": "Bachelor of Science in Electronics & Communications Engineering",
        "BSEE": "Bachelor of Science in Electrical Engineering",
        "BSMiningE": "Bachelor of Science in Mining Engineering",
        "BSEnET": "Bachelor of Science in Environmental Engineering Technology",
        "BSME": "Bachelor of Science in Mechanical Engineering",
        "BSMetE": "Bachelor of Science in Metallurgical Engineering",
        "BSN": "Bachelor of Science in Nursing"
    }
def on_button_submit():
    # Gets the user inputs
    name = entry_name.get()
    id_num = entry_idnum.get()
    yr_lvl = entry_yrlvl.get()
    gender = entry_gender.get()
    course_code = entry_courseCode.get()

    # Checks if user filled the entry fields
    if not (name and id_num and yr_lvl and gender and course_code):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if not validate_id_number(id_num):
        messagebox.showerror("Error", "Invalid ID number format. Please enter a valid ID number in the format 'YYYY-NNNN'.")
        return

    # Check if the course code is valid
    if course_code not in valid_courses:
        messagebox.showerror("Error", "Invalid course code. Please enter a valid course code.")
        return

    # Get the course title corresponding to the course code
    course_title = valid_courses[course_code]

    # Append the user input to the student.csv file
    with open("student.csv", mode="a", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if csvfile.tell() == 0:  # Check if the file is empty
            csv_writer.writerow(["Name", "ID_Number", "Year_Level", "Gender", "Course_Code", "Course_Title"])
        csv_writer.writerow([name, id_num, yr_lvl, gender, course_code, course_title])

    # Append user input to the course.csv file
    with open("course.csv", mode="a", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if not os.path.exists("course.csv"):
            csv_writer.writerow(["Course", "Course_Title"])
        csv_writer.writerow([course_code, course_title])

    # To show the results
    df = pd.read_csv("student.csv")

    # Clear existing items in the Treeview
    for item in treeview.get_children():
        treeview.delete(item)

    # Insert data into the Treeview with center alignment
    for index, row in df.iterrows():
        treeview.insert("", "end", values=tuple(row), tags="centered")

    # Set a tag for centered alignment
    treeview.tag_configure("centered", anchor="center")

    # Clear entry widgets
    entry_name.delete(0, tk.END)
    entry_idnum.delete(0, tk.END)
    entry_yrlvl.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_courseCode.delete(0, tk.END)

def validate_id_number(id_num):
    pattern = r'^\d{4}-\d{4}$'  # Regex pattern for YEAR-number format
    return bool(re.match(pattern, id_num))

def search_student():
    query = entry_search.get().strip().lower()  # Get the search query and convert it to lowercase

    if not query:
        return  # If the search query is empty, do nothing

    # Iterate through the data in the CSV file and search for the query
    for row_id in treeview.get_children():
        row = treeview.item(row_id)['values']
        if query in row[0].lower() or query in row[1].lower():  # Check if the query matches name or ID number
            treeview.selection_set(row_id)  # Select the row in the treeview
            treeview.focus(row_id)  # Focus on the selected row
            treeview.see(row_id)  # Scroll to make the selected row visible
            return  # Stop searching after the first match


# Create the main window
app = tk.Tk()
app.title("Simple Student Information System")
app.geometry("1160x450")

style = ttk.Style(app)
app.tk.call("source", "forest-light.tcl")
app.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(app)
frame.grid(sticky="nsew")
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(0, weight=1)

widgets_frame = ttk.LabelFrame(frame, text="Register here!")
widgets_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

entry_name = tk.Entry(widgets_frame)
entry_name.insert(0, "Name")
entry_name.bind("<FocusIn>", lambda e: entry_name.delete('0', 'end'))
entry_name.grid(row=0, column=0, sticky="ew", padx=5, pady=10)

entry_idnum = tk.Entry(widgets_frame)
entry_idnum.insert(0, "ID Number")
entry_idnum.bind("<FocusIn>", lambda e: entry_idnum.delete('0', 'end'))
entry_idnum.grid(row=1, column=0, sticky="ew", padx=5, pady=10)

level= ["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "6th Year"]
entry_yrlvl = ttk.Combobox(widgets_frame, values=level)
entry_yrlvl.insert("0", "Year Level")
entry_yrlvl.grid(row=2, column=0, sticky="ew", padx=5, pady=10)

gender_list = ["Male", "Female", "Other"]
entry_gender = ttk.Combobox(widgets_frame, values=gender_list)
entry_gender.insert("0", "Gender")
entry_gender.grid(row=3, column=0, sticky="ew", padx=5, pady=10)

courseCode_list = ["BSCS", "BSCA", "BSIT", "BSIS", "BSPSYCH",
                   "BAPSYCH",
                   "BAELS",
                   "BALCS",
                   "BSSOCIO",
                   "BAHIS",
                   "BAFIL",
                   "BAPAN",
                   "BAPOLSCI",
                   "BSCE",
                   "BSCoE",
                   "BSECE",
                   "BSEE",
                   "BSMiningE",
                   "BSEnET",
                   "BSME",
                   "BSMetE",
                   "BSN"]
entry_courseCode = ttk.Combobox(widgets_frame, values=courseCode_list)
entry_courseCode.insert("0", "Course")
entry_courseCode.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

button_submit = tk.Button(widgets_frame, text="SUBMIT", command=on_button_submit)
button_submit.grid(row=6, column=0, padx=5, pady=5)

seperator = ttk.Separator(widgets_frame)
seperator.grid(row=7, column=0, sticky="ew", padx=(20, 10), pady=5)

treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10, sticky="nsew")
treeFrame.columnconfigure(0, weight=1)
treeFrame.rowconfigure(0, weight=1)

def on_button_edit():
    # Get the selected item in the treeview
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to edit.")
        return

    # Get the values of the selected row
    values = treeview.item(selected_item)['values']

    # Populate the registration segment fields with the selected values
    entry_name.delete(0, tk.END)
    entry_name.insert(0, values[0])

    entry_idnum.delete(0, tk.END)
    entry_idnum.insert(0, values[1])

    entry_yrlvl.delete(0, tk.END)
    entry_yrlvl.insert(0, values[2])

    entry_gender.delete(0, tk.END)
    entry_gender.insert(0, values[3])

    entry_courseCode.delete(0, tk.END)
    entry_courseCode.insert(0, values[4])

    #This removes the submit button to be replaced by the save button
    button_submit.grid_remove()

    button_save.grid(row=6, column=0, padx=5, pady=5)


def on_button_save():
    # Get the selected item in the treeview
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to save.")
        return

    # Get the values of the selected row
    values = [entry_name.get(), entry_idnum.get(), entry_yrlvl.get(), entry_gender.get(), entry_courseCode.get()]

    # Check if the course code is valid
    if values[4] not in valid_courses:
        messagebox.showerror("Error", "Invalid course code. Please enter a valid course code.")
        return

    # Get the course title corresponding to the updated course code
    course_title = valid_courses[values[4]]

    # Get the index of the selected row
    selected_row_index = treeview.index(selected_item)

    # Update the values in the CSV file
    with open("student.csv", mode="r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        if len(rows) > selected_row_index + 1:  # Check if the selected row index is within bounds
            rows[selected_row_index + 1] = values[:4] + [values[4], course_title]  # Update the values in the corresponding row
        else:
            messagebox.showerror("Error", "Selected row index is out of bounds.")
            return

    with open("student.csv", mode="w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

    # Update the Treeview with the edited values
    treeview.item(selected_item, values=values[:4] + [values[4], course_title])

    # Clear entry widgets
    entry_name.delete(0, tk.END)
    entry_idnum.delete(0, tk.END)
    entry_yrlvl.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_courseCode.delete(0, tk.END)

    button_save.grid_remove()
    button_submit.grid(row=6, column=0, padx=5, pady=5)


def on_button_del():
    # Get the selected item in the treeview
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to delete.")
        return

    # Ask for confirmation before deleting
    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this row?")

    if confirmation:
        # Get the index of the selected row
        selected_row_index = treeview.index(selected_item)

        # Delete the selected row from the CSV file
        with open("student.csv", mode="r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if len(rows) > selected_row_index + 1:  # Check if the selected row index is within bounds
                del rows[selected_row_index + 1]  # Delete the corresponding row
            else:
                messagebox.showerror("Error", "Selected row index is out of bounds.")
            return

        # Write the updated rows back to the CSV file
        with open("student.csv", mode="w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        # Delete the selected row from the Treeview
        treeview.delete(selected_item)

def on_button_load():
    if os.path.exists("student.csv"):
        df = pd.read_csv("student.csv")

        # Clear existing items in the Treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Insert data into the Treeview with center alignment
        for index, row in df.iterrows():
            treeview.insert("", "end", values=tuple(row), tags="centered")

        # Set a tag for centered alignment
        treeview.tag_configure("centered", anchor="center")


# Create the frame to contain the buttons
button_frame1 = ttk.Frame(treeFrame)
button_frame1.pack(side="bottom", pady=10, anchor="e")

# Create the "EDIT" button
button_edit = tk.Button(button_frame1, text="EDIT", command=on_button_edit)
button_edit.pack(side="left", padx=5)

# Create the "SAVE" button
button_del = tk.Button(button_frame1, text="DELETE", command=on_button_del)
button_del.pack(side="left", padx=5)

button_load = tk.Button(button_frame1, text="LOAD", command=on_button_load)
button_load.pack(side="right", padx=5)

search_frame = ttk.Frame(treeFrame)
search_frame.pack(side="top", pady=10, anchor="e")

# Create the search entry
entry_search = tk.Entry(search_frame)
entry_search.insert(0,"Search Name or ID")
entry_search.bind("<FocusIn>", lambda e: entry_search.delete('0', 'end'))
entry_search.pack(side="left", padx=5)

# Create the "SEARCH" button
button_search = tk.Button(search_frame, text="SEARCH", command=search_student)
button_search.pack(side="left", padx=5)

button_save = tk.Button(widgets_frame, text="SAVE", command=on_button_save)

treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("Name", "ID_Number", "Year_Level", "Gender", "Course_Code", "Course Title")
treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)

# Add headings to the Treeview
for col in cols:
    treeview.heading(col, text=col)

# Set column widths
treeview.column("Name", width=200, anchor="center")
treeview.column("ID_Number", width=100, anchor="center")
treeview.column("Year_Level", width=80, anchor="center")
treeview.column("Gender", width=80, anchor="center")
treeview.column("Course_Code", width=100, anchor="center")
treeview.column("Course Title", width=300, anchor="center")

treeview.pack(expand=True, fill="both")
treeScroll.config(command=treeview.yview)

# Run the main loop
app.mainloop()
