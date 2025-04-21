from llama_index.core.tools import FunctionTool
"""
A FunctionTool provides a simple way to wrap any Python function and make it available to an agent. You can pass either a synchronous or asynchronous function to the tool, along with optional name and description parameters. The name and description are particularly important as they help the agent understand when and how to use the tool effectively. Let’s look at how to create a FunctionTool below and then call it.

When using an agent or LLM with function calling, the tool selected (and the arguments written for that tool) rely strongly on the tool name and description of the purpose and arguments of the tool.
"""

def get_weather(location: str) -> str:
    """Useful for getting the weather for a given location."""
    print(f"Getting weather for {location}")
    return f"The weather in {location} is sunny"

tool = FunctionTool.from_defaults(
    get_weather,
    name="my_weather_tool",
    description="Useful for getting the weather for a given location."
)

tool.call("New York")