from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import numpy as np
import os
import time
import sqlite3
from algorithm import regressor, train_model


# Creates first screen
screen_loading = Tk()
screen_loading.resizable(False, False)
screen_loading.title("Grade Prediction System")
screen_loading.geometry("300x400")
screen_loading.iconbitmap("icon.ico")
screen_loading.configure(bg="#f0f0f0")


def login():
    screen_loading.withdraw()
    screen_login = Toplevel()
    screen_login.resizable(False, False)
    screen_login.title("")
    screen_login.geometry("300x400")
    screen_login.iconbitmap("icon.ico")

    def login_verify():
        # Assigns text in entry fields to _log variables
        username_log = (entry_log_username.get()).strip()
        password_log = (entry_log_password.get()).strip()

        # Clears text in entry fields
        entry_log_username.delete(0, END)
        entry_log_password.delete(0, END)

        # Checks current filedir to match username w/ filename then checks password
        file_list = os.listdir()
        if username_log in file_list:
            user_file = open(username_log, "r")
            verify = user_file.read().splitlines()

            if password_log in verify:
                screen_login.withdraw()
                database()
            else:
                Label(screen_login, text="Account not recognised!", fg="green", font=("calibri", 11)).pack()
        else:
            Label(screen_login, text="Account not recognised!", fg="green", font=("calibri", 11)).pack()

    # Creates login screen (labels, entries, buttons)
    Label(screen_login, text="Login", font=("Cascadia Code SemiBold", 25, "italic")).place(x=100, y=36)
    Label(screen_login, text="Username", font=("Abadi", 12)).place(x=40, y=146)
    entry_log_username = Entry(screen_login); entry_log_username.place(x=130, y=149)
    Label(screen_login, text="Password", font=("Abadi", 12)).place(x=40, y=216)
    entry_log_password = Entry(screen_login, show="*"); entry_log_password.place(x=130, y=219)
    Button(screen_login, text="Login", bg="#C1CDCD", font=("Abadi", 12, "bold"), relief="groove", command=login_verify).place(x=120, y=286)
    Button(screen_login, text="Not registered?", font=("Abadi", 8), relief="flat", command=register).place(x=110, y=356)


def register():
    def create_user():
        # Assigns text in entry fields to _reg variables
        username_reg = (entry_reg_username.get()).strip()
        password_reg = (entry_reg_password.get()).strip()

        # Clears text in entry fields
        entry_reg_username.delete(0, END)
        entry_reg_password.delete(0, END)

        # Creates a text file using username as filename to store user info
        user_file = open(username_reg, "w")
        user_file.write(username_reg + "\n" + password_reg)
        user_file.close()

        Label(screen_register, text="Registration Successful!", fg="green", font=("calibri", 11)).pack()

    # Creates a new toplevel screen
    screen_register = Toplevel()
    screen_register.resizable(False, False)
    screen_register.title("Register")
    screen_register.geometry("300x400")
    screen_register.iconbitmap("icon.ico")

    # Creates register screen (labels, entries, buttons)
    Label(screen_register, text="Register", font=("Cascadia Code SemiBold", 25, "italic")).place(x=75, y=36)
    Label(screen_register, text="Username", font=("Abadi", 12)).place(x=40, y=146)
    entry_reg_username = Entry(screen_register); entry_reg_username.place(x=130, y=149)
    Label(screen_register, text="Password", font=("Abadi", 12)).place(x=40, y=216)
    entry_reg_password = Entry(screen_register, show="*"); entry_reg_password.place(x=130, y=219)
    Button(screen_register, text="Register", bg="#C1CDCD", font=("Abadi", 12, "bold"), relief="groove", command=create_user).place(x=110, y=286)


def database():
    def query():
        # Connect to db
        conn = sqlite3.connect("student_grades.db")
        cursor = conn.cursor()

        # Query db
        cursor.execute("SELECT *, oid FROM students")  # Creates primary key for you
        records = cursor.fetchall()

        print_records = ""
        Label(screen_database, text="- - - Students - - -", font=("Arial", 11, "bold")).place(x=287, y=300)

        # Loop through db info
        for record in records:
            print_records += str(record[5]) + " " + (record[1]).upper() + ", " + str(record[0]).title() + " - " + str(record[4]) + "\n"

        global students
        students = Label(screen_database, text=print_records, width=38); students.place(x=215, y=320)  # Uses width in 'text units', not pixels. i.e. width of '0' character

        conn.commit()
        conn.close()

    def submit():
        # Connect to db
        conn = sqlite3.connect("student_grades.db")
        cursor = conn.cursor()

        # Insert into table
        cursor.execute("INSERT INTO students VALUES(:forename, :surname, :g1, :g2, :g3)",
                       {
                           "forename": (entry_forename.get()).strip(),
                           "surname": (entry_surname.get()).strip(),
                           "g1": (entry_g1.get()).strip(),
                           "g2": (entry_g2.get()).strip(),
                           "g3": entry_g3.get()
                       })

        conn.commit()
        conn.close()

        # Clear text boxes
        entry_forename.delete(0, END)
        entry_surname.delete(0, END)
        entry_g1.delete(0, END)
        entry_g2.delete(0, END)
        entry_g3.delete(0, END)
        entry_oid.delete(0, END)

        students.destroy()
        query()

    def delete_record():
        # Connect to db
        conn = sqlite3.connect("student_grades.db")
        cursor = conn.cursor()

        # Delete a record
        cursor.execute("DELETE from students WHERE oid= " + entry_oid.get())
        conn.commit()
        conn.close()

        entry_oid.delete(0, END)
        students.destroy()
        query()

    def update_record():
        # Connect to db
        conn = sqlite3.connect("student_grades.db")
        cursor = conn.cursor()

        cursor.execute("""UPDATE students SET
            forename = :forename,
            surname = :surname,
            g1 = :g1,
            g2 = :g2,
            g3 = :g3
            
            WHERE oid = :oid""",
            {
                "forename": entry_forename.get(),
                "surname": entry_surname.get(),
                "g1": entry_g1.get(),
                "g2": entry_g2.get(),
                "g3": entry_g3.get(),
                "oid": entry_oid.get()
            }

        )

        conn.commit()
        conn.close()

        # Clear text boxes
        entry_forename.delete(0, END)
        entry_surname.delete(0, END)
        entry_g1.delete(0, END)
        entry_g2.delete(0, END)
        entry_g3.delete(0, END)
        entry_oid.delete(0, END)

        query()

    def search_record():
        # Clear text boxes
        entry_forename.delete(0, END)
        entry_surname.delete(0, END)
        entry_g1.delete(0, END)
        entry_g2.delete(0, END)
        entry_g3.delete(0, END)

        # Connect to db
        conn = sqlite3.connect("student_grades.db")
        cursor = conn.cursor()

        # Query db
        cursor.execute("SELECT * FROM students WHERE oid = " + entry_oid.get())  # Creates primary key for you
        records = cursor.fetchall()

        for record in records:
            entry_forename.insert(0, record[0])
            entry_surname.insert(0, record[1])
            entry_g1.insert(0, record[2])
            entry_g2.insert(0, record[3])
            entry_g3.insert(0, record[4])

        conn.commit()
        conn.close()

    def predict_g3():
        # Error catching
        g1 = int()
        g2 = int()

        if len(entry_g1.get()) == 0 and len(entry_g2.get()) == 0:
            pass
        elif len(entry_g1.get()) == 0 or len(entry_g2.get()) == 0:
            pass
        else:
            try:
                g1 = int(entry_g1.get())
                g2 = int(entry_g2.get())
            except ValueError:
                messagebox.showerror("Error!", "Grades must be integers!")

        g3 = np.round(regressor.predict([[g1, g2]])).astype(int)

        # Create upper and lower limits for g3 value
        if g3[0] > 20:
            g3[0] = 20
        elif g3[0] < 0:
            g3[0] = 0

        # Check if G1 or G2 in a valid range
        if not(0 <= g1 <= 20) or not(0 <= g2 <= 20):
            messagebox.showerror("Invalid grade!", "Please enter a grade between 0 and 20.")
        else:
            entry_g3.delete(0, END)
            if 0 <= g3[0] <= 4:
                entry_g3.insert(0, "F")
            elif 5 <= g3[0] <= 8:
                entry_g3.insert(0, "D")
            elif 9 <= g3[0] <= 12:
                entry_g3.insert(0, "C")
            elif 13 <= g3[0] <= 15:
                entry_g3.insert(0, "B")
            elif 16 <= g3[0] <= 18:
                entry_g3.insert(0, "A")
            else:
                entry_g3.insert(0, "A*")

    screen_database = Toplevel()
    screen_database.resizable(False, False)
    screen_database.title("Student Database")
    screen_database.geometry("470x700")
    screen_database.iconbitmap("icon.ico")

    # Create/conncet to database
    conn = sqlite3.connect("student_grades.db")

    # Create db cursor
    cursor = conn.cursor()

    # # Create table               <----- Commented out to not create table each execution ----->
    # cursor.execute("""
    # CREATE TABLE students(
    # forename text,
    # surname text,
    # g1 integer,
    # g2 integer,
    # g3 integer
    # )""")

    # Create GUI
    entry_forename = Entry(screen_database, width=30); entry_forename.place(x=30, y=210)
    entry_surname = Entry(screen_database, width=30); entry_surname.place(x=30, y=270)
    entry_g1 = Entry(screen_database, width=30); entry_g1.place(x=30, y=330)
    entry_g2 = Entry(screen_database, width=30); entry_g2.place(x=30, y=390)
    entry_g3 = Entry(screen_database, width=30); entry_g3.place(x=30, y=450)
    entry_oid = Entry(screen_database, width=30); entry_oid.place(x=256, y=210)

    Label(screen_database, text="Final Grade Prediction", font=("Arial", 16, "bold")).place(x=132, y=20)
    Label(screen_database, text="1) Input information", font=("Arial", 9)).place(x=25, y=70)
    Label(screen_database, text="2) Click \'Predict Grade\' button", font=("Arial", 9)).place(x=25, y=90)
    Label(screen_database, text="3) Click \'Save Student\' button", font=("Arial", 9)).place(x=25, y=110)
    Label(screen_database, text="Note: to edit, search for ID and click \'Update\' to save changes.", font=("Arial", 9)).place(x=25, y=140)

    Label(screen_database, text="Forename").place(x=29, y=187)
    Label(screen_database, text="Surname").place(x=29, y=247)
    Label(screen_database, text="Grade 1").place(x=29, y=307)
    Label(screen_database, text="Grade 2").place(x=29, y=367)
    Label(screen_database, text="Final Grade").place(x=29, y=427)
    Label(screen_database, text="Student ID").place(x=255, y=187)

    Button(screen_database, text="Predict Grade", command=predict_g3, relief="groove").place(x=35, y=490)
    Button(screen_database, text="Save Student", command=submit, relief="groove").place(x=130, y=490)
    Button(screen_database, text="Search", command=search_record, relief="groove").place(x=265, y=240)
    Button(screen_database, text="Update", command=update_record, relief="groove").place(x=324, y=240)
    Button(screen_database, text="Delete", command=delete_record, relief="groove").place(x=385, y=240)

    # Defines logout procedure
    def logout():
        screen_database.destroy()
        login()
    Button(screen_database, text="Log Out", command=logout, relief="groove").place(x=10, y=665)

    # Defines help procedure
    def help():
        messagebox.showinfo("Grading Information", "Grades 1 and 2 are numerical (0-20). The final grade is predicted using machine learning and mapped to the following bands:\n\n"
                                                    "0-4:      F\n5-8:      D\n9-12:    C\n13-15:  B\n16-18:  A\n19-20:  A*")
    Button(screen_database, text="Help", command=help, relief="groove").place(x=425, y=665)

    query()

    # Commit Changes
    conn.commit()

    # Close connection
    conn.close()


#  Creates loading screen
logo = PhotoImage(file="logo.gif")
Label(image=logo).place(x=0, y=0)

Label(text="Loading...").place(x=125, y=290)

progress = Progressbar(screen_loading, orient=HORIZONTAL, length=100, mode="determinate")
progress.place(x=102, y=320)

Label(text="Brendan Rogan 2020 \u00A9", font=("Abadi", 8, "italic")).place(x=90, y=370)

for x in range(1, 100):  # Updates progress bar and sleeps after each iteration
    progress["value"] = x
    screen_loading.update_idletasks()
    time.sleep(0.02)

    if x == 99:
        train_model()
        time.sleep(1)
        login()

# Program runs by looping
mainloop()
