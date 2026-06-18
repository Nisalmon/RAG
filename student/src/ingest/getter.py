import bm25s
from typing import List, Dict, Any
from src.classes import MinimalSource, UnansweredQuestion, MinimalSearchResults
import tqdm


def get_file_info(content: str, files: List[MinimalSource]) -> Dict[str, Any]:
    '''
    PARAMETERS:
        content: str
        files: List[MinimalSource]

    BEHAVIOR:
        This function returns the inforamtion of a file.
        Such as file_path, text

    RETURN:
        Dict[str, Any]
    '''
    for elem in files:
        if elem.text == content:
            return {
                "file_path": elem.file_path,
                "first_character_index": elem.first_character_index,
                "last_character_index": elem.last_character_index,
                "text": elem.text
            }
    return {}


def get_index(data: List[str]) -> None:
    '''
    PARAMETERS:
        data: List[str]

    BEHAVIOR:
        This function index all the data
    '''
    data_tokens = bm25s.tokenize(data, show_progress=False)
    ind = bm25s.BM25(corpus=data)
    ind.index(data_tokens, show_progress=False)
    ind.save("bm25_index", corpus=data, show_progress=False)


def get_most_accurate(prompts: List[UnansweredQuestion] | str,
                      k: int, full_data: List[MinimalSource]) -> List[Any]:
    '''
    PARAMETERS:
        prompts: List[UnansweredQuestion] | str
        k: int
        full_data: List[MinimalSource]

    BEHAVIOR:
        This function returns a list of retrieved documents for each prompt.

    RETURN:
        List[Any]
    '''
    retrieval = []
    stopwords = [
        "a", "an", "the"
    ]
    if not isinstance(prompts, (str, List)):
        print("⚠️ ERROR ⚠️: The prompt must be given as a list or a string !")
        return []
    if isinstance(prompts, str):
        prompts = [UnansweredQuestion(
            question_id="1",
            question=prompts
        )]
    if isinstance(prompts, List):
        retrieval = prompt_lst(prompts, k, full_data,
                               stopwords)
    return retrieval


def prompt_lst(prompts: List[UnansweredQuestion],
               k: int, full_data: List[MinimalSource],
               stopwords: List[str]) -> List[MinimalSearchResults]:
    '''
    PARAMETERS:
        prompts: List[UnansweredQuestion]
        k: int
        full_data: List[MinimalSource]
        stopwords: List[str]

    BEHAVIOR:
        This function retrieve k documents for each prompt.

    RETURN:
        List[MinimalSearchResults]
    '''
    ind = 0
    indexes = []
    result = []
    retriever = bm25s.BM25.load("bm25_index", load_corpus=True, mmap=True)
    for prompt in tqdm.tqdm(prompts, desc=f"Retrieving {k} documents"):

        prompt_token = bm25s.tokenize(prompt.question, stopwords=stopwords,
                                      show_progress=False, return_ids=False)
        res = retriever.retrieve(prompt_token, k=k,
                                 show_progress=False)

        indexes.append(
            {
                "prompt": prompt.question,
                "prompt_id": prompt.question_id
            }
        )

        for i in range(k):
            indexes[ind].update({
                f"section_{i + 1}": get_file_info(str(
                    res.documents[0][i]['text']
                    ), full_data)
            })
        result.append(
            MinimalSearchResults(
                question_id=indexes[ind]["prompt_id"],
                question_str=indexes[ind]["prompt"],
                retrieved_sources=get_sources(indexes[ind])
            )
        )
        ind += 1

    return result


def get_sources(sources: Dict[str, Any]) -> List[MinimalSource]:
    '''
    PARAMETERS:
        sources: Dict[str, Any]

    BEHAVIOR:
        This function return all the MinimalSource stored in sources.

    RETURN:
        List[MinimalSource]
    '''
    try:
        max_ind = 1
        while 1:
            _ = sources[f"section_{max_ind}"]
            max_ind += 1
    except KeyError:
        ind = 1
        result = []
        while ind < max_ind:
            result.append(
                MinimalSource(
                    file_path=sources[f"section_{ind}"]["file_path"],
                    first_character_index=sources[f"section_{ind}"]
                    ["first_character_index"],
                    last_character_index=sources[f"section_{ind}"]
                    ["last_character_index"],
                    text=sources[f"section_{ind}"]["text"]
                )
            )
            ind += 1
        return result
