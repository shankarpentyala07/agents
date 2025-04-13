import os
import numpy as np
import time
import datetime

from huggingface_hub import login
from dotenv import load_dotenv

from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel
from smolagents import LiteLLMModel

from smolagents import tool

# Load environment variables from .env file
load_dotenv()

#Retrieve the environment variable
hf_token = os.getenv("HF_TOKEN")

#Login using the token
login(token=hf_token, add_to_git_credential=False)

#LLM to use watsonx.ai models
llm  = LiteLLMModel(
    model_id = "watsonx/meta-llama/llama-3-3-70b-instruct",
    api_key = os.getenv("WATSONX_API_KEY"),
    num_ctx=8162
)
# To use Hugging Face Models
#agent = CodeAgent(tools = [DuckDuckGoSearchTool()] , model=HfApiModel())

#To use watsonx models
agent = CodeAgent(tools = [DuckDuckGoSearchTool()] , model=llm)

# Selecting a playlist for the Party Using smolagents
# agent.run("Search for the best music recommendations for a party at the Wayne's mansion")

# Using a Custom Tool to Prepare the Menu

@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occassion.
    Args:
       occasion (str): The type of occasion for the party. Allowed values are:
                       - "casual": Menu for casual party.
                       - "formal": Menu for formal party.
                       - "superhero": Menu for superhero party.
                       - "custom": Custom menu.
    """
    if occasion == "causal":
        return "Pizza, snacks, and drinks"
    elif occasion == "formal":
        return "3-course dinner with wine and dessert"
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food"
    else:
        return "Custom menu for the butler."
    
# Alfred, the butler, preparing menu for the party - To use Hugging Face models
#agent = CodeAgent(tools=[suggest_menu], model=HfApiModel())

agent = CodeAgent(tools=[suggest_menu], model=llm)

# Preparing the menu for the party
# agent.run("Prepare a india menu for the party.")
# The agent will run for a few steps until finding the answer. Precising allowed values in the docstring helps direct agent to occasion argument values which exist and limit hallucinations
#To use watsonx models
agent = CodeAgent(tools=[], model = llm,additional_authorized_imports=['datetime'])

# agent.run(
#     """
#     Alfred needs to prepare for the party. Here are the tasks:
#     1. Prepare the drinks - 30 minutes
#     2. Decorate the mansion - 60 minutes
#     3. Set up the menu - 45 minutes
#     4. Prepare the music and playlist - 45 minutes

#     If we start right now, at what time will the party be ready
#     """
# )

# Change to your username and repo name
agent.push_to_hub('Shankar43/AlfredAgent')