import os
import random
from tkinter import Tk, Button, Label, StringVar, Entry, IntVar
from PIL import Image, ImageTk

# Question and answer directories
question_dir = "question"
response_dir = "reponse"
chiffres_dir = "chiffres"

# List question files
question_files = [f for f in os.listdir(question_dir) if f.endswith(".png")]
chiffre_files = [f for f in os.listdir(chiffres_dir) if f.endswith(".png")]

# Combine all question files
all_question_files = question_files + chiffre_files
random.shuffle(all_question_files)

# Variable to store the previous question number != index (cf. after shuffle)
last_question_num = None

# Current question index
question_index = 0  

def get_random_question():
    global question_index
    if question_index >= len(all_question_files):
        random.shuffle(all_question_files)  # Shuffle questions already asked
        question_index = 0
    question_file = all_question_files[question_index]
    question_index += 1
    return question_file

# Display the question image
def show_question():
    global last_question_num, numeric_mode
    question_file = get_random_question()
    question_path = os.path.join(question_dir if question_file in question_files else chiffres_dir, question_file)
    question_img = Image.open(question_path)
    question_img.thumbnail((600, 600))  # Resize for display
    question_image = ImageTk.PhotoImage(question_img)

    question_label.config(image=question_image)
    question_label.image = question_image
    current_question.set(question_file)

    # Detect numeric mode
    numeric_mode = "_" in question_file
    toggle_answer_mode()

    if "question" in question_file:
        last_question_num = question_file.split("question")[1].split('_')[0]
    else:
        last_question_num = question_file.split('_')[0]

# Toggle between True/False and numeric entry modes
def toggle_answer_mode():
    if numeric_mode:
        true_button.place_forget()
        false_button.place_forget()
        cheat_button.place_forget() 
        number_entry.place(relx=0.5, rely=0.8, anchor="center")
    else:
        number_entry.place_forget()
        true_button.place(relx=0.4, rely=0.8, anchor="center")
        false_button.place(relx=0.6, rely=0.8, anchor="center")
        cheat_button.place(relx=0.5, rely=0.9, anchor="center")

# Check the answer (True/False or numeric)
def check_answer(is_true=None):
    question_file = current_question.get()

    if numeric_mode:
        # Numeric answer check
        correct_answer = int(question_file.split('_')[1].split('.png')[0])
        user_answer = int(number_var.get())
        is_correct = (user_answer == correct_answer)
    else:
        # True/False answer check
        question_num = question_file.split("question")[1].split(".png")[0]
        correct_answer_file = f"reponse{question_num}_{'1' if is_true else '0'}.png"
        correct_answer_path = os.path.join(response_dir, correct_answer_file)
        is_correct = os.path.exists(correct_answer_path)

    result = "Correct!" if is_correct else "Incorrect. Here is the solution"
    previous_result.set(f"Previous answer: {result}")
    update_score(is_correct)

    show_question()

# Update the score
def update_score(is_correct):
    cheat_result.set("Cheat: ")
    cheat_label.config(image=None)
    cheat_label.image = None

    global score, total
    if is_correct:
        score += 1
    else:
        global numeric_mode
        score -= 3
        if not numeric_mode:
            show_cheat()
        else:
            question_file = current_question.get()
            correct_answer = int(question_file.split('_')[1].split('.png')[0])
            previous_result.set(f"Incorrect. Here is the solution: {correct_answer}")
    if numeric_mode:
        number_var.set("")
    total += 1
    score_label.config(text=f"Score: {score} / {total}")

# Show the cheat answer (image and text)
def show_cheat():
    question_file = current_question.get()
    question_num = question_file.split("question")[1].split(".png")[0]
    correct_answer_file = f"reponse{question_num}_1.png"  # Correct answer is always with '1'
    correct_answer_path = os.path.join(response_dir, correct_answer_file)

    if os.path.exists(correct_answer_path):
        answer_img = Image.open(correct_answer_path)
        cheat_result.set("Cheat: The answer is True")
    else:
        answer_img = Image.open(os.path.join(response_dir,f"reponse{question_num}_0.png"))
        cheat_result.set("Cheat: The answer is False")

    answer_img.thumbnail((600, 600))  # Resize for display
    answer_image = ImageTk.PhotoImage(answer_img)
    cheat_label.config(image=answer_image)
    cheat_label.image = answer_image

# Navigate with arrow keys (left/right)
def navigate(event):
    global selected_button
    if event.keysym == "Left":
        selected_button = false_button
    elif event.keysym == "Right":
        selected_button = true_button
    update_button_highlight()

# Highlight the selected button
def update_button_highlight():
    if selected_button == true_button:
        true_button.config(bg="darkgreen", fg="white")
        false_button.config(bg="red", fg="white")
    else:
        false_button.config(bg="darkred", fg="white")
        true_button.config(bg="green", fg="white")

# Select the active button (Enter)
def select_answer(event):
    if numeric_mode:
        check_answer()  # Numeric mode, check with entry
    elif selected_button == true_button:
        check_answer(True)
    else:
        check_answer(False)

# Create the GUI
root = Tk()
root.title("Quiz Application")

# Current question variable
current_question = StringVar()

# Previous answer variable
previous_result = StringVar()

# Initialize score
score = 0
total = 0

# Numeric entry variable
number_var = IntVar()

# Create buttons and labels
question_label = Label(root)
question_label.pack(pady=20)

true_button = Button(root, text="True", command=lambda: check_answer(True), width=20, height=2, bg="green", fg="white")
false_button = Button(root, text="False", command=lambda: check_answer(False), width=20, height=2, bg="red", fg="white")
number_entry = Entry(root, textvariable=number_var, width=10, font=("Arial", 16))

cheat_button = Button(root, text="Cheat", command=show_cheat, width=20, height=2, bg="yellow", fg="black")
cheat_button.place(relx=0.5, rely=0.9, anchor="center")

score_label = Label(root, text=f"Score: {score} / {total}")
score_label.pack()

previous_result_label = Label(root, textvariable=previous_result)
previous_result_label.pack()

cheat_label = Label(root)
cheat_label.pack(pady=10)

cheat_result = StringVar()
cheat_result_label = Label(root, textvariable=cheat_result)
cheat_result_label.pack()

# Show the first question
show_question()

# Key bindings for arrow navigation and selection
root.bind("<Left>", navigate)
root.bind("<Right>", navigate)
root.bind("<Return>", select_answer)

# Initialize button highlight
selected_button = true_button
update_button_highlight()

# Run the application
root.mainloop()
