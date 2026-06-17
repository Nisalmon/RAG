*This project has been created as part of the 42 curriculum by nisalmon*


### Description
This Project is called **RAG Against The Machine** and consist of building a RAG.


### Instruction
To install the program, you can do 
```sh
    git clone git@github.com:Nisalmon/RAG.git RAG
    cd RAG
```

Upon cloning the repo, the first thing to do is to launch the script package_installation.sh
```sh
    ./package_installation.sh
```
After installation, you must follow the instruction given by the script.


From there, you can execute the program.

For exemple:
```sh
    uv run --active python main.py index
```
```sh
    uv run --active python main.py answer "What does HTTPS stands for ?" --k 5
```


### Resources
[The BM25s documentation](https://bm25s.github.io/)  
[The astchunk documentation](https://github.com/yilinjz/astchunk)  
AI was used to review strategies on the best way to chunk all the files
and to improve the recall value.  


### System architecture
The RAG pipeline is as follow.

You first need to index the chunk.

Then you can execute search_dataset

And after that, you can execute answer_dataset.


### Chunking strategy:
The python files are chunked with the astchunk package.

The Markdown files are chunked by looping on their content and when the program detect a double '\n', it cuts it and turn it into a chunk.


### Retrieval method
The retrieval is done with the bm25s package.
It loads the indexed chunks, tokenize them.  
Tokenize the prompt.  
And return a list containg, in order, the best k documents for the prompt.


### Performance analysis
For this project when using Recall@5, we use achieve 80% for docs questions and 50% for code questions.

My program achieve 79% for docs questions ans 52% for code questions.  
I managed to achieve 83% for docs question but it increased the retrieving time from 6sec for 100 prompts to 25sec for 100 prompts. So I when back to my 79%.  
I rather have 1% less than 20 more sec to wait because in the subject it is asked to retrieve 5 documents for 1000 prompt in 90 second and it wasn't possible when I was hitting 83%.  


### Design decisions
For the CLI is decided to make a class because I wanted it to be simple,
I liked the idea of having all of the methods in the same object.


### Challenges faced
One of the biggest challenge was to implement the Recall@k system,
I didn't know the method to say if a document was relevant or not but turns out it was written in the subject.


### Example usage
You can index the chunks by doing
```sh
    uv run --activate python main.py index
```


If you want to search datasets, you can do
```sh
    uv run --active python main.py search_datasets --dataset_path "your_path/file.json" --k 10 --save_directory "save/file/path"
```