# INGEST IMPORTS
from src.ingest.loader import (load_data, load_single_prompt,
                               load_chunks, load_prompts,
                               load_dataset, load_answers)
from src.ingest.chunker import chunking
from src.ingest.getter import get_index, get_most_accurate
from src.ingest.storer import (store_processed_data, store_search_result,
                               store_answers)

# ANSWER IMPORTS
from src.answer.augment import augment_prompt
from src.answer.generate_answer import generate_answer

# RECALL IMPORTS
from src.recall import recall_at_k

# CLASSES IMPORTS
from llm_sdk import Model
from src.classes import (StudentSearchResults, MinimalAnswer,
                         StudentSearchResultsAndAnswer,
                         UnansweredQuestion)

# OTHER IMPORTS
import tqdm
import time


class CLI():
    def __init__(self) -> None:
        self.model = Model()

    def index(self, max_chunk_size: int = 2000) -> None:
        print("Loading data")
        data = load_data()

        start_timer = time.time()
        print("Chunking data")
        chunked_data = chunking(data, max_chunk_size)

        print("Storing chunked data")
        store_processed_data(chunked_data)

        print("Indexing chunks")
        data_as_str = [elem.text for elem in chunked_data]
        get_index(data_as_str)

        end_timer = time.time()
        tot_time = round(end_timer - start_timer, 2)
        print(f"It took {tot_time} sec to chunk, store and index the data")

    def search(self, question: str, k: int = 5,
               save_directory: str = "./") -> None:
        prompt = load_single_prompt(question)
        chunks = load_chunks()
        retrievial = get_most_accurate(
            prompt,
            k,
            chunks
        )
        student_search_result = StudentSearchResults(
            search_results=retrievial,
            k=k
        )
        store_search_result(student_search_result,
                            save_directory)

    def search_datasets(self, dataset_path: str, k: int = 5,
                        save_directory: str = "./") -> None:
        prompts = load_prompts(dataset_path)
        chunks = load_chunks()
        start = time.time()
        retrievial = get_most_accurate(
            prompts,
            k,
            chunks
        )
        student_search_result = StudentSearchResults(
            search_results=retrievial,
            k=k
        )
        end = time.time()
        print(round(end - start), "sec")
        store_search_result(student_search_result,
                            save_directory, dataset_path)

    def answer(self, question: str, k: int = 5) -> None:
        prompt = load_single_prompt(question)
        chunks = load_chunks()
        if chunks == []:
            print("No chunks have been found.")
            print("Therefore, no answer can be provided.")
            return
        retrievial = get_most_accurate(
            prompt,
            k,
            chunks
        )
        augmented_prompt = augment_prompt(retrievial)
        answer = []
        for question in augmented_prompt:
            answer.append(generate_answer(self.model, question))
            print(answer[-1])

    def answer_datasets(self, student_search_results_path: str,
                        save_directory: str):
        dataset = load_dataset(student_search_results_path)
        if dataset == []:
            print("No dataset has been found.")
            print("Therefore, no answer can be provided.")
            return
        print(f"Loaded {len(dataset)} questions from " +
              f"{student_search_results_path}")
        augmented_prompt = augment_prompt(dataset)
        answer = []
        count = 0
        for question in tqdm.tqdm(augmented_prompt,
                                  desc="Generating answers..."):
            answer.append(MinimalAnswer(
                question=dataset[count].question,
                question_id=dataset[count].question_id,
                retrieved_sources=dataset[count].retrieved_sources,
                answer=generate_answer(self.model, question)
                )
                )
            count += 1
        result = StudentSearchResultsAndAnswer(
            search_results=answer,
            k=len(dataset[0].retrieved_sources),
        )
        store_answers([result], save_directory,
                      student_search_results_path)

    def evaluate(self, student_answer_path: str, dataset_path: str,
                 k: int, max_context_length: int) -> None:
        if k > 20 or k <= 0:
            print("You must retrieve a number of data higher than 1 " +
                  "and up to 20.")
            return
        test = [
            1, 3, 5, 10, 15, 20
        ]
        data = load_data()
        chunked_data = chunking(data, max_context_length)
        dataset = load_answers(dataset_path)
        search_result = load_dataset(student_answer_path)
        prompts = []
        for data in search_result:
            prompts.append(
                UnansweredQuestion(
                    question_id=data.question_id,
                    question=data.question
                )
            )
        print("Evaluation Results")
        print("=" * 30)
        print("Question evaluated:", len(dataset))
        for recall in test:
            value = []
            if recall > k:
                break
            retrieval = get_most_accurate(
                prompts,
                recall,
                chunked_data
            )
            for elem in retrieval:
                for question in dataset:
                    if elem.question == question.question:
                        value.append(recall_at_k(question.sources,
                                                 elem.retrieved_sources))

            moyenne = sum(1 for nb in value if nb == 1.0)/len(value)
            print(f"Recall@{recall}: {moyenne}")
