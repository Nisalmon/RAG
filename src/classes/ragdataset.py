from pydantic import BaseModel
from src.classes import (AnsweredQuestion,
                         UnansweredQuestion)
from typing import List


class RagDataset(BaseModel):
    '''
    PARAMETERS:
        rag_questions: List[AnsweredQuestion | UnansweredQuestion]
    '''
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]
