from src.classes import MinimalSource


def compute_overlap(a: MinimalSource, b: MinimalSource) -> int:
    '''
    PARAMETERS:
        a: MinimalSource
        b: MinimalSource

    BEHAVIOR:
        This function compare the given sources and by how much
        their content overlaps.

    RETURN:
        int
    '''
    file_path = [
        a.file_path.split("vllm-0.10.1")[-1],
        b.file_path.split("vllm-0.10.1")[-1],
    ]
    if file_path[0] != file_path[1]:
        return 0

    start = max(a.first_character_index, b.first_character_index)
    end = min(a.last_character_index, b.last_character_index)

    return max(0, end - start)


def overlap_ratio(correct: MinimalSource, retrieved: MinimalSource) -> float:
    '''
    PARAMETERS:
        correct: MinimalSource. The reference source.
        retrieved: MinimalSource. The retrieved source by the program

    BEHAVIOR:
        This function returns a ratio of how much the given sources overlaps.

    RETURN:
        int
    '''
    correct_size = correct.last_character_index - correct.first_character_index

    if correct_size == 0:
        return 0.0

    overlap = compute_overlap(correct, retrieved)

    return overlap / correct_size


def is_found(correct: MinimalSource,
             retrieved_list: list[MinimalSource]) -> bool:
    '''
    PARAMETERS:
        correct: MinimalSource. The reference source.
        retrieved: List[MinimalSource]. The retrieved sources by the program

    BEHAVIOR:
        This function returns if one of the retrieved sources has at least
        5 percent of overlap with he correct source.

    RETURN:
        bool
    '''
    for r in retrieved_list:
        if overlap_ratio(correct, r) >= 0.05:
            return True
    return False


def recall_at_k(correct_sources: list[MinimalSource],
                retrieved_sources: list[MinimalSource]) -> float:
    '''
    PARAMETERS:
        correct_sources: List[MinimalSource]
        retrieved_sources: List[MinimalSource]

    BEHAVIOR:
        Return a percentage of how many retrieved sources are correct.

    RETURN:
        int
    '''
    if not correct_sources:
        return 0.0

    found = 0

    for c in correct_sources:
        if is_found(c, retrieved_sources):
            found += 1

    return found / len(correct_sources)
