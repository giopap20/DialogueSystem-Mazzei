import string

import spacy
import re

from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import wordnet, stopwords, words
import Levenshtein as lev
from sympy.physics.units import length

nlp = spacy.load('en_core_web_lg')

stop = stopwords.words('english')
punct = string.punctuation + '’'
lemmatizer = WordNetLemmatizer()

def clean_input(text):
    # Rimuovi numeri e punteggiatura
    text = re.sub(r'[^\w\s]', '', text)
    # Rimuovi numeri
    text = re.sub(r'\d+', '', text)
    # Rimuovi spazi multipli
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def check_english(sentence):
    sentence = [lemmatizer.lemmatize(word) for word in word_tokenize(sentence.lower()) if word not in punct]
    bools = [word in words.words() for word in sentence]
    return (sum(bools) / len(bools)) > 0.5

def check_grammar(user_input):
    doc = nlp(user_input)

    has_subject = any(token.dep_ == 'nsubj' for token in doc)
    has_verb = any(token.dep_ == 'ROOT' for token in doc)
    # has_object = any(token.dep_ in ['dobj', 'pobj'] for token in doc)
    # has_adverbs = any(token.pos_ == 'ADV' for token in doc)
    # has_prepositions = any(token.dep_ == 'prep' for token in doc)

    is_grammatically_valid = (
            has_subject and
            has_verb
           # (has_object or has_adverbs or has_prepositions)
    )

    return is_grammatically_valid


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
    final_similarity = 0.5 * semantic_similarity + 0.5 * syntactic_similarity
    return final_similarity

def preprocess_text(text):
    text = re.sub(r'\b(and|or)\b', ',', text)
    return text

def extract_keywords(text):
    text = preprocess_text(text)
    doc = nlp(text)

    noun_chunks = [" ".join([lemmatize_with_pos(token) for token in chunk]) for chunk in doc.noun_chunks]
    keywords = [lemmatize_with_pos(token) for token in doc if token.text.lower() not in stop and token.text not in punct]
    combined_keywords = noun_chunks + keywords
    return combined_keywords

def keyword_match(user_input, keywords):
    user_keywords = set(extract_keywords(user_input))
    matches = [kw for kw in user_keywords if kw in keywords]
    total_keywords = len(keywords)

    keyword_similarity = len(matches) / total_keywords
    return keyword_similarity


def lemmatize_with_pos(token):
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
        return token.text


def evaluate_answer(self):
    user_input_cleaned = clean_input(self.frame.user_answer[-1].lower())
    correct_answer_cleaned = clean_input(self.frame.correct_answer.lower())
    is_english = check_english(user_input_cleaned)

    if len(self.frame.user_answer) > 1 and self.frame.user_answer[-1] == self.frame.user_answer[-2]:
        return {
            "same_answer": True,
            "is_english": is_english,
        }

    if self.frame.questions_type == 'list':
       keyword_similarity = keyword_match(self.frame.user_answer[-1], self.frame.keywords)
       return {
           "final_similarity": keyword_similarity,
           "is_english": is_english,
           "check_grammar": True,
           "same_answer": False
         }

    semantic_similarity = calculate_semantic_similarity(user_input_cleaned, correct_answer_cleaned)
    #print(semantic_similarity)

    syntactic_similarity = calculate_syntactic_similarity(user_input_cleaned, correct_answer_cleaned)
    #print(syntactic_similarity)

    final_similarity = combined_similarity(semantic_similarity, syntactic_similarity)
    #print(final_similarity)


    return {
        "same_answer": False,
        "semantic_similarity": semantic_similarity,
        "syntactic_similarity": syntactic_similarity,
        "final_similarity": final_similarity,
        "is_english": is_english,
        "check_grammar": check_grammar(user_input_cleaned) if self.frame.questions_type == 'definition' else True
    }
