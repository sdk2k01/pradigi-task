from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.fastembed import FastEmbedEmbedding

from qdrant_client import QdrantClient
import os

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    client = QdrantClient(
        url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY")
    )
    qdrant_store = QdrantVectorStore(
        collection_name=os.getenv("QDRANT_CN"), client=client
    )
    service_context = ServiceContext.from_defaults(
        llm=MistralAI(
            model="mistral-small",
            max_tokens=8192,
            max_retries=2,
            api_key=os.getenv("MISTRAL_API_KEY"),
        ),
        embed_model=FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5"),
        context_window=8192,
    )
    index = VectorStoreIndex.from_vector_store(
        vector_store=qdrant_store,
        embed_model=FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5"),
        service_context=service_context,
    )
    query_engine = index.as_query_engine()

    while True:
        query = input()
        resp = query_engine.query(query)
        print(f"\nResp: {resp}\n")
