from analysis.language_understanding import evaluate_answer
from generation.response_generation import greetings, intro, grammar_not_valid, response_correct, next_question, \
    partial_correct_response, try_again, no_more_retries, incorrect_response
from dm.frames import Frame
from db.tln_dictionary import questions


class DialogManager:
    def __init__(self):
        self.questions = None
        self.scores = []
        self.frame = Frame()
        self.current_question_index = 0

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
        evaluation = evaluate_answer(user_input, self.frame.correct_answer, self.frame.questions_type, self.frame.keywords)

        # Punteggio iniziale
        score = 30
        # Se la risposta è grammaticalmente errata
        if not evaluation["check_grammar"]:
            return grammar_not_valid()

        # Se la risposta è corretta
        if evaluation["final_similarity"] >= 0.8:
            self.scores.append(score)  # Punteggio pieno
            self.frame.retries = 0
            self.current_question_index += 1
            if self.current_question_index == len(self.frame.questions):
                return response_correct()
            else:
                return response_correct() + " " + next_question()

        # Se la risposta è parzialmente errata
        self.frame.retries += 1
        if  0.6 <= evaluation["final_similarity"] < 0.8 :
            score -= 2 * self.frame.retries  # Penalità progressiva
            if self.frame.retries == 2:  # Troppi tentativi
                self.scores.append(max(15, score))  # Valuta la risposta corrente
                self.current_question_index += 1
                self.frame.retries = 0
                return partial_correct_response() + " " + no_more_retries()
            else:
                return partial_correct_response() + " " + try_again()
        else:  # Risposta errata
            score -= 5 * self.frame.retries  # Penalità progressiva
            if self.frame.retries == 2:  # Troppi tentativi
                self.scores.append(max(15, score))  # Valuta la risposta corrente
                self.current_question_index += 1
                self.frame.retries = 0  # Reset dei retries
                return incorrect_response() + " " + no_more_retries()

        # Assicurati che il punteggio non scenda sotto 15
        final_score = max(15, score)
        self.scores.append(final_score)

        return incorrect_response() + " " + try_again()


    def calculate_final_score(self):
        if self.scores:
            average_score = (sum(self.scores) / len(self.scores))
            if average_score == 30:
                return 32  # Assegna la lode se il punteggio medio è 30
            return average_score
        return 0

    def has_more_questions(self):
        return self.current_question_index < 3

