from PIL import Image
import requests
from io import BytesIO
from dotenv import load_dotenv
import os
from smolagents import CodeAgent,LiteLLMModel


# Load environment variables from .env file
load_dotenv()

# LiteLLM for watsonx.ai Inference Engine
llm = LiteLLMModel(
    model_id="watsonx/meta-llama/llama-guard-3-11b-vision",
    # model_id="watsonx/ibm/granite-vision-3-2-2b",
    api_key=os.getenv("WATSONX_API_KEY"),
    num_ctx=8162 # Context window size
)

image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/e/e8/The_Joker_at_Wax_Museum_Plus.jpg", #Joker image
    "https://upload.wikimedia.org/wikipedia/en/9/98/Joker_%28DC_Comics_character%29.jpg" #Joker image
]

images = []

for url in image_urls:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    images.append(image)


#Instantiate the agent
agent = CodeAgent(
    tools=[],
    model=llm,
    max_steps=20,
    verbosity_level=2
)


response = agent.run(
    """
    Describe the costume and makeup that the comic character in these photos is wearing and return the description.
    Tell me if the guest is The Joker or Wonder Woman.
    """,
    images=images
)

print(response)