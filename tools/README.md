agents use tools to perform various actions. In smolagents, tools are treated as functions that an LLM can call within an agent system.

To interact with a tool, the LLM needs an interface description with these key components:

* Name: What the tool is called
* Tool description: What the tool does
* Input types and descriptions: What arguments the tool accepts
* Output type: What the tool returns

Example:

* Name: web_search
* Tool description: Searches the web for specific queries
* Input: query (string) - The search term to look up
* Output: String containing the search results

### Tool Creation Methods
In smolagents, tools can be defined in two ways:

* Using the @tool decorator for simple function-based tools
* Creating a subclass of Tool for more complex functionality

### The @tool Decorator

The @tool decorator is the recommended way to define simple tools. Under the hood, smolagents will parse basic information about the function from Python. So if you name your function clearly and write a good docstring, it will be easier for the LLM to use.

Using this approach, we define a function with:

* A clear and descriptive function name that helps the LLM understand its purpose.
* Type hints for both inputs and outputs to ensure proper usage.
* A detailed description, including an Args: section where each argument is explicitly described. These descriptions provide valuable context for the LLM, so it’s important to write them carefully.


### Defining a Tool as a Python Class

This approach involves creating a subclass of Tool. For complex tools, we can implement a class instead of a Python function. The class wraps the function with metadata that helps the LLM understand how to use it effectively. In this class, we define:

* name: The tool’s name.
* description: A description used to populate the agent’s system prompt.
* inputs: A dictionary with keys type and description, providing information to help the Python interpreter process inputs.
* output_type: Specifies the expected output type.
* forward: The method containing the inference logic to execute.

### Default Toolbox
smolagents comes with a set of pre-built tools that can be directly injected into your agent. The default toolbox includes:

* PythonInterpreterTool
* FinalAnswerTool
* UserInputTool
* DuckDuckGoSearchTool
* GoogleSearchTool
* VisitWebpageTool

### Sharing and Importing Tools

One of the most powerful features of smolagents is its ability to share custom tools on the Hub and seamlessly integrate tools created by the community. This includes connecting with HF Spaces and LangChain tools

### Sharing a Tool to the Hub

Sharing your custom tool with the community is easy! Simply upload it to your Hugging Face account using the push_to_hub() method.

```
party_theme_tool.push_to_hub("{your_username}/party_theme_tool", token="<YOUR_HUGGINGFACEHUB_API_TOKEN>")
```

### Importing a Tool from the Hub

You can easily import tools created by other users using the load_tool() function

Ex: generate a promotional image for the party using AI. Instead of building a tool from scratch,leverage a predefined one from the community

### Importing a Hugging Face Space as a Tool
You can also import a HF Space as a tool using Tool.from_space(). This opens up possibilities for integrating with thousands of spaces from the community for tasks from image generation to data analysis

The tool will connect with the spaces Gradio backend using the gradio_client, so make sure to install it via pip if you don’t have it already


### Importing a LangChain Tool

we can reuse LangChain tools in your smolagents workflow!You can easily load LangChain tools using the Tool.from_langchain() method

### Importing a tool collection from any MCP server

smolagents also allows importing tools from the hundreds of MCP servers available on glama.ai or smithery.ai.
https://glama.ai/mcp/servers
https://smithery.ai/


