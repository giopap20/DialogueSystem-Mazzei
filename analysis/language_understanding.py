import spacy
import re
from nltk.corpus import wordnet

# Carica il modello di spaCy per l'inglese
nlp = spacy.load('en_core_web_trf')

# Funzione per analizzare l'input utente con spaCy
def parse_input(user_input):
    doc = nlp(user_input)
    return doc

# Funzione per controllare se una parola è sinonimo di una keyword
def is_synonym(word, keyword):
    synonyms = set()
    for syn in wordnet.synsets(keyword):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return word in synonyms

# Funzione per valutare la struttura della frase rispetto al Sentence-Plan

def evaluate_sentence_plan(doc, sentence_plan):
    subject, verb, object_, modifiers_present = False, False, False, False

    # Controlla la presenza di soggetto, verbo e oggetto
    for token in doc:
        print(f"Token: {token.text}, Dep: {token.dep_}, Lemma: {token.lemma_}")  # Debugging

        # Controlla il soggetto
        if token.dep_ in {"nsubj"}:
            # Controlla il soggetto considerando i lemmi
            subject = token.lemma_.lower() == sentence_plan['subject'].lower()

        # Controlla il verbo
        if token.dep_ == "ROOT":
            verb_variants = [sentence_plan['verb'].lower(), 'be']  # Aggiungi altre forme se necessario
            if token.lemma_.lower() in verb_variants:
                verb = True

        # Controlla l'oggetto
        if token.dep_ in {"dobj", "pobj", "attr"} and token.lemma_.lower() == sentence_plan['object'].lower():
            object_ = True

    # Debugging finale
    print(f"Subject: {subject}, Verb: {verb}, Object: {object_}")

    # Restituisce True solo se soggetto, verbo, oggetto e (se presenti) modificatori sono soddisfatti
    return subject and verb and object_



# Funzione per valutare l'input dell'utente confrontandolo con le keyword (Text-Plan)
def evaluate_answer(user_input, keywords, sentence_plan=None):
    doc = parse_input(user_input)
    tokens = [token.lemma_ for token in doc if not token.is_stop]

    matched_keywords = []
    for token in tokens:
        for keyword in keywords:
            if token == keyword or is_synonym(token, keyword):
                matched_keywords.append(keyword)
                break

    completeness_score = len(matched_keywords) / len(keywords)
    is_correct = completeness_score == 1.0
    is_partially_correct = 0 < completeness_score < 1.0

    # Aggiungi controllo della struttura (Sentence-Plan) se fornito
    sentence_structure_correct = False
    if sentence_plan:
        sentence_structure_correct = evaluate_sentence_plan(doc, sentence_plan)

    print("Matched Keywords:", matched_keywords)
    print("Keywords:", keywords)
    print("Completeness Score:", completeness_score)
    print("sentence structure Correct:", sentence_structure_correct)
    print("Is Partially Correct:", is_partially_correct)
    return {
        "matched_keywords": matched_keywords,
        "keywords": keywords,
        "completeness_score": completeness_score,
        "is_correct": is_correct and sentence_structure_correct,  # Aggiungi struttura grammaticale
        "is_partially_correct": is_partially_correct  # Modificato per usare la variabile esistente
    }
