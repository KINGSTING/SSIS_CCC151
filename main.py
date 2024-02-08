import tkinter as tk
import csv
from tkinter import ttk
import pandas as pd
from customtkinter import *


def on_button_submit():
    # Gets the User inputs
    name = entry_name.get()
    id_num = entry_idnum.get()
    yr_lvl = entry_yrlvl.get()
    gender = entry_gender.get()
    courseCode = entry_courseCode.get()

    # Appends to Student CSV File
    with open("student.csv", mode="a", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header only if the file is empty
        if csvfile.tell() == 0:
            csv_writer.writerow(["Name:", "ID_Number:", "Year_Level:", "Gender:", "Course_Code:"])
        csv_writer.writerow([name, id_num, yr_lvl, gender, courseCode])

    # Appends to Course CSV File
    valid_courses = {"BSCS": "Bachelor of Science in Computer Science",
                     "BSCA": "Bachelor of Science in Computer Applications",
                     "BSIT": "Bachelor of Science in Information Technology",
                     "BSIS": "Bachelor of Science in Information Systems"}

    # Checks if the user input is valid
    if courseCode in valid_courses:
        course_description = valid_courses[courseCode]

        # Append user input to a CSV file
        with open("course.csv", mode="a", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            if not os.path.exists("course.csv"):
                csv_writer.writerow(["Course", "Course_Title"])
            csv_writer.writerow([courseCode, course_description])
    else:
        print("Invalid course. Please enter BSCS, BSCA, BSIT, or BSIS.")

    # Clear entry widgets
    entry_name.delete(0, tk.END)
    entry_idnum.delete(0, tk.END)
    entry_yrlvl.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_courseCode.delete(0, tk.END)


def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")


# Create the main window
app = tk.Tk()
app.title("Simple Student Information System")
app.geometry("880x400")

style = ttk.Style(app)
app.tk.call("source", "forest-light.tcl")
app.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(app)
frame.grid(sticky="nsew")

widgets_frame = ttk.LabelFrame(frame, text="Register here!")
widgets_frame.grid(row=0, column=0, padx=20, pady=10)

entry_name = tk.Entry(widgets_frame)
entry_name.insert(0, "Enter Full Name Here")
entry_name.bind("<FocusIn>", lambda e: entry_name.delete('0', 'end'))
entry_name.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

entry_idnum = tk.Entry(widgets_frame)
entry_idnum.insert(0, "Enter ID Number Here")
entry_idnum.bind("<FocusIn>", lambda e: entry_idnum.delete('0', 'end'))
entry_idnum.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

entry_yrlvl = ttk.Spinbox(widgets_frame, from_=1, to=9)
entry_yrlvl.insert("0", "Enter Year Level Here")
entry_yrlvl.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

gender_list = ["Male", "Female", "Other"]
entry_gender = ttk.Combobox(widgets_frame, values=gender_list)
entry_gender.insert("0", "Enter Gender Here")
entry_gender.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

courseCode_list = ["BSCS", "BSCA", "BSIT", "BSIS"]
entry_courseCode = ttk.Combobox(widgets_frame, values=courseCode_list)
entry_courseCode.insert("0", "Enter Course Code Here")
entry_courseCode.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

button_submit = tk.Button(widgets_frame, text="SUBMIT", command=on_button_submit)
button_submit.grid(row=6, column=0, padx=5, pady=5)

seperator = ttk.Separator(widgets_frame)
seperator.grid(row=7, column=0, sticky="ew", padx=(20, 10), pady=5)

def populate_treeview():
    # Read your CSV file into a DataFrame
    df = pd.read_csv("student.csv")

    # Clear existing items in the Treeview
    for item in treeview.get_children():
        treeview.delete(item)

    # Insert data into the Treeview with center alignment
    for index, row in df.iterrows():
        treeview.insert("", "end", values=tuple(row), tags="centered")

    # Set a tag for centered alignment
    treeview.tag_configure("centered", anchor="center")


treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10, sticky="nsew")
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("Name", "ID_Number", "Year_Level", "Gender", "Course_Code")
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

treeview.pack(expand=True, fill="both")
treeScroll.config(command=treeview.yview)

# Add a button to populate the Treeview with data from the CSV file
button_populate_treeview = tk.Button(frame, text="Populate Treeview", command=populate_treeview)
button_populate_treeview.grid(row=1, column=1, pady=10)

# Run the main loop
app.mainloop()
