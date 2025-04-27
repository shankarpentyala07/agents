import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Sequence
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain_ibm import WatsonxLLM

from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods

from langgraph.graph import END, StateGraph

import functools

# Display Graph imports
from PIL import Image
from io import BytesIO


# Setting Up Environment Variables
load_dotenv()


# Define the agent state
# The AgentState class defines the state structure that each agent node will use. It keeps track of the messages, the sender, and the user’s query
class AgentState(TypedDict):
    messages: Sequence[AIMessage]
    sender: str
    user_query: str

# Initializing Tools and Modules 
# Tool Initialization for the Researcher (Agent).Initializes the Tavily Search tool to fetch up to 5 results from the web. This will be used by the Researcher agent later.

tavily_tool = TavilySearchResults(max_results=5)

# Watsonx LLM Setup
parameters = {
    GenParams.DECODING_METHOD: DecodingMethods.SAMPLE.value,
    GenParams.MAX_NEW_TOKENS: 100,
    GenParams.MIN_NEW_TOKENS: 50,
    GenParams.TEMPERATURE: 0.7,
    GenParams.TOP_K: 50,
    GenParams.TOP_P: 1
}

#Loading API keys
watsonx_api_key = os.getenv("WATSONX_API_KEY")
project_id = os.getenv("WATSONX_PROJECT_ID")
url = os.getenv("WATSONX_URL")

# Defining LLM
# Initializes the Creator agent’s language model using WatsonxLLM. It sets up the model ID and API credentials.
llm_creator = WatsonxLLM(
    model_id="meta-llama/llama-3-3-70b-instruct",
    url=url,
    apikey=watsonx_api_key,
    project_id=project_id,
    params=parameters
)

# Set up the routers agent language model
llm_router = WatsonxLLM(
    model_id="meta-llama/llama-3-3-70b-instruct",
    url=url,
    apikey=watsonx_api_key,
    project_id=project_id,
    params=parameters
)

# Defining Agent Nodes
# Router Agent Node 
"""
The Router agent analyzes the user query and determines which agent (Researcher or Creator) should handle it. It uses a language model to make this decision and updates the state accordingly.
"""

def router_agent_node(state, name):
    query = state["messages"][-1].content
    # Very Important router_prompt 
    router_prompt = (
        "You are a router agent who must choose between two specialists:\n"
        "  • Researcher: uses the internet to provide up-to-date information (news, real-time data, statistics, recent research).\n"
        "  • Creator: generates content based on the model's internal knowledge (conceptual explanations, creativity, general advice) **without** access to the web.\n\n"
        "Evaluate the user's request and respond with a single word: **Researcher** or **Creator**.\n\n"
        f"User request: «{query}»\n"
        "Answer:"
    )
    selected_agent = llm_router.invoke(router_prompt).strip().lower()
    if 'researcher' in selected_agent:
        selected_agent = 'Researcher'
    elif 'creator' in selected_agent:
        selected_agent = 'Creator'
    else:
        raise ValueError(f"Unexpected agent response: {selected_agent}")
    
    return {
        "messages": [AIMessage(content=f"Router Agent: Selected {selected_agent}", name=name)],
        "sender": name,
        "selected_agent": selected_agent,
        "user_query": query,
    }

# Researcher Agent Node - The Researcher agent uses the Tavily tool to fetch updated information based on the user query. It returns the search results as its response
def researcher_agent_node(state, name):
    query = state["user_query"]
    search_results = tavily_tool.invoke(query)
    result = f"Researcher Agent: Fetched search results for '{query}': {search_results}"
    return {
        "messages": [AIMessage(content=result, name=name)],
        "sender": name,
    }

# Creator Agent Node - The Creator agent uses the language model to generate a response to the user query based on general knowledge.
def creator_agent_node(state, name):
    query = state["user_query"]
    creator_prompt = f"Please answer the following query: {query}"
    result = llm_creator.invoke(creator_prompt)
    return {
        "messages": [AIMessage(content=f"Creator Agent: {result}", name=name)],
        "sender": name,
    }

# Setting up the workflow - Define the graph and its nodes

# Define nodes for each agent
research_node = functools.partial(researcher_agent_node, name="Researcher")
creator_node = functools.partial(creator_agent_node, name="Creator")

# Define the graph and its nodes - Defines the workflow and adds nodes for each agent.
workflow = StateGraph(AgentState)
workflow.add_node("Router", functools.partial(router_agent_node, name="Router"))
workflow.add_node("Researcher", research_node)
workflow.add_node("Creator", creator_node)

# Adding conditional edges
def extract_selected_agent(state) -> str:
    return state["selected_agent"]

# Add conditional edges based on the Router agent's response - directing the flow to either the Researcher or Creator node.
workflow.add_conditional_edges("Router", extract_selected_agent, {"Researcher": "Researcher", "Creator": "Creator"})

# After either Researcher or Creator is done, the program ends
workflow.add_conditional_edges("Researcher", lambda state: "__end__", {"__end__": END})
workflow.add_conditional_edges("Creator", lambda state: "__end__", {"__end__": END})

# Set entry point
workflow.set_entry_point("Router")

# Compiling the workflow - Compiles the workflow, turning it into an executable state machine. This step is necessary to make the workflow operational and capable of handling dynamic paths.
graph = workflow.compile()

# Displaying the architecture
def display_architecture():
    try:
        #display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
        #diagram_path = graph.get_graph(xray=True).draw_mermaid_png()
        # Get the diagram image as bytes
        diagram_bytes = graph.get_graph(xray=True).draw_mermaid_png()
        # Open and show the image using PIL
        #img = Image.open(diagram_path)
        # Wrap bytes in BytesIO so PIL can open it

        img = Image.open(BytesIO(diagram_bytes))
        img.show()
    except Exception as e:
        print("Unable to display graph architecture. Extra dependencies might be missing.")
        print(f"Error details: {e}")

# This function displays the architecture of the workflow using a mermaid diagram. It provides a visual representation of how the nodes and edges connect
display_architecture()

# Evaluating the system - Evaluates user messages, routes them through the system, and prints the output step by step
def evaluate_message(message: str):
    try:
        events = graph.stream(
            {"messages": [HumanMessage(content=message)]},
            {"recursion_limit": 50}
        )
        for s in events:
            print(s)
            print("-----")
        print("Final")
    except Exception as e:
        print(f"Error during evaluation: {e}")

# Example Usage
# evaluate_message("Fetch the bitcoin price over the past 5 days.") # Researcher case

# evaluate_message("Explain what Bitcoin is.") # Creator case

evaluate_message("What is the current bitcoin price")


