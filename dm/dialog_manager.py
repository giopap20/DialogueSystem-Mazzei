from analysis.language_understanding import evaluate_answer
from generation.response_generation import generate_feedback
from dm.frames import PosTaggingFrame, TokenizationFrame, NamedEntityRecognitionFrame
from db.tln_dictionary import questions_with_keywords


class DialogManager:
    def __init__(self):
        self.current_question_index = 0
        self.scores = []
        self.questions = list(questions_with_keywords.keys())
        self.frames = []
        self.retries = 0
        self.max_retries = 2  # Massimo numero di tentativi

    def ask_question(self):
        if self.current_question_index < len(self.questions):
            current_question = self.questions[self.current_question_index]
            question_info = questions_with_keywords[current_question]
            explain_question(question_info['keywords'])
            return current_question
        return None

    def process_answer(self, user_input):
        current_question = self.questions[self.current_question_index]
        question_info = questions_with_keywords[current_question]

        # Estrai le keywords e il sentence plan
        keywords = question_info['keywords']
        sentence_plan = question_info['sentence_plan']

        # Crea il frame corretto in base alla domanda
        if current_question == "What is POS tagging?":
            frame = PosTaggingFrame(keywords)
        elif current_question == "What is tokenization in NLP?":
            frame = TokenizationFrame(keywords)
        elif current_question == "What are named entity recognitions?":
            frame = NamedEntityRecognitionFrame(keywords)

        self.frames.append(frame)

        # Valuta la risposta dell'utente
        evaluation = evaluate_answer(user_input, keywords, sentence_plan)
        response = generate_feedback(evaluation, self.retries, self.current_question_index == len(self.questions) - 1)

        # Punteggio iniziale
        score = 30

        if evaluation["is_correct"]:
            self.scores.append(score)  # Punteggio pieno
            self.retries = 0
            self.current_question_index += 1
            if self.current_question_index == len(self.questions):  # Ultima domanda
                return response  # Restituisce solo il messaggio di correttezza
            return response + " Let's move on to the next question."

        # Se la risposta è parzialmente corretta o errata
        self.retries += 1
        if evaluation["is_partially_correct"]:
            score -= 2 * self.retries  # Penalità progressiva
            if self.retries > self.max_retries:  # Troppi tentativi
                response = "Too many attempts. Let's try another question."
                self.scores.append(max(15, score))  # Valuta la risposta corrente
                self.current_question_index += 1
                self.retries = 0  # Reset dei retries
        else:  # Risposta errata
            score -= 5 * self.retries  # Penalità progressiva
            if self.retries > self.max_retries:  # Troppi tentativi
                response = "Too many attempts. Let's try another question."
                self.scores.append(max(15, score))  # Valuta la risposta corrente
                self.current_question_index += 1
                self.retries = 0  # Reset dei retries

        # Assicurati che il punteggio non scenda sotto 15
        final_score = max(15, score)
        self.scores.append(final_score)

        return response

    def calculate_final_score(self):
        if self.scores:
            average_score = sum(self.scores) / len(self.scores)
            if average_score == 30:
                return "30 e lode"  # Assegna la lode se il punteggio medio è 30
            return average_score
        return 0

    def has_more_questions(self):
        return self.current_question_index < len(self.questions)


def explain_question(keywords):
    print("Your answer will be evaluated based on the following key points:")
    print(f"- {', '.join(keywords)}")
