from tkinter import *
import os
from GradePredict import graph_plot

# Creates first screen
screen_first = Tk()
screen_first.resizable(False, False)
screen_first.geometry("300x250")
screen_first.title("Teacher Login")


def register():
    def create_user():
        # Assigns text in entry fields to _reg variables
        username_reg = entry_reg_username.get()
        password_reg = entry_reg_password.get()

        # Clears text in entry fields
        entry_reg_username.delete(0, END)
        entry_reg_password.delete(0, END)

        # Creates a text file using username as filename to store user info
        user_file = open(username_reg, "w")
        user_file.write(username_reg + "\n" + password_reg)
        user_file.close()

        Label(screen_register, text="Registration Successful!", fg="green", font=("calibri", 11)).pack()

    # Creates a new toplevel screen
    screen_register = Toplevel(screen_first)
    screen_register.resizable(False, False)
    screen_register.title("Register")
    screen_register.geometry("300x250")

    # Creates & places labels and a button. Assigns button to nested function above
    Label(screen_register, text="Register User", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()

    Label(screen_register, text="Please enter details").pack()
    Label(screen_register, text="").pack()

    Label(screen_register, text="Username").pack()
    entry_reg_username = Entry(screen_register); entry_reg_username.pack()
    Label(screen_register, text="").pack()
    Label(screen_register, text="Password").pack()
    entry_reg_password = Entry(screen_register, show="*"); entry_reg_password.pack()
    Label(screen_register, text="").pack()

    Button(screen_register, text="Register", width="10", height="1", command=create_user).pack()


def mainscreen():
    # Creates new toplevel screen
    screen_main = Toplevel(screen_first)
    screen_main.resizable(False, False)
    screen_main.title("Grade Prediction System")
    screen_main.geometry("700x300")

    Label(screen_main, text="Grade Prediction System", bg="orange", width="700", height="2", font=("Calibri", 13)).pack()

    Button(screen_main, text="Generate Graph", width="20", height="1", font=("Calibri", 13), command=graph_plot).pack()


def login():
    def login_verify():
        # Assigns text in entry fields to _log variables
        username_log = entry_log_username.get()
        password_log = entry_log_password.get()

        # Clears text in entry fields
        entry_log_username.delete(0, END)
        entry_log_password.delete(0, END)

        # Checks current filedir to match username w/ filename then checks password
        file_list = os.listdir()
        if username_log in file_list:
            user_file = open(username_log, "r")
            verify = user_file.read().splitlines()

            if password_log in verify:
                screen_login.destroy()
                screen_first.withdraw()
                mainscreen()
            else:
                Label(screen_login, text="Account not recognised!", fg="green", font=("calibri", 11)).pack()
        else:
            Label(screen_login, text="Account not recognised!", fg="green", font=("calibri", 11)).pack()

    # Creates a new toplevel screen
    screen_login = Toplevel(screen_first)
    screen_login.resizable(False, False)
    screen_login.title("Login")
    screen_login.geometry("300x250")

    # Creates and places labels, entry fields, and a button
    Label(screen_login, text="Login", bg="pink", width="300", height="2", font=("Calibri", 13)).pack()

    Label(screen_login, text="Please enter details").pack()
    Label(screen_login, text="").pack()

    Label(screen_login, text="Username").pack()
    entry_log_username = Entry(screen_login); entry_log_username.pack()
    Label(screen_login, text="").pack()
    Label(screen_login, text="Password").pack()
    entry_log_password = Entry(screen_login, show="*"); entry_log_password.pack()
    Label(screen_login, text="").pack()

    Button(screen_login, text="Login", width="10", height="1", command=login_verify).pack()


# Creates and places labels and buttons
Label(text="Teacher Login", bg="grey", width="300", height="2", font=("Calibri", 13)).pack()
Label(text="").pack()  # Blank line
Button(text="Login", width="30", height="2", command=login).pack()
Label(text="").pack()
Button(text="Register", width="30", height="2", command=register).pack()
Label(text="").pack()
Label(text="").pack()
Label(text="Brendan Rogan \u00A9").pack()

# Program runs by looping
screen_first.mainloop()
