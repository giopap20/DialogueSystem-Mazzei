from dm.dialog_manager import DialogManager


def main():
    dm = DialogManager()

    print("Welcome to the NLP Quiz!")

    while dm.has_more_questions():
        question = dm.ask_question()
        print(f"Prof: {question}")

        user_input = input("Student: ")

        response = dm.process_answer(user_input)
        print(response)

    final_score = dm.calculate_final_score()
    if final_score.isnumeric():
        if final_score < 18:
            print(f"Your final score is: {final_score:.2f}, You need to study more. Next time you will do better.")
        elif 19 < final_score < 25:
            print(f"Your final score is: {final_score:.2f}, You did well but you can aim higher.")
        elif final_score > 25:
            print(f"Your final score is: {final_score:.2f}, You did great!")
    else:
        print(f"Your final score is: {final_score}, I have some thesis projects for you to work on if you want.")



if __name__ == "__main__":
    main()
