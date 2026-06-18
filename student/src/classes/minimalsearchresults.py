from pydantic import BaseModel
from .minimalsources import MinimalSource
from typing import List


class MinimalSearchResults(BaseModel):
    '''
    PARAMETERS:
        question_id: str
        quesiton_str: str. The prompt
        retrieved_sources: List[MinimalSource]. The retrieved documents
    '''
    question_id: str
    question_str: str
    retrieved_sources: List[MinimalSource]
