import string

import spacy
import re

from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import wordnet, stopwords
import Levenshtein as lev

# Carica il modello di spaCy per l'inglese
nlp = spacy.load('en_core_web_md')

stop = stopwords.words('english')
punct = string.punctuation + '’'
lemmatizer = WordNetLemmatizer()

# Funzione per pulire l'input dell'utente
def clean_input(text):
    # Rimuovi numeri e punteggiatura
    text = re.sub(r'[^\w\s]', '', text)
    # Rimuovi numeri
    text = re.sub(r'\d+', '', text)
    # Rimuovi spazi multipli
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Funzione per ottenere i sinonimi di una parola
def get_synonyms(keyword):
    synonyms = set()
    for syn in wordnet.synsets(keyword):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

# Funzione per controllare se una parola è sinonimo di una keyword
def is_synonym(word, keyword):
    return word in get_synonyms(keyword)

# Funzione per controllare la similarità semantica tra due frasi
def calculate_semantic_similarity(user_input, correct_answer):
    doc1 = nlp(user_input)
    doc2 = nlp(correct_answer)

    # Check if tokens have vectors
    print(all([token.has_vector for token in doc1]))
    print(all([token.has_vector for token in doc2]))

    print(doc1)
    print(doc2)

    if all([token.has_vector for token in doc1]) and all([token.has_vector for token in doc2]):
        similarity = doc1.similarity(doc2)
    else:
        similarity = 0

    return similarity

def calculate_syntactic_similarity(answer, reference):
    return 1 - lev.distance(answer, reference) / max(len(answer), len(reference))

def dependency_similarity(answer, reference):
    doc1 = nlp(answer)
    doc2 = nlp(reference)

    # Estrarre le dipendenze
    deps1 = [(token.text, token.dep_) for token in doc1]
    deps2 = [(token.text, token.dep_) for token in doc2]

    # Compara le dipendenze
    return len(set(deps1) & set(deps2)) / float(len(set(deps1) | set(deps2)))

def combined_similarity(semantic_similarity, syntactic_similarity):
    # Pondera i punteggi come desideri; ad esempio, dando più peso alla similarità semantica
    final_similarity = 0.7 * semantic_similarity + 0.3 * syntactic_similarity
    return final_similarity

# Funzione per verificare la struttura grammaticale
def check_grammar(user_input):
    # Utilizza SpaCy per l'analisi grammaticale
    doc = nlp(user_input)

    # Controlli sulle dipendenze principali
    has_subject = any(token.dep_ == 'nsubj' for token in doc)
    has_verb = any(token.dep_ == 'ROOT' for token in doc)
    has_object = any(token.dep_ in ['dobj', 'pobj'] for token in doc)
    has_adverbs = any(token.pos_ == 'ADV' for token in doc)
    has_prepositions = any(token.dep_ == 'prep' for token in doc)

    for token in doc:
        print(token.text, token.dep_, token.pos_, token.head.text)

    # Definisci una condizione di validità grammaticale basata su soggetto, verbo, e altre dipendenze
    is_grammatically_valid = (
            has_subject and
            has_verb and
            (has_object or has_adverbs or has_prepositions)
    )

    print(has_subject, has_verb, has_object, has_adverbs, has_prepositions)
    return is_grammatically_valid


def match_with_flexibility(token, keyword):
    # Crea un pattern per catturare diverse forme della parola (es. run, running, ran)
    keyword_pattern = rf'\b{keyword}(ing|ed|s)?\b'
    return bool(re.search(keyword_pattern, token))

# Funzione per valutare l'input dell'utente confrontandolo con le keyword (Text-Plan)
def evaluate_answer(user_input, correct_answer, question_type):
    # Pulizia dell'input
    user_input_cleaned = clean_input(user_input.lower())
    correct_answer_cleaned = clean_input(correct_answer.lower())

    # Calcola la similarità semantica tra la risposta corretta e quella fornita
    semantic_similarity = calculate_semantic_similarity(user_input_cleaned, correct_answer_cleaned)
    print(semantic_similarity)

    # Calcola similarità sintattica
    syntactic_similarity = calculate_syntactic_similarity(user_input_cleaned, correct_answer_cleaned)
    print(syntactic_similarity)

    # Calcola similarità delle dipendenze
    dep_similarity = dependency_similarity(user_input_cleaned, correct_answer_cleaned)
    print(dep_similarity)

    #Calcola la similarità combinata
    final_similarity = combined_similarity(semantic_similarity, syntactic_similarity)
    print(combined_similarity(semantic_similarity, syntactic_similarity))

    return {
        "semantic_similarity": semantic_similarity,
        "syntactic_similarity": syntactic_similarity,
        "dep_similarity": dep_similarity,
        "final_similarity": final_similarity,
        "check_grammar": check_grammar(user_input_cleaned) if question_type == 'definition' else True
    }
