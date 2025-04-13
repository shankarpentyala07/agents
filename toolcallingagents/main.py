from smolagents import ToolCallingAgent , DuckDuckGoSearchTool, LiteLLMModel

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# LiteLLM for watsonx.ai Inference Engine
llm = LiteLLMModel(
    model_id="watsonx/meta-llama/llama-3-3-70b-instruct",
    api_key=os.getenv("WATSONX_API_KEY"),
    num_ctx=8162 # Context window size
)

agent = ToolCallingAgent(tools=[DuckDuckGoSearchTool()], model=llm)

agent.run("Search for the best music recommendations for a party at the Wayne's mansion.")
