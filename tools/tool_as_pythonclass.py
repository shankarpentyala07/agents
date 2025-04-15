from smolagents import CodeAgent , Tool, LiteLLMModel

import os
from dotenv import load_dotenv

load_dotenv()


# LiteLLM for watsonx.ai Inference Engine
llm = LiteLLMModel(
    model_id="watsonx/meta-llama/llama-3-3-70b-instruct",
    api_key=os.getenv("WATSONX_API_KEY"),
    num_ctx=8162 # Context window size
)


class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description= """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""

    inputs = {
        "category": {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic Gotham').",
        }
    }

    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysteripus masquerade where guests dress as classic Batman villains",
            "futuristic Gotham": "Neo-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets."
        }

        return themes.get(category.lower(), "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic Gotham'.")
    
party_theme_tool = SuperheroPartyThemeTool()

agent = CodeAgent(tools=[party_theme_tool], model=llm)

# Run the agent to generate a party theme idea
result = agent.run(
    "What would be a good superhero party idea for a 'villain masquerade' theme?"
)

print(result)