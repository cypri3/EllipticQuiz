import os
import random
from tkinter import Frame, OptionMenu, Radiobutton, Scale, Tk, Button, Label, StringVar, Entry, IntVar
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

    window_width = root.winfo_width()
    window_height = root.winfo_height()

    scale_percentage = 0.35

    new_width = int(window_width * scale_percentage)
    new_height = int(window_height * scale_percentage)

    if new_width <= 0 or new_height <= 0:
        new_width, new_height = 400, 400  
    
    question_img.thumbnail((new_width, new_height))
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
        radio_frame.pack_forget() 
        cheat_button.place_forget()
        number_entry.place(relx=0.5, rely=0.8, anchor="center")
    else:
        number_entry.place_forget()
        radio_frame.pack(pady=10)  
        cheat_button.place(relx=0.5, rely=0.9, anchor="center")

# Check the answer (True/False or numeric)
def check_answer(t=None):
    question_file = current_question.get()

    if numeric_mode:
        # Numeric answer check
        correct_answer = int(question_file.split('_')[1].split('.png')[0])
        user_answer = number_var.get()
        if user_answer == "":
            global score
            score += 0.2
            is_correct = False
        else:
            user_answer = int(user_answer)
            is_correct = (user_answer == correct_answer)
    else:
        # True/False answer check
        question_num = question_file.split("question")[1].split(".png")[0]
        correct_answer_file = f"reponse{question_num}_1.png"
        correct_answer_path = os.path.join(response_dir, correct_answer_file)
        is_correct = os.path.exists(correct_answer_path)

    update_score(is_correct)

    show_question()

# Update the score
def update_score(is_correct):
    cheat_result.set("")
    cheat_label.config(image=None)
    cheat_label.image = None

    global score, total, numeric_mode
    user_confidence = confidence_value.get() / 100

    if not numeric_mode:
        if is_correct:
            question_score = (1/5) * (8 * (1 - 2 * (1 - user_confidence)**2) - 3)
        else:
            question_score = (1/5) * (8 * (1 - 2 * user_confidence**2) - 3)
        if(question_score != 1):
            show_cheat()
        score += question_score
    else:
        if(is_correct):
            score += 1
        else:
            question_file = current_question.get()
            correct_answer = int(question_file.split('_')[1].split('.png')[0])
            previous_result.set(f"Incorrect. Here is the solution: {correct_answer}")
        number_var.set("")
    total += 1
    score_label.config(text=f"Score: {round(score,2)} / {total}")

# Show the cheat answer (image and text)
def show_cheat():
    question_file = current_question.get()
    question_num = question_file.split("question")[1].split(".png")[0]
    correct_answer_file = f"reponse{question_num}_1.png"  # Correct answer is always with '1'
    correct_answer_path = os.path.join(response_dir, correct_answer_file)

    if os.path.exists(correct_answer_path):
        answer_img = Image.open(correct_answer_path)
    else:
        answer_img = Image.open(os.path.join(response_dir,f"reponse{question_num}_0.png"))

    window_width = root.winfo_width()
    window_height = root.winfo_height()

    scale_percentage = 0.40

    new_width = int(window_width * scale_percentage)
    new_height = int(window_height * scale_percentage)

    if new_width <= 0 or new_height <= 0:
        new_width, new_height = 400, 400  
    

    answer_img.thumbnail((new_width, new_height))
    answer_image = ImageTk.PhotoImage(answer_img)
    cheat_label.config(image=answer_image)
    cheat_label.image = answer_image

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
number_var = StringVar()

# Create buttons and labels
question_label = Label(root)
question_label.pack(pady=20)

radio_frame = Frame(root)
radio_frame.pack(pady=10)  

confidence_value = IntVar(value=0)
radio_buttons = []
for idx, i in enumerate(range(0, 101, 10)):
    radio_button = Radiobutton(radio_frame, text=f"{i}%", variable=confidence_value, value=i)
    radio_button.grid(row=1, column=idx, padx=5, pady=10)
    radio_buttons.append(radio_button)

validate_button = Button(radio_frame, text="Valider", command=check_answer)
validate_button.grid(row=2, columnspan=len(radio_buttons), pady=10)

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

# Key bindings for selection
root.bind("<Return>", check_answer)

# Run the application
root.mainloop()
