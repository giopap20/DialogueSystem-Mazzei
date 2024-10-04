import spacy
from nltk.corpus import wordnet
import nltk

# Carica il modello di spaCy per l'inglese
nlp = spacy.load('en_core_web_trf')


# Funzione per analizzare l'input utente con spaCy
def parse_input(user_input):
    doc = nlp(user_input)
    return [token.lemma_ for token in doc if not token.is_stop]


# Funzione per controllare se una parola è sinonimo di una keyword
def is_synonym(word, keyword):
    synonyms = set()
    for syn in wordnet.synsets(keyword):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return word in synonyms


# Funzione per valutare l'input dell'utente confrontandolo con le keyword
def evaluate_answer(user_input, keywords):
    tokens = parse_input(user_input)
    matched_keywords = []
    for token in tokens:
        for keyword in keywords:
            if token == keyword or is_synonym(token, keyword):
                matched_keywords.append(keyword)
                break

    completeness_score = len(matched_keywords) / len(keywords)
    is_correct = completeness_score == 1.0
    is_partially_correct = 0 < completeness_score < 1.0

    return {
        "matched_keywords": matched_keywords,
        "keywords": keywords,
        "completeness_score": completeness_score,
        "is_correct": is_correct,
        "is_partially_correct": is_partially_correct
    }

