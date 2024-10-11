import random

from db.tln_dictionary import questions


class Frame:
    def __init__(self) -> None:
        self.student_name = ""
        self.retries = 0
        self.questions = random.sample(list(questions.keys()), 3)
        self.questions_type = ""
        self.correct_answer = []
        self.keywords = []


    def set_student_name(self, student_name):
        self.student_name = student_name

    def set_retries(self, retries):
        self.retries = retries

    def set_answer(self, correct_answer):
        self.correct_answer = correct_answer

    def get_answer(self):
        return self.correct_answer

    def get_student_name(self):
        return self.student_name

    def get_retries(self):
        return self.retries

    def get_questions(self, current_index):
        return self.questions[current_index]




