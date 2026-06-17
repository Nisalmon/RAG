from typing import List
from src.classes import MinimalSearchResults


def get_resources(prompt: MinimalSearchResults) -> str:
    '''
    PARAMETERS:
        prompt: MinimalSearchResults. The prompt with retrieved documents.

    BEHAVIOR:
        This function is used to return a string of the retrieved documents.

    RETURN:
        str
    '''
    text = ""
    for elem in prompt.retrieved_sources:
        text += f"{elem.file_path}\n"
        text += f"{elem.text}\n\n"
    return text


def augment_prompt(prompts: List[MinimalSearchResults]) -> List[str]:
    '''
    PARAMETERS:
        prompt: List[MinimalSearchResults].

    BEHAVIOR:
        This function is used to add context to the prompts.

    RETURN:
        List[str]
    '''
    augmented_prompt = []
    sentences = [
        "You have to answer the following question using given resources.\n",
        "The question: ",
        "\nThe resources:\n"
    ]
    res = ""
    for prompt in prompts:
        res += sentences[0]
        res += sentences[1]
        res += prompt.question
        res += sentences[2]
        res += get_resources(prompt)
        augmented_prompt.append(res)
        res = ""
    return augmented_prompt
