import json
from src.classes import MinimalSearchResults, MinimalSource


def load_answered_question():
    files = [
        "./datasets_public/public/AnsweredQuestions/dataset_code_public.json",
        "./datasets_public/public/AnsweredQuestions/dataset_docs_public.json"
    ]
    try:
        answered_questions = []
        code = []
        docs = []
        with open(files[0], "r") as f:
            code = json.load(f)
        with open(files[1], "r") as f:
            docs = json.load(f)
        fill_questions(answered_questions, code, docs)
        return answered_questions
    except (FileNotFoundError, PermissionError, Exception) as e:
        print(e)
        return []


def fill_questions(answered_questions, code, docs):
    for question in code["rag_questions"]:
        answered_questions.append(
            MinimalSearchResults(
                question_id=question["question_id"],
                question=question["question"],
                retrieved_sources=[
                    MinimalSource(
                        file_path=question["sources"][0]["file_path"],
                        first_character_index=question["sources"][0]["first_character_index"],
                        last_character_index=question["sources"][0]["last_character_index"],
                        text=""
                    )
                ]
            )
        )
    for question in docs["rag_questions"]:
        answered_questions.append(
            MinimalSearchResults(
                question_id=question["question_id"],
                question=question["question"],
                retrieved_sources=[
                    MinimalSource(
                        file_path=question["sources"][0]["file_path"],
                        first_character_index=question["sources"][0]["first_character_index"],
                        last_character_index=question["sources"][0]["last_character_index"],
                        text=""
                    )
                ]
            )
        )
