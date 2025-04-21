from llama_index.core import VectorStoreIndex
from llama_index.core.tools import QueryEngineTool

import os
from dotenv import load_dotenv

from llama_index.llms.ibm import WatsonxLLM
from llama_index.embeddings.ibm import WatsonxEmbeddings
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb


# Load environment variables
load_dotenv()

# Load required config from environment
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# adjust embedding parameters for different tasks
truncate_input_tokens = 3

# Set API key in environment for WatsonxLLM
os.environ["WATSONX_APIKEY"] = WATSONX_API_KEY

# Model parameters
model_config = {
    "model_id": "ibm/slate-125m-english-rtrvr",
    "url": WATSONX_URL,
    "project_id": WATSONX_PROJECT_ID,
    "truncate_input_tokens": truncate_input_tokens
}

# Initialize Watsonx Embedding Model
print("Initializing WatsonxEmbedding...")
watsonx_embedding = WatsonxEmbeddings(**model_config)

# Create Vector Store
db = chromadb.PersistentClient(path="./alfred_chroma_db")
chroma_collection = db.get_or_create_collection("alfred")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Create Vector Store Index
index = VectorStoreIndex.from_vector_store(vector_store, embed_model=watsonx_embedding)

# Create Query Engine
# Model parameters
model_config = {
    "model_id": "ibm/granite-3-3-8b-instruct",
    "url": WATSONX_URL,
    "project_id": WATSONX_PROJECT_ID,
    "temperature": 0.5,
    "max_new_tokens": 150,
    "additional_params": {
        "decoding_method": "sample",
        "min_new_tokens": 1,
        "top_k": 50,
        "top_p": 1,
    }
}

# Initialize WatsonxLLM
print("Initializing WatsonxLLM...")
watsonx_llm = WatsonxLLM(**model_config)
query_engine = index.as_query_engine(watsonx_llm)

tool = QueryEngineTool.from_defaults(query_engine,name="some useful name", description="some useful description")



