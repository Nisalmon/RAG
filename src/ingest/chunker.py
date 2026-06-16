from src.classes import MinimalSource
from astchunk import ASTChunkBuilder
from typing import List, Dict, Any


def chunking(data: List[List[Dict[str, Any]]],
             maxchunk: int) -> List[MinimalSource]:
    chunk_lst: List[MinimalSource] = []
    chunk_python(data[0], chunk_lst, maxchunk)
    chunk_markdown(data[1], chunk_lst, maxchunk)
    return chunk_lst


def chunk_python(data: List[Dict[str, Any]],
                 lst: List[MinimalSource], maxchunk: int) -> None:
    config = {
         "max_chunk_size": min(maxchunk, 2000),
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
