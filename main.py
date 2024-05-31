from tkinter import *
import tkinter.messagebox
from textwrap import wrap
from tkinter import messagebox
import json
import random

# Global vriables
show_ans = ""
random_question = ""
imported_json = ""
total_answers = 0
right_answers = 0

# Color pallet
YELLOW = "#FBFF72"
BLACK = "#030303"
WHITE = "#FFFFF2"

# _____________Main UI_____________
# Window
window = Tk()
window.title("Flash Cards")
window.minsize(width=550, height=500)
window.config(bg=YELLOW)
window.resizable(False, False)
# _____________Frames_____________
def show_page(page):
    page.tkraise()


container = Frame(window, width=550, height=500, bg='black')
container.place(x=0, y=0)
main_page = Frame(container, width=550, height=500, bg='white')
main_page.place(x=0, y=0)
import_page = Frame(container, width=550, height=500, bg='green')
import_page.place(x=0, y=0)
export_page = Frame(container, width=550, height=500, bg='blue')
export_page.place(x=0, y=0)

show_page(main_page)
# _____________Delete JSON Data_____________
def delete_results():
    with open("results.json", 'w') as file:
        # truncate() method removes all data from the file
        file.truncate()

def delete_results_on_closing():
    with open("results.json", 'w') as file:
        file.truncate()
        window.destroy()


# _____________Greyed out default text_____________
def handle_focus_in(widget):
    widget.delete("1.0", END)
    widget.config(fg='black')

def handle_focus_in_entry(_):
    file_entry.delete(0, END)
    file_entry.config(fg='black')

def handle_focus_in_term(_):
    term_entry.delete(0, END)
    term_entry.config(fg='black')
# _____________Menu_____________
menu_bar = Menu(window)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Home', command=lambda: show_page(main_page))
file_menu.add_command(label='Import', command=lambda: show_page(import_page))
file_menu.add_command(label='Export', command=lambda: show_page(export_page))
file_menu.add_separator()
menu_bar.add_cascade(label='File', menu=file_menu)
window.config(menu=menu_bar)
# _____________Canvas main page_____________

canvas = Canvas(main_page, width=550, height=500, bg=WHITE, highlightthickness=0)
canvas.create_rectangle(110, 50, 445, 105, fill=YELLOW, width=0)
# Term label
term_text = canvas.create_text(280, 80, text="", fill='black', justify="center", width=300, font=("Courier", 12, "italic", "bold"))
canvas.pack()
# Multiline text box for user
guess_text = Text(main_page, height=6, width=50, borderwidth=1)
guess_text.place(x=75, y=125)
guess_text.config(fg='grey')
guess_text.insert(END, "Your answer")
guess_text.bind("<FocusIn>", lambda event, guess_text=guess_text: handle_focus_in(guess_text))

# The right answer

c_input = ""
right_answer = '\n'.join(wrap(c_input, width=50))
answer = canvas.create_text(280, 285, text=right_answer, fill=BLACK, font=("Courier", 8))


# _____________Button Commands_____________
def correct():
    global imported_json
    global random_question
    global show_ans
    global total_answers
    global right_answers
    total_answers += 1
    right_answers += 1
    try:
        with open("results.json", "r") as data_file:
            data = json.load(data_file)
            data[random_question[0]]["score"] = data[random_question[0]]["score"] + 1
            with open("results.json", "w") as data_file:
                json.dump(data, data_file)

    except:
        messagebox.showerror(title="Error", message="Please import the file first!")

    try:
        with open(f"{imported_json}.json", "r") as data_file:
            data = json.load(data_file)
            random_question = random.choice(list(data.items()))
            show_ans = data[random_question[0]]["definition"]
            canvas.itemconfig(answer, text="")
            canvas.itemconfig(term_text, text=random_question[0])

    except:
        messagebox.showerror(title="Error", message="Please import the file first!")

    hide_button(correct_b, show_answer_b)


def wrong():
    global imported_json
    global random_question
    global show_ans
    global total_answers
    total_answers += 1
    try:
        with open("results.json", "r") as data_file:
            data = json.load(data_file)
            data[random_question[0]]["score"] = data[random_question[0]]["score"] - 1
            with open("results.json", "w") as data_file:
                json.dump(data, data_file)

    except:
        messagebox.showerror(title="Error", message="Please import the file first!")

    try:
        with open(f"{imported_json}.json", "r") as data_file:
            data = json.load(data_file)
            random_question = random.choice(list(data.items()))
            show_ans = data[random_question[0]]["definition"]
            canvas.itemconfig(answer, text="")
            canvas.itemconfig(term_text, text=random_question[0])

    except:
        messagebox.showerror(title="Error", message="Please import the file first!")

    hide_button(correct_b, show_answer_b)


def skip():
    global imported_json
    global random_question
    global show_ans
    try:
        with open(f"{imported_json}.json", "r") as data_file:
            data = json.load(data_file)
            random_question = random.choice(list(data.items()))
            show_ans = data[random_question[0]]["definition"]
            canvas.itemconfig(answer, text="")
            canvas.itemconfig(term_text, text=random_question[0])

    except:
        messagebox.showerror(title="Error", message="Please import the file first!")


def show_answer():
    if show_ans == "":
        messagebox.showerror(title="Error", message="Please import the file first!")
    else:
        right_answer = '\n'.join(wrap(show_ans, width=65))
        canvas.itemconfig(answer, text=right_answer)
        hide_button(show_answer_b, correct_b)


def info():
    # global total_answers
    # global right_answers
    try:
        with open("results.json", "r") as data_file:
            data = json.load(data_file)
            lst = []
            for n in data:
                score = data[n]["score"]
                lst.append(f"{n}: {score}")
        grade = round((right_answers / total_answers) * 100)
        lst.append(f"Grade: {grade} %")
        results = "\n".join(lst)
        messagebox.showinfo(title="Results", message=results)
    except:
        messagebox.showerror(title="Error", message="Please import the file first!")

def hide_button(current, replacement):
    current.place(x=1000, y=1000)
    replacement.place(x=380, y=420)


# _____________Buttons_____________
wrong_b = Button(main_page, width=12, text="Wrong", command=wrong, highlightthickness=4, state="normal", borderwidth=0, height=1, bg=YELLOW)
wrong_b.place(x=88, y=420)
skip_b = Button(main_page, width=12, text="Skip", command=skip, highlightthickness=4, state="normal", borderwidth=0, height=1, bg=YELLOW)
skip_b.place(x=230, y=420)
show_answer_b = Button(main_page, width=12, text="Show Answer", command=show_answer, highlightthickness=4, state="normal", borderwidth=0, height=1, bg=YELLOW)
show_answer_b.place(x=370, y=420)
correct_b = Button(main_page, width=12, text="Correct", command=correct, state="normal", highlightthickness=4, borderwidth=0, height=1, bg=YELLOW)
correct_b.place(x=1000, y=1000)
info_b = Button(main_page, text="    ℹ️", width=2, command=info, highlightthickness=0, state="normal", font=(10), borderwidth=0, bg=WHITE)
info_b.place(x=20, y=20)


# _____________Canvas Import Page_____________
canvas_import_page = Canvas(import_page, width=550, height=500, bg=WHITE, highlightthickness=0)
canvas_import_page.pack()
import_file = Entry(import_page, width=40)
import_file.insert(END, string="")
import_file.place(x=175, y=65)
imp_label = Label(import_page, text='File name:', bg=WHITE, font=("Courier", 10))
imp_label.place(x=80, y=65)
# _____________Button function_____________

def import_data():
    delete_results()
    global imported_json
    imported_json = import_file.get()
    try:
        with open(f"{imported_json}.json", "r") as data_file:
            global show_ans
            global random_question
            data = json.load(data_file)
            random_question = random.choice(list(data.items()))
            show_ans = data[random_question[0]]["definition"]
            canvas.itemconfig(term_text, text=random_question[0])

        with open(f"{imported_json}.json", "r") as key_data:
            imported_data = json.load(key_data)
            key_values = list(imported_data.keys())

            for k in key_values:
                results_data = {
                    k: {
                        "score": 0,
                    }
                }
                try:
                    with open("results.json", "r") as data_file:
                        data = json.load(data_file)

                except:
                    with open("results.json", "w") as data_file:
                        json.dump(results_data, data_file, indent=4)
                else:
                    data.update(results_data)

                    with open("results.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="File not found!\n Please check the spelling.")

imp_button = Button(import_page, text="Import Data", command=import_data, highlightthickness=4, state="normal", borderwidth=0, height=1, bg=YELLOW)
imp_button.place(x=225, y=220)

# _____________Export page_____________
canvas_export_page = Canvas(export_page, width=550, height=500, bg=WHITE, highlightthickness=0)
canvas_export_page.pack()
file_entry = Entry(export_page, width=40)
file_entry.place(x=155, y=65)
file_entry.config(fg='grey')
file_entry.insert(0, 'File name')
file_entry.bind("<FocusIn>", handle_focus_in_entry)
term_entry = Entry(export_page, width=40)
term_entry.config(fg='grey')
term_entry.insert(0, 'Term')
term_entry.place(x=155, y=90)
definition_textbox = Text(export_page, height=15, width=50)
definition_textbox.place(x=90, y=120)
definition_textbox.config(fg='grey', font=("Calibri", 10))
definition_textbox.insert(END, "Term definition")
# _____________Button function_____________
def exp_json():
    file_name_json = file_entry.get()
    term_entry_json = term_entry.get()
    definition_json = definition_textbox.get("0.0", END)
    new_data = {
        term_entry_json: {
            "definition": definition_json,
        }
    }
    if file_name_json == "" or term_entry_json == "" or definition_json == "":
        messagebox.showerror(title="Error", message="One of the fields are empty!\n Please fill the empty fields")
    else:
        try:
            with open(f"{file_name_json}.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open(f"{file_name_json}.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open(f"{file_name_json}.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            term_entry.delete(0, END)
            definition_textbox.delete("0.0", END)

exp_button = Button(export_page, text="Save", command=exp_json, width=10, highlightthickness=4, state="normal", borderwidth=0, height=1, bg=YELLOW)
exp_button.place(x=232, y=420)


window.protocol("WM_DELETE_WINDOW", delete_results_on_closing)


# Main loop
window.mainloop()
