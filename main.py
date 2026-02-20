import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
from datetime import datetime

# ---------------- LOAD QUESTIONS ----------------
with open("questions.json", "r") as f:
    questions = json.load(f)

current_q = 0
score = 0
start_time = 0
start_timestamp = ""
end_timestamp = ""

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Quiz Application")
root.geometry("450x450")
root.configure(bg="#FF8FAB")

# ---------------- STYLE ----------------
style = ttk.Style()
style.theme_use("default")

style.configure("TButton", font=("Arial", 10, "bold"), padding=8)
style.configure("Title.TLabel", font=("Arial", 16, "bold"), background="#f2f2f2")
style.configure("TLabel", font=("Arial", 11), background="#f2f2f2")
style.configure("TRadiobutton", font=("Arial", 10), background="#f2f2f2")

# ---------------- FRAME 1 (NAME ENTRY) ----------------
frame1 = ttk.Frame(root, padding=30)
frame1.place(relx=0.5, rely=0.5, anchor="center")

ttk.Label(frame1, text="Quiz Application", style="Title.TLabel").pack(pady=10)
ttk.Label(frame1, text="Enter your Name").pack(pady=5)

name_entry = ttk.Entry(frame1, width=25)
name_entry.pack()

warning = ttk.Label(frame1, text="", foreground="red")
warning.pack(pady=5)

# ---------------- FRAME 2 (QUIZ) ----------------
frame2 = ttk.Frame(root, padding=20)

question_label = ttk.Label(frame2, text="", wraplength=380, font=("Arial", 12, "bold"))
question_label.pack(pady=10)

var = tk.StringVar()

rb1 = ttk.Radiobutton(frame2, variable=var)
rb2 = ttk.Radiobutton(frame2, variable=var)
rb3 = ttk.Radiobutton(frame2, variable=var)
rb4 = ttk.Radiobutton(frame2, variable=var)

rb1.pack(anchor="w", pady=2)
rb2.pack(anchor="w", pady=2)
rb3.pack(anchor="w", pady=2)
rb4.pack(anchor="w", pady=2)

# ---------------- FUNCTIONS ----------------
def load_question():
    q = questions[current_q]

    question_label.config(text=q["question"])

    rb1.config(text=q["options"][0], value=q["options"][0])
    rb2.config(text=q["options"][1], value=q["options"][1])
    rb3.config(text=q["options"][2], value=q["options"][2])
    rb4.config(text=q["options"][3], value=q["options"][3])

    var.set("")

def save_result(total_time):
    result = {
        "name": name_entry.get(),
        "score": score,
        "total_questions": len(questions),
        "start_time": start_timestamp,
        "end_time": end_timestamp,
        "time_taken_seconds": total_time
    }

    try:
        with open("results.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(result)

    with open("results.json", "w") as f:
        json.dump(data, f, indent=4)

def check_next():
    global current_q, score, end_timestamp

    if var.get() == "":
        messagebox.showwarning("Warning", "Please select an option")
        return

    selected = var.get().strip().lower()
    correct = questions[current_q]["answer"].strip().lower()

    if selected == correct:
        score += 1

    current_q += 1

    if current_q < len(questions):
        load_question()
    else:
        end_time = time.time()
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_time = int(end_time - start_time)

        save_result(total_time)

        messagebox.showinfo(
            "Quiz Result",
            f"Name: {name_entry.get()}\n"
            f"Score: {score}/{len(questions)}\n\n"
            f"Start Time: {start_timestamp}\n"
            f"End Time: {end_timestamp}\n"
            f"Time Taken: {total_time} seconds"
        )
        root.destroy()

def start_quiz():
    global start_time, start_timestamp

    if name_entry.get().strip() == "":
        warning.config(text="Please enter your name")
    else:
        warning.config(text="")
        frame1.place_forget()
        frame2.place(relx=0.5, rely=0.5, anchor="center")

        start_time = time.time()
        start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        load_question()

# ---------------- BUTTONS ----------------
ttk.Button(frame1, text="Start Quiz", command=start_quiz).pack(pady=15)
ttk.Button(frame2, text="Next", command=check_next).pack(pady=15)

root.mainloop()