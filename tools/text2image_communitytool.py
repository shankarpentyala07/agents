from smolagents import load_tool, CodeAgent , LiteLLMModel
import os
from dotenv import load_dotenv

load_dotenv()

# LiteLLM for watsonx.ai Inference Engine
llm = LiteLLMModel(
    model_id="watsonx/meta-llama/llama-3-3-70b-instruct",
    api_key=os.getenv("WATSONX_API_KEY"),
    num_ctx=8162 # Context window size
)

image_generation_tool = load_tool(
    "m-ric/text-to-image",
    trust_remote_code=True
)


agent = CodeAgent(
    tools=[image_generation_tool],
    model=llm
)

agent.run("Generate an image of a luxurious superhero-themed party at Wayne Manor with made-up superheros.")