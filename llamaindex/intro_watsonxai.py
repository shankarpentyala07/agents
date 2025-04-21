import os
import warnings
from dotenv import load_dotenv
from llama_index.llms.ibm import WatsonxLLM

# Suppress all warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Load required config from environment
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Set API key in environment for WatsonxLLM
os.environ["WATSONX_APIKEY"] = WATSONX_API_KEY

# Model parameters
model_config = {
    "model_id": "ibm/granite-3-3-8b-instruct",
    "url": WATSONX_URL,
    "project_id": WATSONX_PROJECT_ID,
    "temperature": 0.5,
    "max_new_tokens": 50,
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

# Generate a completion
prompt = "What is Generative AI?"
response = watsonx_llm.complete(prompt)

# Output raw response
print(response.raw)

"""
Initializing WatsonxLLM...
{'model_id': 'ibm/granite-3-3-8b-instruct', 'model_version': '3.3.0', 'created_at': '2025-04-20T19:10:48.218Z', 'results': [{'generated_text': '\nGenerative AI is a subset of artificial intelligence that focuses on creating new content, such as images, text, voice, or video. It learns patterns from existing data and generates novel content based on those patterns.\n\n', 'generated_token_count': 50, 'input_token_count': 6, 'stop_reason': 'max_tokens'}]}
"""
