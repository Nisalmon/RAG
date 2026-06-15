from typing import List, Any


def reranking(chunks: Any) -> List:
    print(sorted(chunks.score[0]))
