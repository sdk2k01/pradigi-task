import gradio as gr

from llama_index.core import VectorStoreIndex
from llama_index.core.settings import Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.postprocessor.jinaai_rerank import JinaRerank

from qdrant_client import QdrantClient
import os

from dotenv import load_dotenv

load_dotenv(override=True)

# Instantiate vector store client
client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

# Instantiate vector store
qdrant_store = QdrantVectorStore(collection_name=os.getenv("QDRANT_CN"), client=client)

# Initialise settings
Settings.llm = MistralAI(
    model="mistral-small-latest",
    max_tokens=8192,
    max_retries=2,
    api_key=os.getenv("MISTRAL_API_KEY"),
)
Settings.embed_model = FastEmbedEmbedding(model_name=os.getenv("FASTEMBED_MODEL"))
Settings.context_window = 32768

index = VectorStoreIndex.from_vector_store(
    vector_store=qdrant_store,
)

# rerank = JinaRerank(top_n=10, model='jina-reranker-v2-base-multilingual', api_key=os.getenv('JINA_RR_API_KEY')) # Optional

query_engine = index.as_query_engine(
    streaming=True,
    vector_store_query_mode="mmr",
    similarity_top_k=10,
    # node_postprocessors = [rerank] # Works better for multi-node retrieval tasks (>50)
)

with gr.Blocks(
    title="Pratham Chatbot", theme="JohnSmith9982/small_and_pretty@>=1.0.0"
) as demo:
    chatbot = gr.Chatbot(label="Ask me anything", show_copy_button=True, layout="panel")
    msg = gr.Textbox(
        placeholder="Tell me about the positive impacts brought about by Pratham."
    )
    clear = gr.ClearButton([msg, chatbot])

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def streaming_response(history):
        stream_resp = query_engine.query(history[-1][0])
        history[-1][1] = ""
        for text in stream_resp.response_gen:
            history[-1][1] += text
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        streaming_response, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
