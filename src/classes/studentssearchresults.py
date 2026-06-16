from pydantic import BaseModel
from src.classes import MinimalSearchResults, MinimalAnswer
from typing import List


class StudentSearchResults(BaseModel):
    search_results: List[MinimalSearchResults | MinimalAnswer]
    k: int


class StudentSearchResultsAndAnswer(StudentSearchResults):
    search_results: List[MinimalSearchResults | MinimalAnswer]
