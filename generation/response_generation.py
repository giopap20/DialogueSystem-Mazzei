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
    coord.setConjunction(", ")
    coord.addCoordinate(s_1)
    coord.addCoordinate(s_2)

    output = realiser.realiseSentence(coord)
    return output

def intro():
    subj_1 = nlg_factory.createNounPhrase("I")
    verb_1 = nlg_factory.createVerbPhrase("ask")
    obj_1 = nlg_factory.createNounPhrase("some", "questions")
    prep_1 = nlg_factory.createPrepositionPhrase("about", "NLP")


    verb_1.setFeature(nlg.Feature.TENSE, nlg.Tense.FUTURE)
    s_1 = nlg_factory.createClause(subj_1, verb_1, "you")
    s_1.addComplement(obj_1)
    s_1.addComplement(prep_1)
    s_2 = nlg_factory.createClause("you", "be", "ready?")
    s_2.setFeature(nlg.Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.YES_NO)

    coord = nlg_factory.createCoordinatedPhrase()
    coord.setConjunction(". ")
    coord.addCoordinate(s_1)
    coord.addCoordinate(s_2)
    output = realiser.realiseSentence(coord)
    output = output.replace(". are", ". Are")
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


def partial_correct_response():
    subj_1 = nlg_factory.createNounPhrase("your", "answer")
    verb_1 = nlg_factory.createVerbPhrase("be")
    obj_1 = nlg_factory.createNounPhrase("partially correct")
    s_1 = nlg_factory.createClause(subj_1, verb_1, obj_1)


    subj_2 = nlg_factory.createNounPhrase("the", "answer")
    verb_2 = nlg_factory.createVerbPhrase("be")
    obj_2 = nlg_factory.createNounPhrase("only partially correct")
    s_2 = nlg_factory.createClause(subj_2, verb_2, obj_2)
    s_2.setFrontModifier("Not bad, but")


    subj_3 = nlg_factory.createNounPhrase("the", "answer")
    verb_3 = nlg_factory.createVerbPhrase("be")
    obj_3 = nlg_factory.createNounPhrase("partially", "right")
    s_3 = nlg_factory.createClause(subj_3, verb_3, obj_3)
    s_3.setFrontModifier("You're close, but")


    subj_4 = nlg_factory.createNounPhrase("the", "answer")
    verb_4 = nlg_factory.createVerbPhrase("be")
    verb_4.setFeature(Feature.NEGATED, True)
    obj_4 = nlg_factory.createNounPhrase("fully correct")
    s_4 = nlg_factory.createClause(subj_4, verb_4, obj_4)
    s_4.setFrontModifier("Good attempt, but")


    sentences = [
        realiser.realiseSentence(s_1),
        realiser.realiseSentence(s_2),
        realiser.realiseSentence(s_3),
        realiser.realiseSentence(s_4)
    ]


    return random.choice(sentences)


def incorrect_response():

    subj_1 = nlg_factory.createNounPhrase("your", "answer")
    verb_1 = nlg_factory.createVerbPhrase("be")
    obj_1 = nlg_factory.createNounPhrase("incorrect")
    s_1 = nlg_factory.createClause(subj_1, verb_1, obj_1)


    subj_2 = nlg_factory.createNounPhrase("that")
    verb_2 = nlg_factory.createVerbPhrase("be")
    obj_2 = nlg_factory.createNounPhrase("not the right answer")
    s_2 = nlg_factory.createClause(subj_2, verb_2, obj_2)
    s_2.setFrontModifier("Unfortunately")


    subj_3 = nlg_factory.createNounPhrase("that")
    verb_3 = nlg_factory.createVerbPhrase("be")
    obj_3 = nlg_factory.createNounPhrase("wrong")
    s_3 = nlg_factory.createClause(subj_3, verb_3, obj_3)
    s_3.setFrontModifier("I'm sorry, but")


    subj_4 = nlg_factory.createNounPhrase("that")
    verb_4 = nlg_factory.createVerbPhrase("be")
    obj_4 = nlg_factory.createNounPhrase("incorrect")
    s_4 = nlg_factory.createClause(subj_4, verb_4, obj_4)
    s_4.setFrontModifier("No")

    # Lista di tutte le frasi
    sentences = [
        realiser.realiseSentence(s_1),
        realiser.realiseSentence(s_2),
        realiser.realiseSentence(s_3),
        realiser.realiseSentence(s_4)
    ]

    # Seleziona una frase casualmente
    return random.choice(sentences)


def failed_exam():
    subj_1 = nlg_factory.createNounPhrase("you")
    verb_1 = nlg_factory.createVerbPhrase("need")
    obj_1 = nlg_factory.createVerbPhrase("study")
    obj_1.addComplement("more")
    verb_1.addComplement(obj_1)
    s_1 = nlg_factory.createClause(subj_1, verb_1)

    subj_2 = nlg_factory.createNounPhrase("you")
    verb_2 = nlg_factory.createVerbPhrase("do")
    verb_2.addComplement("better")
    verb_2.setFeature(Feature.TENSE, "future")
    s_2 = nlg_factory.createClause(subj_2, verb_2)
    s_2.setFrontModifier("Next time")

    coord = nlg_factory.createCoordinatedPhrase()
    coord.setConjunction(". ")
    coord.addCoordinate(s_1)
    coord.addCoordinate(s_2)
    output = realiser.realiseSentence(coord)

    return output

def passed_exam():
    subj_1 = nlg_factory.createNounPhrase("you")
    verb_1 = nlg_factory.createVerbPhrase("do")
    verb_1.setFeature(Feature.TENSE, "past")
    verb_1.addComplement("well")
    s_1 = nlg_factory.createClause(subj_1, verb_1)


    subj_2 = nlg_factory.createNounPhrase("you")
    verb_2 = nlg_factory.createVerbPhrase("can")


    aim_verb = nlg_factory.createVerbPhrase("aim")
    aim_verb.setFeature(Feature.FORM, "base")

    verb_2.addComplement(aim_verb)
    aim_verb.addComplement("higher")

    s_2 = nlg_factory.createClause(subj_2, verb_2)

    coord = nlg_factory.createCoordinatedPhrase()
    coord.setConjunction("but")
    coord.addCoordinate(s_1)
    coord.addCoordinate(s_2)

    output = realiser.realiseSentence(coord)

    return output

def good_exam():
    subj = nlg_factory.createNounPhrase("you")
    verb = nlg_factory.createVerbPhrase("do")
    verb.setFeature(Feature.TENSE, "past")
    verb.addComplement("great")
    s = nlg_factory.createClause(subj, verb)

    return realiser.realiseSentence(s)

def best_exam():
    subj_1 = nlg_factory.createNounPhrase("I")
    verb_1 = nlg_factory.createVerbPhrase("have")
    obj_1 = nlg_factory.createNounPhrase("some", "thesis projects")
    s_1 = nlg_factory.createClause(subj_1, verb_1, obj_1)

    prep = nlg_factory.createPrepositionPhrase("for", "you")
    verb_2 = nlg_factory.createVerbPhrase("work")
    verb_2.addComplement("on")
    prep.addComplement(verb_2)

    if_clause = nlg_factory.createClause("you", "want")
    if_clause.setFeature(Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.YES_NO)
    s_1.addPostModifier(prep)
    s_1.addPostModifier(if_clause)

    return realiser.realiseSentence(s_1)


def try_again():
    verb_2 = nlg_factory.createVerbPhrase("try")
    verb_2.addComplement("again")
    verb_2.setFeature(Feature.FORM, "imperative")
    s_2 = nlg_factory.createClause()
    s_2.setVerb(verb_2)
    output = realiser.realiseSentence(s_2)

    return output

def next_question():
    verb = nlg_factory.createVerbPhrase("move")
    prep_phrase = nlg_factory.createPrepositionPhrase("to", "the next question")
    verb.addComplement(prep_phrase)
    s = nlg_factory.createClause()
    s.setSubject("let us")
    s.setVerb(verb)

    return realiser.realiseSentence(s)

def no_more_retries():
    subj = nlg_factory.createNounPhrase("we")
    modal = nlg_factory.createVerbPhrase("should")
    verb = nlg_factory.createVerbPhrase("try")
    verb.setFeature(Feature.FORM, "base")
    obj = nlg_factory.createNounPhrase("another", "question")
    verb.addComplement(obj)
    modal.addComplement(verb)
    s = nlg_factory.createClause(subj, modal)
    s.setFrontModifier("Maybe")

    return realiser.realiseSentence(s)


def same_answer():
    subj = nlg_factory.createNounPhrase("you")
    verb = nlg_factory.createVerbPhrase("say")
    verb.setFeature(Feature.TENSE, "past")  # Passato
    obj = nlg_factory.createNounPhrase("that")

    s = nlg_factory.createClause(subj, verb, obj)
    s.addComplement(nlg_factory.createAdverbPhrase("already"))

    return realiser.realiseSentence(s)


