from pydantic import BaseModel
from .minimalsources import MinimalSource
from typing import List


class MinimalSearchResults(BaseModel):
    '''
    PARAMETERS:
        question_id: str
        quesiton: str. The prompt
        retrieved_sources: List[MinimalSource]. The retrieved documents
    '''
    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]
