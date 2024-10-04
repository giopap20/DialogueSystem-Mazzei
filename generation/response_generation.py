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

