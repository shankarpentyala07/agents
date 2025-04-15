import os
from PIL import Image
from smolagents import CodeAgent, GoogleSearchTool, VisitWebpageTool

from smolagents import LiteLLMModel
import os
from dotenv import load_dotenv

import cargo_plane_transfertime
from cargo_plane_transfertime import  calculate_cargo_travel_time

load_dotenv()

#Initalize the model
# LiteLLM for watsonx.ai Inference Engine
llm = LiteLLMModel(
    model_id="watsonx/meta-llama/llama-3-3-70b-instruct",
    api_key=os.getenv("WATSONX_API_KEY"),
    num_ctx=8162 # Context window size
)

task = """Find all Batman filming locations in the world, calculate the time to transfer via cargo plane to here (we're in Gotham, 40.7128° N, 74.0060° W), and return them to me as a pandas dataframe. Also give me some supercar factories with the same cargo plane transfer time."""

agent = CodeAgent(
    model=llm,
    tools=[GoogleSearchTool("serper"), VisitWebpageTool(), calculate_cargo_travel_time],
    additional_authorized_imports=["pandas"],
    max_steps=20
)

result = agent.run(task)

print(result)