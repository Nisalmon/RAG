from pydantic import BaseModel
from src.classes import MinimalSearchResults, MinimalAnswer
from typing import List


class StudentSearchResults(BaseModel):
    search_results: List[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(StudentSearchResults):
    search_results: List[MinimalAnswer]
