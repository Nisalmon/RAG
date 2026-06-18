from typing import List, Dict, Any
from pathlib import Path
from src.classes import (UnansweredQuestion,
                         MinimalSource,
                         MinimalSearchResults,
                         AnsweredQuestion)
import json


def load_data() -> List[List[Dict[str, str]]]:
    '''
    BEHAVIOR:
        This function loads all the python/markown file in the vllm folder.

    RETURN:
        List[List[Dict[str, str]]]
    '''
    data: List[Any] = [[], []]
    res = Path("../data/raw/vllm-0.10.1")
    for file in res.rglob("*"):
        if file.suffix != ".py" and file.suffix != ".md":
            continue
        tpe = 0 if file.suffix == ".py" else 1
        data[tpe].append({
            "path": str(file.as_posix()),
            "content": file.read_text(encoding="utf-8")
        })
    return data


def load_prompts(file_path: str) -> List[UnansweredQuestion]:
    '''
    PARAMETERS:
        file_path: str

    BEHAVIOR:
        This function load all the UnansweredQuestion stored in the given
        json file_path.

    RETURN:
        List[UnansweredQuestion]
    '''
    prompts = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            all_prompts = json.load(f)
        question = all_prompts['rag_questions']
        for elem in question:
            prompts.append(
                UnansweredQuestion(
                    question_id=elem["question_id"],
                    question=elem["question"]
                )
            )
        return prompts
    except (FileNotFoundError, json.JSONDecodeError):
        print("An error occured")
        return []


def load_single_prompt(prompt: str) -> List[UnansweredQuestion]:
    '''
    PARAMETERS:
        prompt: str

    BEHAVIOR:
        This function return a list containing a single UnansweredQuestion

    RETURN:
        List[UnansweredQuestion]
    '''
    return ([UnansweredQuestion(
        question_id="1",
        question=prompt
    )])


def load_chunks() -> List[MinimalSource]:
    '''
    BEHAVIOR:
        This function loads all the chunks stored in a file created
        after indexing

    RETURN:
        List[MinimalSource]
    '''
    chunks = []
    try:
        data = []
        with open("data/processed/processed_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for chunk in data:
            chunks.append(
                MinimalSource(
                    **chunk
                )
            )
        return chunks
    except (FileNotFoundError, PermissionError,
            json.JSONDecodeError, Exception) as e:
        print(e)
        return []


def load_dataset(file_path: str) -> List[MinimalSearchResults]:
    '''
    PARAMETERS:
        file_path: str

    BEHAVIOR:
        This function loads all the MinimalSearhResults stored in the
        given json file_path

    RETURN:
        List[MinimalSearchResults]
    '''
    result: List[MinimalSearchResults] = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for search in data["search_results"]:
            result.append(
                MinimalSearchResults(
                    **search
                )
            )
        return result
    except (FileNotFoundError, PermissionError,
            json.JSONDecodeError, Exception) as e:
        print(e)
        return []


def load_answers(file_path: str) -> List[AnsweredQuestion]:
    '''
    PARAMETERS:
        file_path: str

    BEHAVIOR:
        This function loads all the AnsweredQuestion stored in the
        given json file_path

    RETURN:
        List[AnsweredQuestion]
    '''
    answer = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            all_answer = json.load(f)
        question = all_answer['rag_questions']
        for elem in question:
            answer.append(
                AnsweredQuestion(
                    question_id=elem["question_id"],
                    question=elem["question"],
                    sources=[
                        MinimalSource(
                            file_path=sub_elem["file_path"],
                            first_character_index=sub_elem[
                                "first_character_index"],
                            last_character_index=sub_elem[
                                "last_character_index"],
                            text=""
                        ) for sub_elem in elem["sources"]
                    ],
                    answer=elem["answer"]
                )
            )
        return answer
    except (FileNotFoundError, json.JSONDecodeError, KeyError,
            PermissionError, Exception) as e:
        print("An error occured")
        print(e)
        return []
