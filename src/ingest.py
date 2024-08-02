from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.core.extractors import TitleExtractor, KeywordExtractor
from llama_index.core.settings import Settings
from llama_index.core import Document
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding

from qdrant_client import QdrantClient
import os
import time

from .utils import get_site_text, update_sitemap_recursively, get_social_media_set
from .doc_utils import DocumentTransformer
from .llm_utils import CustomMistralAI, TITLE_CMB_PROMPT


def ingest(
    sitemap: set,
    qclient: QdrantClient,
    mistral_api_key: str,
    collection_name: str,
    embedding_model_name: str,
) -> None:
    """
    Ingest documents from BASE_URL sitemap.
    """
    social_media_links = get_social_media_set(sitemap)

    docs = get_site_text(sitemap.difference(social_media_links))  # Resource Intensive

    docs.append(Document(text="\n".join(social_media_links)))
    docs = list(map(DocumentTransformer.generate_doc_id, docs))

    # Settings.llm = None
    Settings.llm = CustomMistralAI(
        model="open-mistral-nemo",
        api_key=mistral_api_key,
    )
    Settings.embed_model = FastEmbedEmbedding(model_name=embedding_model_name)

    transformations = [
        DocumentTransformer(),
        SentenceSplitter(chunk_size=400, chunk_overlap=40),
        TitleExtractor(nodes=3, combine_template=TITLE_CMB_PROMPT),
        KeywordExtractor(keywords=10),
    ]
    Settings.transformations = transformations

    qdrant_store = QdrantVectorStore(collection_name=collection_name, client=qclient)
    storage_context = StorageContext.from_defaults(vector_store=qdrant_store)

    for i in range(0, len(docs), 10):
        VectorStoreIndex.from_documents(
            docs[i : (i + 10)],
            storage_context=storage_context,
            show_progress=True,
        )  # Resource Intensive

        time.sleep(30)  # 30 sec cool-down

    if i < len(docs):
        VectorStoreIndex.from_documents(
            docs[i : len(docs)],
            storage_context=storage_context,
            show_progress=True,
        )  # Resource Intensive


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(override=True)

    # Initialize base sitemap
    base_sitemap = {
        f"{os.getenv('PROJ_BASE_URL')}",
    }

    # Instantiate qdrant client
    qclient = QdrantClient(
        url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY")
    )

    # Recursively generate sitemap at depth=2
    sitemap = update_sitemap_recursively(base_sitemap, os.getenv("PROJ_BASE_URL"), 2)

    # Ingest
    ingest(
        sitemap,
        qclient,
        os.getenv("MISTRAL_API_KEY"),
        os.getenv("QDRANT_CN"),
        os.getenv("FASTEMBED_MODEL"),
    )
