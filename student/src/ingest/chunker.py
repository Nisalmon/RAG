from src.classes import MinimalSource
from astchunk import ASTChunkBuilder
from typing import List, Dict, Any
import tqdm


def chunking(data: List[List[Dict[str, Any]]],
             maxchunk: int) -> List[MinimalSource]:
    '''
    PARAMETERS:
        data: List[List[Dict[str, Any]]]
        maxchunk: int

    BEHAVIOR:
        This function chunks all the data stored in data

    RETURN:
        List[MinimalSource]
    '''
    chunk_lst: List[MinimalSource] = []
    chunk_by_ast_py(data[0], chunk_lst, maxchunk)
    chunk_markdown(data[1], chunk_lst, maxchunk)
    return chunk_lst


def chunk_python(data: List[Dict[str, Any]],
                 lst: List[MinimalSource], maxchunk: int) -> None:
    '''
    PARAMETERS:
        data: List[Dict[str, Any]]
        lst: List[MinimalSource]

    BEHAVIOR:
        This function fills lst with chunks of python file
    '''
    config = {
         "max_chunk_size": maxchunk if maxchunk < 2000 else 2000,
         "language": "python",
         "metadata_template": "default"
    }
    chunk_builder = ASTChunkBuilder(**config)

    for code in data:
        chunks = chunk_builder.chunkify(code['content'])
        for chunk in chunks:
            start_line = chunk["metadata"]["start_line_no"]
            end_line = chunk["metadata"]["end_line_no"]
            lines = code["content"].splitlines(keepends=True)

            start = sum(len(line) for line in lines[:start_line])
            end = sum(len(line) for line in lines[:end_line + 1])
            lst.append(
                MinimalSource(
                    file_path=code['path'],
                    first_character_index=start,
                    last_character_index=end,
                    text=str(chunk["content"])
                )
            )


def chunk_markdown(data: List[Dict[str, Any]],
                   lst: List[MinimalSource], maxchunk: int) -> None:
    '''
    PARAMETERS:
        data: List[Dict[str, Any]]
        lst: List[MinimalSource]

    BEHAVIOR:
        This function fills lst with chunks of markdown file
    '''
    for elem in data:
        ind = 0
        fst_chr = ind
        nb_chr = 0
        previous_char = None
        for ch in elem["content"]:
            nb_chr += 1
            if ((previous_char and previous_char == "\n" and ch == "\n")
               or (nb_chr >= 2000 or nb_chr >= maxchunk)):
                lst.append(
                    MinimalSource(
                        file_path=elem["path"],
                        first_character_index=fst_chr,
                        last_character_index=ind,
                        text=str(elem["content"][fst_chr:ind])
                    )
                )
                overlap = 350
                nb_chr = int(overlap * 0.1)
                fst_chr = max(0, ind - nb_chr)
            previous_char = ch
            ind += 1
        lst.append(
                    MinimalSource(
                        file_path=elem["path"],
                        first_character_index=fst_chr,
                        last_character_index=len(elem["content"]),
                        text=str(elem["content"][fst_chr:ind])
                    )
                )


def chunk_by_ast_py(
        python: List[Dict[str, Any]],
        lst: List[MinimalSource],
        max_char: int = 2000) -> List[MinimalSource]:
    try:
        for file in tqdm.tqdm(python):
            code = file["content"]
            configs = {
                "max_chunk_size": int(max_char * (90 / 100)),
                "language": "python",
                "metadata_template": "default"
            }
            chunk_builder = ASTChunkBuilder(**configs)

            chunks = chunk_builder.chunkify(code)
            start = 0
            for chunk in chunks:
                text = chunk["content"]
                if len(text) > max_char:
                    sub_chunks = [
                        text[i:i + max_char] for i in range(0, len(text),
                                                            max_char - 1
                                                            )]
                else:
                    sub_chunks = [text]
                for sub_chunk in sub_chunks:
                    lst.append(
                        MinimalSource(
                            file_path=str(file["path"]),
                            first_character_index=start,
                            last_character_index=start + len(sub_chunk),
                            text=sub_chunk
                        )
                    )
                    start += len(sub_chunk)
    except Exception:
        print("Error while chunking python file")
        quit()
