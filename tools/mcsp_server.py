# The MCP servers tools can be loaded in a ToolCollection object as follow:
from smolagents import ToolCollection, CodeAgent, LiteLLMModel
from mcp import StdioServerParameters

import os
from dotenv import load_dotenv

load_dotenv()

# LiteLLM for watsonx.ai Inference Engine
llm = LiteLLMModel(
    model_id="watsonx/meta-llama/llama-3-3-70b-instruct",
    api_key=os.getenv("WATSONX_API_KEY"),
    num_ctx=8162 # Context window size
)

server_parameters = StdioServerParameters(
    command="uvx",
    args=["--quiet", "pubmedmcp@0.1.3"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
    agent = CodeAgent(tools=[*tool_collection.tools], model=llm, add_base_tools=True)
    agent.run("Please find a remedy for hangover.")