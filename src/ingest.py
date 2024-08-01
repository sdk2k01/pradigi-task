from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.core.settings import Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from qdrant_client import QdrantClient
import os

from .utils import get_site_text, update_sitemap_recursively
from .doc_utils import DocumentTransformer


def ingest(
    sitemap: set, qclient: QdrantClient, collection_name: str | None = "pradigi"
) -> None:
    """
    Ingest documents from BASE_URL sitemap.
    """
    docs = get_site_text(sitemap)  # Resource Intensive

    docs = list(map(DocumentTransformer.generate_doc_id, docs))

    transformations = [
        DocumentTransformer(),
        SentenceSplitter(chunk_size=400, chunk_overlap=40),
    ]

    Settings.llm = None
    Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.transformations = transformations

    qdrant_store = QdrantVectorStore(collection_name=collection_name, client=qclient)
    storage_context = StorageContext.from_defaults(vector_store=qdrant_store)

    VectorStoreIndex.from_documents(
        docs,
        storage_context=storage_context,
        show_progress=True,
    )


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    # Initialize base sitemap
    base_sitemap = {
        f"{os.getenv('PROJ_BASE_URL')}",
    }

    # Instantiate qdrant client
    qclient = QdrantClient(
        url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY")
    )

    # Recursively generate sitemap at depth=2
    sitemap = update_sitemap_recursively(base_sitemap, 2)

    # Ingest
    ingest(sitemap, qclient, os.getenv("QDRANT_CN"))
