from smolagents import CodeAgent, DuckDuckGoSearchTool
from smolagents import LiteLLMModel

import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the search tool
search_tool = DuckDuckGoSearchTool()

#Initalize the model
# LiteLLM for watsonx.ai Inference Engine
llm = LiteLLMModel(
    model_id="watsonx/meta-llama/llama-3-3-70b-instruct",
    api_key=os.getenv("WATSONX_API_KEY"),
    num_ctx=8162 # Context window size
)

# Initalize CodeAgent
agent = CodeAgent(
    tools=[search_tool],
    model=llm,
)

# Usage
response = agent.run(
    "Search for luxury superhero-themed party ideas, including decorations, entertainment, and catering."
)

# response
print(response)

"""
The agent follows this process:

Analyzes the Request: Alfred’s agent identifies the key elements of the query—luxury superhero-themed party planning, with focus on decor, entertainment, and catering.
Performs Retrieval: The agent leverages DuckDuckGo to search for the most relevant and up-to-date information, ensuring it aligns with Alfred’s refined preferences for a luxurious event.
Synthesizes Information: After gathering the results, the agent processes them into a cohesive, actionable plan for Alfred, covering all aspects of the party.
Stores for Future Reference: The agent stores the retrieved information for easy access when planning future events, optimizing efficiency in subsequent tasks.
"""

