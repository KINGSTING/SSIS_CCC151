import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import csv
import os
import re


def load_courses(filename):
    courses = {}
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:
                code, name = row
                courses[code.strip()] = name.strip()
    return courses

def check_course(course_code, courses):
    return course_code.upper() in courses

def update_student_status():
    # Read student data from CSV
    df = pd.read_csv("student.csv")
    courses = load_courses('course.csv')
    statuses = []

    # Update statuses for each student
    for index, row in df.iterrows():
        course_code = row['Course_Code']
        if course_code in courses:
            statuses.append("Enrolled")
        else:
            # If course is not found, keep the course title and change status to "Unenrolled"
            statuses.append("Unenrolled")

    # Update status column in DataFrame
    df['Status'] = statuses

    # Write updated DataFrame back to CSV
    df.to_csv("student.csv", index=False)


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
        messagebox.showerror("Error",
                             "Invalid ID number format. Please enter a valid ID number in the format 'YYYY-NNNN'.")
        return

    existing_ids = load_student_ids('student.csv')
    if check_duplicate_id(id_num,existing_ids):
        messagebox.showerror("Error",
                             "Invalid ID number. Already existing ID number.")
        return

    # Get the course title
    courses = load_courses('course.csv')
    course_title = courses[course_code]

    # Check if the student is enrolled or not
    status = "Enrolled" if check_course(course_code, courses) else "Unenrolled"

    # Append the user input to the student.csv file
    with open("student.csv", mode="a", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if csvfile.tell() == 0:  # Check if the file is empty
            csv_writer.writerow(["Name", "ID_Number", "Year_Level", "Gender", "Course_Code", "Course_Title", "Status"])
        csv_writer.writerow([name, id_num, yr_lvl, gender, course_code, course_title, status])

    # Update student status
    update_student_status()

    # Refresh Treeview
    on_button_load()

    # Clear entry widgets
    entry_name.delete(0, tk.END)
    entry_idnum.delete(0, tk.END)
    entry_yrlvl.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_courseCode.delete(0, tk.END)

    # Make the guides appear
    entry_name.insert(0, "Name")
    entry_idnum.insert(0, "ID Number")
    entry_yrlvl.insert(0, "Year Level")
    entry_gender.insert(0, "Gender")
    entry_courseCode.insert(0, "Course Code")

def on_button_edit():
    # Get the selected item in the treeview
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to edit.")
        return

    id_num = entry_idnum.get()
    existing_ids = load_student_ids('student.csv')
    if check_duplicate_id(id_num, existing_ids):
        messagebox.showerror("Error",
                             "Invalid ID number. Already existing ID number.")
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

    # This removes the submit button to be replaced by the save button
    button_submit.grid_remove()

    button_save.grid(row=6, column=0, padx=5, pady=5)


def on_button_save():
    # Get the selected item in the treeview
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to save.")
        return


    # Get the values of the selected row
    name = entry_name.get()
    id_num = entry_idnum.get()
    yr_lvl = entry_yrlvl.get()
    gender = entry_gender.get()
    course_code = entry_courseCode.get()

    # Check if any field is empty
    if not (name and id_num and yr_lvl and gender and course_code):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Validate ID number format
    if not validate_id_number(id_num):
        messagebox.showerror("Error",
                             "Invalid ID number format. Please enter a valid ID number in the format 'YYYY-NNNN'.")
        return

    #Validate ID duplication
    existing_ids = load_student_ids('student.csv')
    if check_duplicate_id(id_num, existing_ids):
        messagebox.showerror("Error",
                             "Invalid ID number. Already existing ID number.")
        return


    # Get the index of the selected row
    selected_row_index = treeview.index(selected_item)

    # Update the values in the CSV file
    with open("student.csv", mode="r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        if len(rows) > selected_row_index + 1:  # Check if the selected row index is within bounds
            rows[selected_row_index + 1] = [name, id_num, yr_lvl, gender, course_code]  # Update the values in the corresponding row
        else:
            messagebox.showerror("Error", "Selected row index is out of bounds.")
            return

    with open("student.csv", mode="w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

    # Update the Treeview with the edited values
    treeview.item(selected_item, values=(name, id_num, yr_lvl, gender, course_code))

    # Update student status
    update_student_status()

    # Clear entry widgets
    entry_name.delete(0, tk.END)
    entry_idnum.delete(0, tk.END)
    entry_yrlvl.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_courseCode.delete(0, tk.END)

    button_save.grid_remove()
    button_submit.grid(row=6, column=0, padx=5, pady=5)

    update_student_status()
    on_button_load()


def on_button_del():
    # Get the selected item in the treeview
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a row to delete.")
        return

    # Ask for confirmation before deleting
    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this row?")

    if confirmation:
        # Get the unique identifier of the selected row (e.g., ID number)
        selected_row_id = treeview.item(selected_item)['values'][1]

        # Delete the selected row from the CSV file
        with open("student.csv", mode="r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = [row for row in reader if row[1] != selected_row_id]  # Exclude the selected row

        # Write the updated rows back to the CSV file
        with open("student.csv", mode="w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        # Delete the selected row from the Treeview
        treeview.delete(selected_item)

        # Update student status
        update_student_status()
        on_button_load()


def validate_id_number(id_num):
    pattern = r'^\d{4}-\d{4}$'  # Regex pattern for YEAR-number format
    return bool(re.match(pattern, id_num))

def load_student_ids(filename):
    student_ids = set()
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                student_ids.add(row[1])  # Assuming ID_Number is in the second column
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    except Exception as e:
        print(f"Error: {e}")
    return student_ids

def check_duplicate_id(id_num, student_ids):
    return id_num in student_ids

courses = {
        "BSCS": "Bachelor of Science in Computer Science",
        "BSCA": "Bachelor of Science in Computer Applications",
        "BSIT": "Bachelor of Science in Information Technology",
        "BSIS": "Bachelor of Science in Information Systems",
        "BSPSYCH": "Bachelor of Science in Psychology",
        "BAPSYCH": "Bachelor of Arts in Psychology",
        "BAELS": "Bachelor of Arts in English Language Studies",
        "BALCS": "Bachelor of Arts in Language and Culture Studies",
        "BASOCIO": "Bachelor of Arts in Sociology",
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
def get_course_title(course_code):
    courses = {}  # Initialize an empty dictionary to store course information

    # Read course information from the CSV file
    with open("course.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:  # Check if the row contains course code and title
                code, title = row
                courses[code.strip()] = title.strip()  # Add course code and title to the dictionary

    # Get the course title corresponding to the given course code
    return courses.get(course_code.upper(), "Unknown")


def on_button_load():
    if os.path.exists("student.csv"):
        df = pd.read_csv("student.csv")

        # Clear existing items in the Treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Insert data into the Treeview with center alignment
        for index, row in df.iterrows():
            # Fetch course title based on course code
            course_code = row['Course_Code']
            course_title = get_course_title(course_code)

            courses = load_courses('course.csv')
            # Check if the course code is in the courses dictionary
            if course_code in courses:
                status = "Enrolled"
            else:
                status = "Unenrolled"

            # Insert the row into the Treeview
            treeview.insert("", "end", values=(
                row["Name"], row["ID_Number"], row["Year_Level"], row["Gender"], row["Course_Code"], course_title,
                status), tags="centered")

        # Set a tag for centered alignment
        treeview.tag_configure("centered", anchor="center")


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

    entry_search.delete(0, tk.END)
    entry_search.insert(0, "Search Name or ID")


# Create the main window
app = tk.Tk()
app.title("Simple Student Information System")
app.geometry("1200x400")

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

level = ["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "6th Year"]
entry_yrlvl = ttk.Combobox(widgets_frame, values=level)
entry_yrlvl.insert("0", "Year Level")
entry_yrlvl.grid(row=2, column=0, sticky="ew", padx=5, pady=10)

gender_list = ["Male", "Female", "Other"]
entry_gender = ttk.Combobox(widgets_frame, values=gender_list)
entry_gender.insert("0", "Gender")
entry_gender.grid(row=3, column=0, sticky="ew", padx=5, pady=10)

def read_course_codes_from_csv(filename, course_code_list):
    if course_code_list is None:
        course_code_list = []

    try:
        with open(filename, mode="r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    course_info = row[0].split(",")  # Split the row by comma
                    if len(course_info) >= 1:
                        course_code = course_info[0].strip().upper()  # Get the course code
                        if course_code not in course_code_list:
                            course_code_list.append(course_code)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    except Exception as e:
        print(f"Error: {e}")

    return course_code_list

courseCode_list = ["BSCS", "BSCA", "BSIT", "BSIS", "BSPSYCH",
                   "BAPSYCH",
                   "BAELS",
                   "BALCS",
                   "BASOCIO",
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

courseCode_list = read_course_codes_from_csv("course.csv", courseCode_list)

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

# Create the frame to contain the buttons
button_frame1 = ttk.Frame(treeFrame)
button_frame1.pack(side="bottom", pady=10, anchor="e")

# Create the "EDIT" button
button_edit = tk.Button(button_frame1, text="EDIT", command=on_button_edit)
button_edit.pack(side="left", padx=5)

# Create the "DELETE" button
button_del = tk.Button(button_frame1, text="DELETE", command=on_button_del)
button_del.pack(side="left", padx=5)

button_load = tk.Button(button_frame1, text="LOAD", command=on_button_load)
button_load.pack(side="right", padx=5)


search_frame = ttk.Frame(treeFrame)
search_frame.pack(side="top", pady=10, anchor="e")

# Create the search entry
entry_search = tk.Entry(search_frame)
entry_search.insert(0, "Search Name or ID")
entry_search.bind("<FocusIn>", lambda e: entry_search.delete('0', 'end'))
entry_search.pack(side="left", padx=5)

# Create the "SEARCH" button
button_search = tk.Button(search_frame, text="SEARCH", command=search_student)
button_search.pack(side="left", padx=5)

button_save = tk.Button(widgets_frame, text="SAVE", command=on_button_save)

treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("Name", "ID_Number", "Year_Level", "Gender", "Course_Code", "Course_Title", "Status")
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
treeview.column("Course_Title", width=300, anchor="center")
treeview.column("Status", width=100, anchor="center")

treeview.pack(expand=True, fill="both")
treeScroll.config(command=treeview.yview)


def update_course_code_list():
    global courseCode_list
    courseCode_list = read_course_codes_from_csv("course.csv", courseCode_list)
    entry_courseCode['values'] = courseCode_list



# Define a global variable to keep track of the manager window
manager_window = None

def createManager(parent):
    global manager_window
    # Check if the manager window is already open
    if manager_window is not None and manager_window.winfo_exists():
        manager_window.lift()  # Bring the existing window to the front
        return

    # Create a new manager window if it doesn't exist
    manager_window = tk.Toplevel(parent)
    manager_window.title("Manage Courses")

    # Create a LabelFrame inside the Toplevel window
    course_frame = ttk.LabelFrame(manager_window, text="Manage Courses")
    course_frame.pack(padx=20, pady=10, fill="both", expand=True)

    entry_course_code = tk.Entry(course_frame)
    entry_course_code.insert(0, "Course Code")
    entry_course_code.bind("<FocusIn>", lambda e: entry_course_code.delete('0', 'end'))
    entry_course_code.grid(row=0, column=0, padx=5, pady=5)
    entry_course_title = tk.Entry(course_frame)
    entry_course_title.insert(0, "Course Title")
    entry_course_title.bind("<FocusIn>", lambda e: entry_course_title.delete('0', 'end'))
    entry_course_title.grid(row=0, column=1, padx=5, pady=5)

    course_listbox = tk.Listbox(course_frame, width=50, height=10)
    course_listbox.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

    def on_button_add_course():
        course_code = entry_course_code.get()
        course_title = entry_course_title.get()

        if not (course_code and course_title):
            messagebox.showerror("Error", "Please fill in both fields (Course Code and Course Title).")
            return
        if course_code == "Course Code":
            messagebox.showerror("Error", "Please enter a valid course code.")
            return
        if course_code == "Course Title":
            messagebox.showerror("Error", "Please enter a valid course code.")
            return

        if course_code not in courses:
            courses[course_code] = course_title
            print(f"Course '{course_code}: {course_title}' added successfully.")
        else:
            print(f"Course '{course_code}: {courses[course_code]}' already exists.")

        with open("course.csv", mode="a", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([course_code.upper(), course_title])


        load_course_list(course_listbox)
        update_course_code_list()
        on_button_load()

        entry_course_code.delete(0, tk.END)
        entry_course_title.delete(0, tk.END)

        entry_course_code.insert(0, "Course Code")
        entry_course_title.insert(0, "Course Title")

    def on_button_delete_course():
        selected_course = course_listbox.curselection()
        if not selected_course:
            messagebox.showerror("Error", "Please select a course to delete.")
            return

        course_info = course_listbox.get(selected_course)
        course_code, course_title = course_info.split(": ", 1)

        confirmation = messagebox.askyesno("Confirmation",
                                           f"Are you sure you want to delete {course_code}: {course_title}?")
        if not confirmation:
            return

        with open("course.csv", mode="r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = [row for row in reader if not row or row[0].strip() != course_code]

        with open("course.csv", mode="w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        load_course_list(course_listbox)
        update_course_code_list()
        on_button_load()

    button_add_course = tk.Button(course_frame, text="Add Course", command=on_button_add_course)
    button_add_course.grid(row=0, column=2, padx=5, pady=5)
    button_delete_course = tk.Button(course_frame, text="Delete Course", command=on_button_delete_course)
    button_delete_course.grid(row=0, column=3, padx=5, pady=5)

    load_course_list(course_listbox)

def load_course_list(course_listbox):
    course_listbox.delete(0, tk.END)

    with open("course.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:
                course_listbox.insert(tk.END, f"{row[0]}: {row[1]}")

button_manage = tk.Button(button_frame1, text="MANAGE", command=lambda: createManager(app))
button_manage.pack(side="left", padx=5)


app.mainloop()
