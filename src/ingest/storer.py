from src.classes import (MinimalSource,
                         StudentSearchResults,
                         StudentSearchResultsAndAnswer)

from pathlib import Path
from typing import List
import json


def store_processed_data(chunked_data: List[MinimalSource]) -> None:
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    serialized_data = [obj.__dict__ for obj in chunked_data]
    with open("./data/processed/processed_data.json", "w") as f:
        json.dump(serialized_data, fp=f, indent=4)


def store_search_result(result: StudentSearchResults,
                        file_path: str, file_name: str | None = None) -> None:
    Path(file_path).mkdir(parents=True, exist_ok=True)
    serialized_data = {
        "search_results": result.search_results,
        "k": result.k
    }
    serialized_data["search_results"] = [obj.__dict__
                                         for obj
                                         in serialized_data["search_results"]]
    for i in range(len(serialized_data["search_results"])):
        data = [obj.__dict__
                for obj
                in serialized_data["search_results"][i]["retrieved_sources"]]
        serialized_data["search_results"][i]["retrieved_sources"] = data
    name = file_name.split("/")[-1] if file_name else "dataset_public.json"
    with open(f"{file_path}/{name}", "w") as f:
        json.dump(serialized_data, fp=f, indent=4)
    print(f"Saving student_search_result to {file_path}/{name}")


def store_answers(answers: List[StudentSearchResultsAndAnswer], file_path: str,
                  file_name: str | None = None) -> None:
    Path(file_path).mkdir(parents=True, exist_ok=True)
    serialized_data = {
        "search_results": [],
        "k": answers[0].k
    }
    for data in answers:
        for sub_data in data.search_results:
            serialized_data["search_results"].append(
                {
                    "question_id": sub_data.question_id,
                    "question": sub_data.question,
                    "retrieved_sources": [
                        obj.__dict__ for obj in sub_data.retrieved_sources
                    ],
                    "answer": sub_data.answer
                }
            )
    name = file_name.split("/")[-1] if file_name else "dataset_public.json"
    with open(f"{file_path}/{name}", "w") as f:
        json.dump(serialized_data, fp=f, indent=4)
