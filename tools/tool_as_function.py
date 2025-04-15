from smolagents import CodeAgent , tool, LiteLLMModel

import os
from dotenv import load_dotenv

load_dotenv()

@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.

    Args:
       query: A search term for finding catering services
    """

    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }

    best_service = max(services, key=services.get)

    return best_service


# LiteLLM for watsonx.ai Inference Engine
llm = LiteLLMModel(
    model_id="watsonx/meta-llama/llama-3-3-70b-instruct",
    api_key=os.getenv("WATSONX_API_KEY"),
    num_ctx=8162 # Context window size
)

agent = CodeAgent(tools=[catering_service_tool],model=llm)

result = agent.run(
    "Can you give me the name of the highest-rated catering service in Gotham City?"
)

print(result)