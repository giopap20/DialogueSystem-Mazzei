from dm.frames import PosTaggingFrame, TokenizationFrame, NamedEntityRecognitionFrame
from simplenlg.realiser.english import Realiser
from simplenlg.framework import NLGFactory


realiser = Realiser()
nlgFactory = NLGFactory()


def generate_feedback(evaluation, retries, is_last_question=False):
    # Creazione della frase con SimpleNLG
    phrase = nlgFactory.createClause()

    if evaluation["is_correct"]:
        phrase.setSubject("Your answer")
        phrase.setVerb("is")
        phrase.setObject("completely correct")
    elif evaluation["is_partially_correct"]:
        phrase.setSubject("Your answer")
        phrase.setVerb("is")
        phrase.setObject("partially correct")
        phrase.addComplement("but it could be improved")
    else:
        phrase.setSubject("Your answer")
        phrase.setVerb("is")
        phrase.setObject("incorrect")
        phrase.addComplement("please try again")

    # Debugging: Print the phrase components
    print(f"Subject: {phrase.getSubject()}")
    print(f"Verb: {phrase.getVerb()}")
    print(f"Object: {phrase.getObject()}")

    return realiser.realiseSentence(phrase)


def generate_adaptive_help(retries):
    if retries == 1:
        return "Here's a hint: Think about the main techniques involved."
    elif retries == 2:
        return "Consider reviewing the key concepts of the topic."
    return ""

def generate_sentence_plan(frame):
    """
    Genera un piano di frase basato sui frame.
    Questo può essere utilizzato per personalizzare ulteriormente la risposta.
    """
    sentence_plan = []
    if isinstance(frame, PosTaggingFrame):
        sentence_plan = [
            "What is the technique for POS tagging?",
            "Can you explain the categories involved?",
            "How do you perform disambiguation?"
        ]
    elif isinstance(frame, TokenizationFrame):
        sentence_plan = [
            "What does segmentation mean in tokenization?",
            "Can you describe the different units used?"
        ]
    elif isinstance(frame, NamedEntityRecognitionFrame):
        sentence_plan = [
            "What methods can be used to identify entities?",
            "How do you classify names, places, and organizations?"
        ]
    return sentence_plan
