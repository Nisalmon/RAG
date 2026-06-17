from pydantic import BaseModel, Field
import uuid
from typing import List
from .minimalsources import MinimalSource


class UnansweredQuestion(BaseModel):
    '''
    PARAMETERS:
        question_id: str
        quesiton: str. The prompt
    '''
    question_id: str = Field(default_factory=lambda:
                             str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    '''
    PARAMETERS:
        sources: List[MinimalSource]. The retrieved documents
        answer: str. The answer to the question
    '''
    sources: List[MinimalSource]
    answer: str
