# Pradigi Hiring Task
A Q&A chatbot for the [website](https://pratham.org/).

## Setup:

### Set `.env` from `.env.example`
```bash
MISTRAL_API_KEY=MistralAI API Key
QDRANT_API_KEY=Qdrant API Key (only if hosted using qdrant cloud)
QDRANT_URL=Qdrant URL
QDRANT_CN=Qdrant Collection Name
PROJ_BASE_URL=https://pratham.org/
JINA_RR_API_KEY=API Key for Jina AI Reranker v2 [optional]
FASTEMBED_MODEL=Embedding model name for fastembed (One of: 1. jinaai/jina-embeddings-v2-small-en or 2. BAAI/bge-small-en-v1.5)
```

### Run Locally
In a Python 3.12 environment shell of your choice, run the following command:

```bash
(venv) python -m pip install pre-commit pip-tools
(venv) pip-sync requirements/requirements.txt
```

### Run locally in dev mode:
```bash
(venv) pip-sync requirements/requirements.txt requirements/requirements-dev.txt
```

## Ingestion:
To ingest data (from pre-defined sources), run the following:
```bash
(venv) python -m src.ingest
```
Note: It is recommended to run this command in a [tmux](https://github.com/tmux/tmux/wiki) shell, since it takes a long time depending upon the chunk size and embedding model used.

## Chat UI:
To run chat ui, run the following:
```bash
(venv) python -m src.chat
```

Then open a new tab in your favourite browser, and enter http://localhost:7860/ into the address bar.


## To re-rank or not to:
While running in dev mode, one can also use the [Jina AI Reranker](https://jina.ai/reranker/) model to filter out the chunks of text chosen for generation. We observe that this approach is effective only as long as the `top_k` vectors to be searched for is greater than `50`.

### To use the reranker:
1. Set `JINA_RR_API_KEY` in `.env`.

2. Uncomment the following lines from [chat.py](src/chat.py):  
a. [line 37](src/chat.py#L37)  
b. [line 43](src/chat.py#L43)

3. Change the `similarity_top_k` argument from `10` to  `50` or greater at [line 42](src/chat.py#L42). Higher value means higher cost per request.

For most of our use-cases, `top_k = 10` is a good standard value and doesnot require reranker api.
