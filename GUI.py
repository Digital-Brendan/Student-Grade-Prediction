from tkinter import *
import sys


def create_gui():
    def command1(event):
        if entry_user.get() == "teacher_admin" and entry_pass.get() == "password":
            root.deiconify()
            top.destroy()
        else:
            popup = Tk()
            popup.wm_title("Error!")
            label_popup = Label(popup, text="Incorrect username or password!", font=("Helvetica", 10))
            label_popup.pack()

    def command2():
        top.destroy()
        root.destroy()
        sys.exit()

    def on_closing():
        sys.exit()

    root = Tk()
    top = Toplevel()

    top.geometry("350x450")
    top.title("TEACHER LOGIN")
    top.configure(bg="#8c7ae6")

    logo = PhotoImage(file="logo.gif")
    label_logo = Label(top, image=logo, bg="white")

    label_user = Label(top, text="Username:", font=("Helvetica", 10), bg="white")
    entry_user = Entry(top, relief="solid")
    label_pass = Label(top, text="Password:", font=("Helvetica", 10), bg="white")
    entry_pass = Entry(top, show="*", relief="solid")

    entry_pass.bind("<Return>", command1)
    button_exit = Button(top, text="Cancel", command=lambda: command2(), relief="solid", borderwidth=1, bg="#0097e6")

    label_footer = Label(top, text="Brendan Rogan 2020 \u00A9", font=("Arial", 8), bg="white")

    label_logo.pack()
    label_user.pack()
    entry_user.pack()
    label_pass.pack()
    entry_pass.pack()
    button_exit.pack()
    label_footer.pack()

    root.title("Main Screen")
    root.configure(bg="white")
    root.geometry("855x650")

    root.withdraw()
    top.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
