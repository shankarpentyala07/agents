from langchain.agents import load_tools
from smolagents import  CodeAgent, HfApiModel, Tool

search_tool = Tool.from_langchain(load_tools(["serpapi"])[0])

agent=CodeAgent(tools=[search_tool], model=model)
agent.run("Search for luxury entertainment ideas for a superhero-themed event, such as live performances and interactive experiences.")