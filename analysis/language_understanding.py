import string

import spacy
import re

from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import wordnet, stopwords, words
import Levenshtein as lev
from rapidfuzz.distance.Levenshtein_py import similarity

from db.tln_dictionary import questions

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

    if all([token.has_vector for token in doc1]) and all([token.has_vector for token in doc2]):
        similarity = doc1.similarity(doc2)
    else:
        similarity = 0

    return similarity

def calculate_syntactic_similarity(answer, reference):
    return 1 - lev.distance(answer, reference) / max(len(answer), len(reference))

def combined_similarity(semantic_similarity, syntactic_similarity):
    # Pondera i punteggi come desideri; ad esempio, dando più peso alla similarità semantica
    final_similarity = 0.5 * semantic_similarity + 0.5 * syntactic_similarity
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


    # Definisci una condizione di validità grammaticale basata su soggetto, verbo, e altre dipendenze
    is_grammatically_valid = (
            has_subject and
            has_verb and
            (has_object or has_adverbs or has_prepositions)
    )

    return is_grammatically_valid

def preprocess_text(text):
    text = re.sub(r'\b(and|or)\b', ',', text)
    return text

def extract_keywords(text):
    text = preprocess_text(text)
    doc = nlp(text)

    # Estrai noun chunks come potenziali frasi chiave
    noun_chunks = [" ".join([lemmatize_with_pos(token) for token in chunk]) for chunk in doc.noun_chunks]

    keywords = [lemmatize_with_pos(token) for token in doc if token.text.lower() not in stop and token.text not in punct]
    combined_keywords = noun_chunks + keywords
    return combined_keywords

def keyword_match(user_input, keywords):
    user_keywords = set(extract_keywords(user_input))

    # Trova il numero di parole chiave che coincidono
    matches = [kw for kw in user_keywords if kw in keywords]

    total_keywords = len(keywords)

    # Normalizza il punteggio delle parole chiave
    keyword_similarity = len(matches) / total_keywords
    return keyword_similarity


def lemmatize_with_pos(token):
    # Mappa i tag POS di spaCy ai tag POS di WordNet
    pos = token.pos_
    if pos.startswith('V'):
        return lemmatizer.lemmatize(token.text, wordnet.VERB)
    elif pos.startswith('N'):
        return lemmatizer.lemmatize(token.text, wordnet.NOUN)
    elif pos.startswith('R'):
        return lemmatizer.lemmatize(token.text, wordnet.ADV)
    elif pos.startswith('J'):
        return lemmatizer.lemmatize(token.text, wordnet.ADJ)
    else:
        return token.text  # Restituisce la parola originale se il POS non è utile


# Funzione per valutare l'input dell'utente confrontandolo con le keyword (Text-Plan)
def evaluate_answer(self):

    # Controlla se l'utente ha risposto ugualmente rispetto a prima
    if self.frame.retries > 0 and self.frame.user_answer[-1] == self.frame.user_answer[-2]:
        return {
            "same_answer": True
        }

    # Se la domanda è di tipo "list", confronta le parole chiave
    if self.frame.questions_type == 'list':
       keyword_similarity = keyword_match(self.frame.user_answer[-1], self.frame.keywords)
       return {
           "final_similarity": keyword_similarity if keyword_similarity > 0.6 else 0,
           "check_grammar": True,
           "same_answer": False
         }

    # Pulizia dell'input
    user_input_cleaned = clean_input(self.frame.user_answer[-1].lower())
    correct_answer_cleaned = clean_input(self.frame.correct_answer.lower())

    # Calcola la similarità semantica tra la risposta corretta e quella fornita
    semantic_similarity = calculate_semantic_similarity(user_input_cleaned, correct_answer_cleaned)
    #print(semantic_similarity)

    # Calcola similarità sintattica
    syntactic_similarity = calculate_syntactic_similarity(user_input_cleaned, correct_answer_cleaned)
    #print(syntactic_similarity)

    # Calcola la similarità combinata
    final_similarity = combined_similarity(semantic_similarity, syntactic_similarity)
    #print(final_similarity)


    return {
        "same_answer": False,
        "semantic_similarity": semantic_similarity,
        "syntactic_similarity": syntactic_similarity,
        "final_similarity": final_similarity,
        "check_grammar": check_grammar(user_input_cleaned) if self.frame.questions_type == 'definition' else True
    }
