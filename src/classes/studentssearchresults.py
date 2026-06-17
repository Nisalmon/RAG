from pydantic import BaseModel
from src.classes import MinimalSearchResults, MinimalAnswer
from typing import List


class StudentSearchResults(BaseModel):
    '''
    PARAMETERS:
        search_results: List[MinimalSearchResults | MinimalAnswer].
        k: int
    '''
    search_results: List[MinimalSearchResults | MinimalAnswer]
    k: int


class StudentSearchResultsAndAnswer(StudentSearchResults):
    '''
    PARAMETERS:
        search_results: List[MinimalSearchResults | MinimalAnswer].
    '''
    search_results: List[MinimalSearchResults | MinimalAnswer]
