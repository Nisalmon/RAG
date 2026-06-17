import json
from src.classes import MinimalSearchResults, MinimalSource
from typing import List, Dict, Any


def load_answered_question() -> List[MinimalSearchResults]:
    '''
    BEHAVIOR:
        This function loads all the AnsweredQuestions JSON file.

    RETURN:
        List[MinimalSearchResults]
    '''
    files = [
        "./datasets_public/public/AnsweredQuestions/dataset_code_public.json",
        "./datasets_public/public/AnsweredQuestions/dataset_docs_public.json"
    ]
    try:
        answered_questions: List[MinimalSearchResults] = []
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


def fill_questions(answered_questions: List[MinimalSearchResults],
                   code: Dict[str, Any], docs: Dict[str, Any]) -> None:
    '''
    PARAMETERS:
        answered_questions: List[MinimalSearchResults]. The list to fill.
        code: Dict[str, Any]. The AnsweredQuestion code dataset.
        docs: Dict[str, Any]. The AnsweredQuestion docs dataset.

    BEHAVIOR:
        Fill the given list with AnsweredQuestion object.
    '''
    for question in code["rag_questions"]:
        answered_questions.append(
            MinimalSearchResults(
                question_id=question["question_id"],
                question=question["question"],
                retrieved_sources=[
                    MinimalSource(
                        file_path=question["sources"][0]["file_path"],
                        first_character_index=question["sources"][0]
                        ["first_character_index"],
                        last_character_index=question["sources"][0]
                        ["last_character_index"],
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
                        first_character_index=question["sources"][0]
                        ["first_character_index"],
                        last_character_index=question["sources"][0]
                        ["last_character_index"],
                        text=""
                    )
                ]
            )
        )
