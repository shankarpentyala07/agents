### Tool Calling Agent

### Setup

* create .env file with below variables

```
WATSONX_API_KEY=""
WATSONX_PROJECT_ID=""
WATSONX_URL=""
```

* Create a virtual environment and install packages `pip install -r requirements.txt`

* To run party planner agent `python3 main.py`

### ToolCallingAgent is a combination of smolagent + IBM watsonx.ai + LiteLLM unified api engine

Notes:

When you examine the agent’s trace, instead of seeing Executing parsed code:, you’ll see something like:

```
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Calling tool: 'web_search' with arguments: {'query': "best music recommendations for a party at Wayne's         │
│ mansion"}                                                                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────```

The agent generates a structured tool call that the system processes to produce the output, rather than directly executing code like a CodeAgent.