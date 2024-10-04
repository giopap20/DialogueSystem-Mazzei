from analysis.language_understanding import evaluate_answer
from generation.response_generation import generate_response
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
            keywords = questions_with_keywords[current_question]
            explain_question(keywords)
            return current_question
        return None

    def process_answer(self, user_input):
        current_question = self.questions[self.current_question_index]
        keywords = questions_with_keywords[current_question]

        if current_question == "What is POS tagging?":
            frame = PosTaggingFrame()
        elif current_question == "What is tokenization in NLP?":
            frame = TokenizationFrame()
        elif current_question == "What are named entity recognitions?":
            frame = NamedEntityRecognitionFrame()

        self.frames.append(frame)

        evaluation = evaluate_answer(user_input, keywords)
        response = generate_response(evaluation, self.retries, self.current_question_index == len(self.questions) - 1)

        score = 30  # Iniziamo da un punteggio di 30


        if evaluation["is_correct"]:
            self.retries = 0
            self.current_question_index += 1
            if self.current_question_index == len(self.questions):  # Controllo se è l'ultima domanda
                return response  # Restituisce solo il messaggio di correttezza
        elif evaluation["is_partially_correct"]:
            self.retries += 1
            score -= 2  # Penalità per tentativo parzialmente corretto
            if self.retries > self.max_retries:  # Se i retries superano il massimo
                response = f"Too many attempts. Let's try another question."
                self.current_question_index += 1
                self.retries = 0  # Reset dei retries dopo la valutazione
        else:
            score -= 5  # Penalità per risposta sbagliata

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
