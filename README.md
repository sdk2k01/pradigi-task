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

## Chat UI:
To run chat ui, run the following:
```bash
(venv) python -m src.chat
```

Then open a new tab in your favourite browser, and enter http://localhost:7860/ into the address bar.
