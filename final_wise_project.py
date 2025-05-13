from tkinter import *
import sqlite3


question = {
    "What comes next in the series? 1, 1, 2, 3, 5, 8, 13, ...": ['15', '20', '21', '30'],
    "Which number is the odd one out? 3, 5, 7, 11, 14, 17": ['3', '7', '11', '14'],
    "What is the missing number? 4, 8, 16, 32, ?, 128": ['48', '56', '64', '72'],
    "Which letter comes next in the series? A, C, E, G, ?": ['I', 'J', 'K', 'L'],
    "Mary's father has five daughters: Nana, Nene, Nini, Nono.\nWhat is the name of the fifth daughter?": ['Nunu', 'Mary', 'Nana', 'Nene'],
    "A plane crashes on the border of the U.S. and Canada.\nWhere do they bury the survivors?": ['In the U.S.', 'In Canada', 'At sea', 'Nowhere'],
    "How many months have 28 days?": ['1', '2', 'All of them', 'None of them'],
    "If you have it, you want to share it.\nIf you share it, you don't have it. What is it?": ['Money', 'A secret', 'Time', 'Knowledge'],
    "What can be broken, but is never held?": ['A promise', 'A glass', 'A heart', 'A rule'],
    "What has keys but can't open locks?": ['A map', 'A piano', 'A car', 'A house'],
    "What has a heart that doesn’t beat?": ['A dead person', 'An artichoke', 'A clock', 'A book'],
    "What is black when you buy it,\nred when you use it,\nand gray when you throw it away?": ['Coal', 'A pencil', 'A candle', 'A car'],
    "If you rearrange the letters “CIFAIPC”\nyou would have the name of a(n)": ['City', 'Animal', 'Ocean', 'River'],
    "What can you hold in your right hand, but not in your left?": ['Your left hand', 'A pencil', 'A book', 'A cup'],
    "What gets wetter the more it dries?": ['A towel', 'Water', 'A sponge', 'Clothes'],
    "What word in the English language does the following:\nthe first two letters signify a male,\nthe first three letters signify a female,\nthe first four letters signify a great,\nwhile the entire world signifies a great woman.\nWhat is the word?": ['Heroine', 'Female', 'Lady', 'Girl'],
    "What has a neck but no head?": ['A bottle', 'A guitar', 'A shirt', 'A person'],
    "Choose the number that is 1/4 of 1/2 of 1/5 of 200": ['2', '5', '10', '50'],
    "I speak without a mouth and hear without ears.\nI have no body, but I come alive with the wind.\nWhat am I?": ['An echo', 'A song', 'A shadow', 'A dream'],
    "What is seen in the middle of March and April \nthat can't be seen at the beginning or end of either month?": ['The letter R', 'The letter A', 'The letter M', 'The letter P']

}

ans = ['21', '14', '64', 'I', 'Mary', 'Nowhere', 'All of them', 'A secret', 'A promise', 'A piano', 'An artichoke', 'Coal', 'City', 'Your left hand', 'A towel', 'Heroine', 'A bottle', '5', 'An echo', 'The letter R']

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IQ TEST")
        self.root.geometry("1800x1920")
        self.root.minsize(950, 570)

        # Set the logo image
        logo_image = PhotoImage(file="colorful-bird-img.png") 
        self.root.iconphoto(True, logo_image)

        self.user_ans = StringVar()
        self.user_ans.set('None')
        self.user_score = IntVar()
        self.user_score.set(0)
        
        # Database setup
        self.conn = sqlite3.connect('quiz_database.db')
        self.c = self.conn.cursor()
        self.create_database_table()


    def create_database_table(self):
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  age INTEGER,
                  score INTEGER
              )
              ''')
        self.conn.commit()

        self.current_question = 0

        self.f1 = Frame(self.root)
        self.f1.pack(side=TOP, fill=X)
        self.welcome()

        self.login_frame = Frame(self.root)
        self.login_frame.pack(side=TOP, fill=X, pady=150)

        Label(self.login_frame, text="Enter your name:", font="consolas 20 bold", fg="#333300").pack()
        self.name_entry = Entry(self.login_frame, insertwidth=10)
        self.name_entry.pack()

        Label(self.login_frame, text="Enter your age:", font="consolas 20 bold", fg="#333300").pack()
        self.age_entry = Entry(self.login_frame, insertwidth=10)
        self.age_entry.pack()

        self.login_button = Button(self.login_frame, text="Login", command=self.login, font="consolas 17 bold", fg="#333300")
        self.login_button.pack()

        self.start_button = Button(self.root, text="Start TEST", command=self.start_quiz, font="calibre 17 bold")
        self.next_button = Button(self.root, text="Next Question", command=self.next_question, font="calibre 17 bold", fg="#339933")

    def welcome(self):
        Label(self.f1, text="Welcome to IQ test",
              font="arial 30 bold", padx=20, pady=10).pack()

    def is_entry_empty(self, entry):
        return entry.get() == ""


    def login(self):
        if not self.is_entry_empty(self.name_entry) and not self.is_entry_empty(self.age_entry):
            if self.validate_age():
                self.login_frame.pack_forget()
                self.start_quiz_page()
        else:
            Label(self.login_frame, text="Please enter a valid Username and age.", font="consolas 12", fg="red").pack()

    def validate_age(self):
        try:
            age = int(self.age_entry.get())
            if 4 <= age <= 98:
                return True
            else:
                Label(self.login_frame, text="Please enter a valid age between 4 and 98.", font="consolas 12", fg="red").pack()
                return False
        except ValueError:
            Label(self.login_frame, text="Please enter a valid age.", font="consolas 12", fg="red").pack()
            return False

    def start_quiz_page(self):
        self.f1.pack(side=TOP, fill=X)
        self.start_button.pack(pady=170)

    def start_quiz(self):
        name = self.name_entry.get()
        age = int(self.age_entry.get())
        self.c.execute("INSERT INTO users (name, age, score) VALUES (?, ?, 0)", (name, age))
        self.conn.commit()
        self.start_button.pack_forget()
        self.next_button.pack()
        self.next_question()

    def calculate_iq_level(self, percentage_score):
        if percentage_score > 90:
            return "Very Superior"
        elif 80 <= percentage_score <= 90:
            return "Superior"
        elif 70 <= percentage_score <= 80:
            return "High Average"
        elif 50 <= percentage_score <= 70:
            return "Average"
        elif 40 <= percentage_score <= 50:
            return "Low Average"
        elif 30 <= percentage_score <= 40:
            return "Borderline"
        else:
            return "Intellectual Disability"

    def next_question(self):
        if self.current_question < len(question):
            self.check_ans()
            self.user_ans.set('None')
            current_question_text = list(question.keys())[self.current_question]
            self.clear_frame()
            Label(self.f1, text=f"Q) {current_question_text}", padx=12,
                  font="arial 23 bold", fg="#003300").pack(anchor=NW)
            for option in question[current_question_text]:
                Radiobutton(self.f1, text=option, variable=self.user_ans,
                            value=option, padx=28, font="arial 23 normal", fg="#999966").pack(anchor=NW)
            self.current_question += 1
        else:
            self.next_button.forget()
            self.check_ans()
            self.clear_frame()
            total_questions = len(question)
            output = f"{self.name_entry.get()} your Score is {self.user_score.get()} out of {total_questions}"
            percentage_score = (self.user_score.get() / total_questions) * 100
            iq_level = self.calculate_iq_level(percentage_score)
            
            Label(self.f1, text=output, font="Times 30 bold",fg = "blue").pack()
            Label(self.f1, text=f"\n\nYour IQ Level is: \n\n{iq_level}", font="Helvetica 20 bold italic").pack()
            Label(self.f1, text="\n\nThanks for Participating", font="Times 30 bold").pack()


    def check_ans(self):
        temp_ans = self.user_ans.get()
        if temp_ans != 'None' and temp_ans == ans[self.current_question - 1]:
            self.user_score.set(self.user_score.get() + 1)
            user_id = self.c.lastrowid
            self.c.execute("UPDATE users SET score = ? WHERE id = ?", (self.user_score.get(), user_id))
            self.conn.commit()

    def clear_frame(self):
        for widget in self.f1.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = Tk()
    app = QuizApp(root)
    root.mainloop()
