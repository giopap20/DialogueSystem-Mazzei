from analysis.language_understanding import evaluate_answer
from generation.response_generation import greetings, intro, grammar_not_valid, response_correct, next_question, \
    partial_correct_response, try_again, no_more_retries, incorrect_response, same_answer
from dm.frames import Frame
from db.tln_dictionary import questions


class DialogManager:
    def __init__(self):
        self.questions = None
        self.scores = []
        self.frame = Frame()
        self.current_question_index = 0
        self.current_question_score = 30

    def first_interaction(self):
        if self.frame.get_student_name() == "" :
            return greetings()
        else:
            return self.frame.get_student_name() + ", " + intro()

    def ask_question(self):
        if self.current_question_index < len(self.frame.questions):
            current_question = self.frame.get_questions(self.current_question_index)
            self.frame.correct_answer = questions[current_question]["correct_answer"]
            self.frame.questions_type = questions[current_question]["type"]
            self.frame.keywords = questions[current_question]["keywords"]
            return current_question
        return None

    def process_answer(self, user_input):
        # Valuta la risposta dell'utente
        self.frame.user_answer.append(user_input)
        evaluation = evaluate_answer(self)

        if evaluation["same_answer"]:
            return same_answer()

        # Se la risposta è grammaticalmente errata
        if not evaluation["check_grammar"]:
            return grammar_not_valid()

        # Se la risposta è corretta
        if evaluation["final_similarity"] >= 0.8:
            self.scores.append(self.current_question_score)  # Punteggio pieno
            self.frame.retries = 0
            self.current_question_index += 1
            self.current_question_score = 30  # Reset del punteggio
            if self.current_question_index == len(self.frame.questions):
                return response_correct()
            else:
                return response_correct() + " " + next_question()

        # Se la risposta è parzialmente errata
        self.frame.retries += 1
        if  (0.6 <= evaluation["final_similarity"] < 0.8 and self.frame.questions_type == 'definition') or (evaluation["final_similarity"] > 0 and self.frame.questions_type == 'list'):
            self.current_question_score -= 3 * self.frame.retries  # Penalità progressiva
            if self.frame.retries == 2:  # Troppi tentativi
                self.scores.append(self.current_question_score)  # Valuta la risposta corrente
                self.current_question_index += 1
                self.frame.retries = 0
                self.current_question_score = 30
                return partial_correct_response() + " " + no_more_retries()
            else:
                return partial_correct_response() + " " + try_again() if self.current_question_index < len(self.frame.questions) else partial_correct_response()
        else:  # Risposta errata
            self.current_question_score -= 6 * self.frame.retries  # Penalità progressiva
            if self.frame.retries == 2:  # Troppi tentativi
                self.scores.append(self.current_question_score)  # Valuta la risposta corrente
                self.current_question_index += 1
                self.frame.retries = 0
                self.current_question_score = 30
                return incorrect_response() + " " + no_more_retries()

        return incorrect_response() + " " + try_again() if self.current_question_index < len(self.frame.questions) else incorrect_response()


    def calculate_final_score(self):
        print(self.scores)
        if self.scores:
            average_score = int((sum(self.scores) / len(self.scores)))
            if average_score == 30:
                return 32  # Assegna la lode se il punteggio medio è 30
            return average_score
        return 0

    def has_more_questions(self):
        return self.current_question_index < 3

