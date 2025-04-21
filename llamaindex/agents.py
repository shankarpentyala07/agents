from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.tools import FunctionTool
import os
from dotenv import load_dotenv
from llama_index.llms.ibm import WatsonxLLM
import asyncio


#define sample Tool -- type annotations , function names, and docstrings, are all included in parsed schemas!
def multiply(a: int, b: int) -> int:
    """Multiplies two integers and returns the resulting integer"""
    return a * b

# Initalize LLM
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

# initialize agent
agent = AgentWorkflow.from_tools_or_functions(
    [FunctionTool.from_defaults(multiply)],
    llm=watsonx_llm
)

"""
Agents are stateless by default, add remembering past interactions is opt-in using a Context object This might be useful if you want to use an agent that needs to remember previous interactions, like a chatbot that maintains context across multiple messages or a task manager that needs to track progress over time.
"""

# remembering state
from llama_index.core.workflow import Context

ctx = Context(agent)

# stateless
#response = await agent.run("What is 2 times 2?")
async def main():
    response = await agent.run("What is 2 times 2?")
    print(response)

    response = await agent.run("My name is Bob.", ctx=ctx)
    print(response)
    response = await agent.run("What was my name again?", ctx=ctx)
    print(response)

asyncio.run(main())





