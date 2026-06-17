from pydantic import BaseModel


class MinimalSource(BaseModel):
    '''
    PARAMETERS:
        file_path: str. The file path
        first_character_index: int. The index of the starting character
        last_character_index: int. The index of the ending character
        text: str. Th content of the chunk
    '''
    file_path: str
    first_character_index: int
    last_character_index: int
    text: str
