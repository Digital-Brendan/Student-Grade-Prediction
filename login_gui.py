from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import numpy as np
import os
import time
import sqlite3
from GradePredict import regressor, train_model

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
    Button(screen_login, text="Login", bg="#C1CDCD", font=("Abadi", 12, "bold"), relief="flat", command=login_verify).place(x=120, y=286)
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
    Button(screen_register, text="Register", bg="#C1CDCD", font=("Abadi", 12, "bold"), relief="flat", command=create_user).place(x=110, y=286)


def database():
    def query():
        # Connect to db
        conn = sqlite3.connect("student_grades.db")
        cursor = conn.cursor()

        # Query db
        cursor.execute("SELECT *, oid FROM students")  # Creates primary key for you
        records = cursor.fetchall()

        print_records = ""

        # Loop through db info
        for record in records:
            print_records += str(record[5]) + " " + (record[1]).upper() + ", " + str(record[0]).title() + " - " + str(record[4]) + "\n"

        global students
        students = Label(screen_database, text=print_records); students.place(x=440, y=30)

        conn.commit()
        conn.close()

    def submit():
        # Connect to db
        conn = sqlite3.connect("student_grades.db")
        cursor = conn.cursor()

        # Insert into table
        cursor.execute("INSERT INTO students VALUES(:forename, :surname, :g1, :g2, :g3)",
                       {
                            "forename": entry_forename.get(),
                            "surname": entry_surname.get(),
                            "g1": entry_g1.get(),
                            "g2": entry_g2.get(),
                            "g3": entry_g3.get()
                       })  # Creates placeholder variables

        conn.commit()
        conn.close()

        # Clear text boxes
        entry_forename.delete(0, END)
        entry_surname.delete(0, END)
        entry_g1.delete(0, END)
        entry_g2.delete(0, END)
        entry_g3.delete(0, END)

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

    def predict_g3():
        if len(entry_g1.get()) == 0 or len(entry_g2.get()) == 0:
            messagebox.showerror("Error", "Do not leave the grades blank!")

        # Error catching
        g1 = int()
        g2 = int()

        try:
            g1 = int(entry_g1.get())
            g2 = int(entry_g2.get())
        except ValueError:
            messagebox.showerror("Error", "Grades must be integers!")

        g3 = np.round(regressor.predict([[g1, g2]])).astype(int)

        if g3[0] > 20:
            g3[0] = 20
        elif g3[0] < 0:
            g3[0] = 0

        # Check if G1 or G2 in a valid range
        if not(0 <= g1 <= 20) or not(0 <= g2 <= 20):
            messagebox.showerror("Invalid grade!", "Please enter a grade between 0 and 20.")
        else:
            entry_g3.delete(0, END)
            entry_g3.insert(0, str(g3[0]))

    screen_database = Toplevel()
    screen_database.resizable(False, False)
    screen_database.title("Student Database")
    screen_database.geometry("700x300")
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
    entry_forename = Entry(screen_database, width=30); entry_forename.place(x=30, y=35)
    entry_surname = Entry(screen_database, width=30); entry_surname.place(x=30, y=90)
    entry_g1 = Entry(screen_database, width=30); entry_g1.place(x=30, y=145)
    entry_g2 = Entry(screen_database, width=30); entry_g2.place(x=30, y=200)
    entry_g3 = Entry(screen_database, width=30); entry_g3.place(x=30, y=255)
    entry_oid = Entry(screen_database, width=30); entry_oid.place(x=250, y=200)

    Label(screen_database, text="Forename").place(x=28, y=10)
    Label(screen_database, text="Surname").place(x=28, y=65)
    Label(screen_database, text="G1 Grade").place(x=28, y=120)
    Label(screen_database, text="G2 Grade").place(x=28, y=175)
    Label(screen_database, text="G3 Grade").place(x=28, y=230)
    Label(screen_database, text="Enter ID of student to delete").place(x=250, y=175)

    Button(screen_database, text="Predict G3 Grade", command=predict_g3).place(x=250, y=35)
    Button(screen_database, text="Add Student to database", command=submit).place(x=250, y=80)
    Button(screen_database, text="Delete", command=delete_record).place(x=250, y=225)

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
