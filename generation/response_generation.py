from dm.frames import PosTaggingFrame, TokenizationFrame, NamedEntityRecognitionFrame

def generate_response(evaluation, retries, is_last_question=False):
    if not evaluation["matched_keywords"]:
        return "I'm sorry, I didn't quite understand your answer. Please try to include the relevant key points."
    elif evaluation["is_correct"]:
        return "Correct! You covered all the necessary points." + ("" if is_last_question else " Let's move on to the next question.")
    elif evaluation["is_partially_correct"]:
        help_message = generate_adaptive_help(retries)
        return f"Partially correct. Your answer is incomplete. {help_message}"
    else:
        return f"Incorrect. Try to include details about: {', '.join(evaluation['keywords'])}."

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
