import tkinter as tk
import csv

def on_button_add():
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
            csv_writer.writerow(["Name:", "ID_Number:", "Year_Level", "Gender"])
        csv_writer.writerow([name, id_num, yr_lvl, gender])

    # Appends to Course CSV File
    valid_courses = ["BSCS", "BSCA", "BSIT", "BSIS"]
    course_Title = ["Bachelor of Science in Computer Science",
                    "Bachelor of Science in Computer Applications",
                    "Bachelor of Science in Information Technology",
                    "Bachelor of Science in Information Systems"]
    # Checks if the user input is valid
    if courseCode in valid_courses:
        index = valid_courses.index(courseCode)
        course_Description = course_Title[index]

        # Append user input to a CSV file
        with open("course.csv", mode="a", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write header only if the file is empty
            if csvfile.tell() == 0:
                csv_writer.writerow(["Course:", "Course_Title:"])
            csv_writer.writerow([courseCode, course_Description])
    else:
        print("Invalid course. Please enter BSCS, BSCA, BSIT, or BSIS.")

    # Read course information from course.csv and append to student.csv
    with open("course.csv", mode="r") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            # Append course information to student.csv
            with open("student.csv", mode="a", newline='') as csvfile_student:
                csv_writer_student = csv.writer(csvfile_student)
                csv_writer_student.writerow(["", "", "", "", row[0], row[1]])

    # Clear entry widgets
    entry_name.delete(0, tk.END)
    entry_idnum.delete(0, tk.END)
    entry_yrlvl.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_courseCode.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Simple Student Information System")
root.geometry("800x400")
root.resizable(False, False)

label_name = tk.Label(root, text="Name:")
label_name.grid(row=1, column=0, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1, pady=5)

label_idnum = tk.Label(root, text="ID Number:")
label_idnum.grid(row=2, column=0, pady=5)
entry_idnum = tk.Entry(root)
entry_idnum.grid(row=2, column=1, pady=5)

label_yrlvl = tk.Label(root, text="Year Level:")
label_yrlvl.grid(row=3, column=0, pady=5)
entry_yrlvl = tk.Entry(root)
entry_yrlvl.grid(row=3, column=1, pady=5)

label_gender = tk.Label(root, text="Gender:")
label_gender.grid(row=4, column=0, pady=5)
entry_gender = tk.Entry(root)
entry_gender.grid(row=4, column=1, pady=5)

label_courseCode = tk.Label(root, text="Course Code:")
label_courseCode.grid(row=5, column=0, pady=5)
entry_courseCode = tk.Entry(root)
entry_courseCode.grid(row=5, column=1, pady=5)

button_add = tk.Button(root, text="Add", command=on_button_add)
button_add.grid(row=6, column=0, columnspan=2, pady=10)

# Run the main loop
root.mainloop()
