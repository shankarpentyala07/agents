from llama_index.core import SimpleDirectoryReader
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
import os
from dotenv import load_dotenv
from llama_index.embeddings.ibm import WatsonxEmbeddings
from llama_index.llms.ibm import WatsonxLLM

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex

import asyncio
#import nltk


# 1. Load Data
reader = SimpleDirectoryReader(input_dir="./data")
documents = reader.load_data()

# 2. Create Node Objects - A Node is just a chunk of text from the original document that’s easier for the AI to work with, while it still has references to the original Document object . The IngestionPipeline helps us create these nodes through two key transformations.
# SentenceSplitter breaks down documents into manageable chunks by splitting them at natural sentence boundaries.
# HuggingFaceEmbedding converts each chunk into numerical embeddings - vector representations that capture the semantic meaning in a way AI can process efficiently.

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

# Initialize WatsonxLLM
print("Initializing WatsonxEmbedding...")
watsonx_embedding = WatsonxEmbeddings(**model_config)

# Set up vector store
db = chromadb.PersistentClient(path="./db/chroma_db")
chroma_collection = db.get_or_create_collection("shankar")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
#nltk.download("stopwords")

# create the pipeline with transformations
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_overlap=0),
        watsonx_embedding,
    ],
    vector_store=vector_store
)

#nodes= await pipeline.arun(documents=documents)
async def main():
    nodes = await pipeline.arun(documents=documents)
    print(len(nodes))

asyncio.run(main())



# Vector embeddings - by embedding both the query and nodes in the same vector space, we can find relevant matches. The VectorStoreIndex handles this for us, using the same embedding model we used during ingestion to ensure consistency.All information is automatically persisted within the ChromaVectorStore object and the passed directory path
index = VectorStoreIndex.from_vector_store(vector_store, embed_model=watsonx_embedding)

# Querying a VectorStoreIndex with prompts and LLMs

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

query_engine = index.as_query_engine(
    llm=watsonx_llm,
    response_mode="tree_summarize",
)

#  we can gain insights into how our system is performing through observability. This is especially useful when we are building more complex workflows and want to understand how each component is performing.
import llama_index
import os

PHOENIX_API_KEY = os.getenv("PHOENIX_API_KEY")
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={PHOENIX_API_KEY}";
llama_index.core.set_global_handler(
    "arize_phoenix",
    endpoint="https://llamatrace.com/v1/traces"
)

response = query_engine.query("Amazon MQ is a managed message broker service for")
print(response)

# Evaluation and observability
# LlamaIndex provides built-in evaluation tools to assess response quality. These evaluators leverage LLMs to analyze responses across different dimensions. Let’s look at the three main evaluators available: FaithfulnessEvaluator, AnswerRelevancyEvaluator, CorrectnessEvaluator
from llama_index.core.evaluation import FaithfulnessEvaluator


# query index
evaluator = FaithfulnessEvaluator(llm=watsonx_llm)
eval_result = evaluator.evaluate_response(response=response)
print(eval_result.passing)



