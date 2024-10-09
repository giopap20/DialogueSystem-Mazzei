import simplenlg as nlg
from simplenlg import Feature, Form, InterrogativeType
from simplenlg.features import Tense
from simplenlg.lexicon import Lexicon
from sympy.strategies.core import switch

from simplenlg.realiser.english import Realiser
from simplenlg.framework import NLGFactory, LexicalCategory
import random


lexicon = Lexicon.getDefaultLexicon()
nlg_factory = NLGFactory(lexicon)
realiser = Realiser(lexicon)
used_responses = []


def greetings():
    verb_1 = nlg_factory.createVerbPhrase("be")
    subj_1 = nlg_factory.createNounPhrase("I")
    obj_1 = nlg_factory.createNounPhrase("prof", "Danny")
    s_1 = nlg_factory.createClause(subj_1, verb_1, obj_1)
    s_1.setFrontModifier("Hi,")

    verb = nlg_factory.createVerbPhrase("be")
    subj = nlg_factory.createNounPhrase("your", "name?")
    s_2 = nlg_factory.createClause(subj, verb)
    s_2.setFeature(nlg.Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.WHAT_OBJECT)

    coord = nlg_factory.createCoordinatedPhrase()
    coord.setConjunction(",")
    coord.addCoordinate(s_1)
    coord.addCoordinate(s_2)

    output = realiser.realiseSentence(coord)
    return output

def intro():
    subj_1 = nlg_factory.createNounPhrase("I") # // Soggetto
    verb_1 = nlg_factory.createVerbPhrase("ask") # Verbo
    obj_1 = nlg_factory.createNounPhrase("some", "questions") # Complemento
    prep_1 = nlg_factory.createPrepositionPhrase("about", "NLP") # Preposizione


    verb_1.setFeature(nlg.Feature.TENSE, nlg.Tense.FUTURE)
    s_1 = nlg_factory.createClause(subj_1, verb_1, "you")
    s_1.addComplement(obj_1)
    s_1.addComplement(prep_1)
    s_2 = nlg_factory.createClause("you", "be", "ready?")  #Frase interrogativa
    s_2.setFeature(nlg.Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.YES_NO)

    coord = nlg_factory.createCoordinatedPhrase()
    coord.setConjunction(".")
    coord.addCoordinate(s_1)
    coord.addCoordinate(s_2)
    output = realiser.realiseSentence(coord)
    return output

def grammar_not_valid():
    subj_1 = nlg_factory.createNounPhrase("Your", "answer")
    verb_1 = nlg_factory.createVerbPhrase("be")
    obj_1 = nlg_factory.createNounPhrase("not", "grammatically valid")
    s_1 = nlg_factory.createClause(subj_1, verb_1, obj_1)
    output = realiser.realiseSentence(s_1)

    return output

def response_correct():
    # Crea la prima frase: "Great! Your answer is correct."
    subj_1 = nlg_factory.createNounPhrase("your", "answer")
    verb_1 = nlg_factory.createVerbPhrase("be")
    obj_1 = nlg_factory.createNounPhrase("correct")
    s_1 = nlg_factory.createClause(subj_1, verb_1, obj_1)
    s_1.setFrontModifier("Great!")

    # Crea la seconda frase: "Well done! You gave the right answer."
    subj_2 = nlg_factory.createNounPhrase("you")
    verb_2 = nlg_factory.createVerbPhrase("give")
    verb_2.setFeature(nlg.Feature.TENSE, nlg.Tense.PAST)
    obj_2 = nlg_factory.createNounPhrase("the right", "answer")
    s_2 = nlg_factory.createClause(subj_2, verb_2, obj_2)
    s_2.setFrontModifier("Well done!")

    # Crea la terza frase: "Correct! You did a great job."
    subj_3 = nlg_factory.createNounPhrase("you")
    verb_3 = nlg_factory.createVerbPhrase("do")
    verb_3.setFeature(nlg.Feature.TENSE, nlg.Tense.PAST)
    obj_3 = nlg_factory.createNounPhrase("a great", "job")
    s_3 = nlg_factory.createClause(subj_3, verb_3, obj_3)
    s_3.setFrontModifier("Correct!")

    # Crea la quarta frase: "Yes, that's the right answer!"
    subj_4 = nlg_factory.createNounPhrase("that")
    verb_4 = nlg_factory.createVerbPhrase("be")
    obj_4 = nlg_factory.createNounPhrase("the right", "answer")
    s_4 = nlg_factory.createClause(subj_4, verb_4, obj_4)
    s_4.setFrontModifier("Yes,")

    # Lista di tutte le frasi
    sentences = [
        realiser.realiseSentence(s_1),
        realiser.realiseSentence(s_2),
        realiser.realiseSentence(s_3),
        realiser.realiseSentence(s_4)
    ]
    # Seleziona una frase casualmente
    return random.choice(sentences)


def next_question():
    verb = nlg_factory.createVerbPhrase("move")  # Verbo: "move"
    prep_phrase = nlg_factory.createPrepositionPhrase("to", "the next question")  # Preposizione: "to the next question"

    # Aggiungi la preposizione al verbo
    verb.addComplement(prep_phrase)

    # Crea il soggetto implicito "Let's"
    s = nlg_factory.createClause()
    s.setSubject("let us")
    s.setVerb(verb)

    # Realizza la frase
    return realiser.realiseSentence(s)




def generate_adaptive_help(retries):
    if retries == 1:
        return "Here's a hint: Think about the main techniques involved."
    elif retries == 2:
        return "Consider reviewing the key concepts of the topic."
    return ""
