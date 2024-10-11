from dm.dialog_manager import DialogManager
from generation.response_generation import failed_exam, good_exam, best_exam, passed_exam


def main():
    dm = DialogManager()

    if dm.frame.get_student_name() == "":
        print(f"Prof Danny: {dm.first_interaction()}")
        student_name = input("Student: ")
        dm.frame.set_student_name(student_name)

        print(f"Prof Danny: {dm.first_interaction()}")
        answer = input("Student: ").strip().lower()
        if not answer in {"yes", "sure", "ok", "yep", "yeah", "y", "of course", "absolutely", "maybe"}:
            return None


    while dm.has_more_questions():
        question = dm.ask_question()
        print(f"Prof Danny: {question}")

        user_input = input("Student: ")
        response = dm.process_answer(user_input)
        print(f"Prof Danny: {response}")

    final_score = dm.calculate_final_score()
    if final_score < 18:
        print(f"{student_name}, Your final score is: {final_score}" + ". " + failed_exam())
    elif 19 < final_score <= 25:
        print(f"{student_name}, Your final score is: {final_score}" + ". " + passed_exam())
    elif 26 <= final_score > 32:
        print(f"{student_name}, Your final score is: {final_score}" + ". " + good_exam())
    else:
        print(f"{student_name}, Your final score is: 30 e lode" + ". " + best_exam())



if __name__ == "__main__":
    main()
