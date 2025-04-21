
### LlamaIndex is a complete toolkit for creating LLM-powered agents over your data using indexes and workflows.
* There are 3 main concepts of LlamaIndex - Components, Agents and Tools and Workflows
* Components: Are the basic building blocks you use in LlamaIndex. These include things like prompts, models, and databases. Components often help connect LlamaIndex with other tools and libraries.
* Tools: Tools are components that provide specific capabilities like searching, calculating, or accessing external services. They are the building blocks that enable agents to perform tasks
* Agents: Agents are autonomous components that can use tools and make decisions. They coordinate tool usage to accomplish complex goals.
* Workflows: Are step-by-step processes that process logic together. Workflows or agentic workflows are a way to structure agentic behaviour without the explicit use of agents.

### What Makes LlamaIndex Special?

* Clear Workflow System: Workflows help break down how agents should make decisions step by step using an event-driven and async-first syntax. This helps you clearly compose and organize your logic.
* Advanced Document Parsing with LlamaParse: LlamaParse was made specifically for LlamaIndex, so the integration is seamless, although it is a paid feature.
* Many Ready-to-Use Components: LlamaIndex has been around for a while, so it works with lots of other frameworks. This means it has many tested and reliable components, like LLMs, retrievers, indexes, and more.
* LlamaHub: is a registry of hundreds of these components, agents, and tools that you can use within LlamaIndex.

### LlamaHub

* LlamaHub is a registry of hundreds of integrations, agents and tools that you can use within LlamaIndex.

* URL - https://llamahub.ai/

### Installation

* Most of the installation commands generally follow an easy-to-remember format

```
pip install llama-index-{component-type}-{framework-name}
```

Example:

* To install the dependencies for an LLM and embedding component using the Hugging Face inference API integration - https://llamahub.ai/l/llms/llama-index-llms-huggingface-api?from=llms

```
pip install llama-index-llms-huggingface-api llama-index-embeddings-huggingface
```

* To use IBM watsonx.ai foundation models - https://docs.llamaindex.ai/en/stable/examples/llm/ibm_watsonx/ .WatsonxLLM is a wrapper for IBM watsonx.ai foundation models. - Sample Code File - intro_watsonxai.py

```
!pip install -qU llama-index-llms-ibm
```

### What are components in LlamaIndex?

* LlamaIndex has many components, we’ll focus specifically on the `QueryEngine` component. Why? Because it can be used as a `Retrieval-Augmented Generation (RAG)` tool for an agent . 

* RAG - LLMs are trained on enormous bodies of data to learn general knowledge. However, they may not be trained on relevant and up-to-date data. RAG solves this problem by finding and retrieving relevant information from your data and giving that to the LLM.

* `QueryEngine` is a key component for building `agentic RAG workflows` in LlamaIndex. Any agent needs a way to find and understand relevant data. The QueryEngine provides exactly this capability.

### Creating a RAG pipeline using components

There are five key stages within RAG , which in turn will be a part of most larger applications. These are:

* Loading: this refers to getting your data from where it lives — whether it’s text files, PDFs, another website, a database, or an API — into your workflow. LlamaHub provides hundreds of integrations to choose from.

* Indexing: this means creating a data structure that allows for querying the data. For LLMs, this nearly always means creating vector embeddings. Which are numerical representations of the meaning of the data. Indexing can also refer to numerous other metadata strategies to make it easy to accurately find contextually relevant data based on properties.

* Storing: once your data is indexed you will want to store your index, as well as other metadata, to avoid having to re-index it.

* Querying: for any given indexing strategy there are many ways you can utilize LLMs and LlamaIndex data structures to query, including sub-queries, multi-step queries and hybrid strategies.

* Evaluation: a critical step in any flow is checking how effective it is relative to other strategies, or when you make changes. Evaluation provides objective measures of how accurate, faithful and fast your responses to queries are.

### Let’s reproduce these stages using components: 

* Loading and embedding documents: LlamaIndex can work on top of your own data, however, before accessing data, we need to load it. There are three main ways to load data into LlamaIndex:

* `SimpleDirectoryReader`: A built-in loader for various file types from a local directory
* `LlamaParse`:  LlamaParse, LlamaIndex’s official tool for PDF parsing, available as a managed API. - https://github.com/run-llama/llama_cloud_services/blob/main/parse.md
* `LlamaHub`: A registry of hundreds of data-loading libraries to ingest data from any source. - https://docs.llamaindex.ai/en/stable/module_guides/loading/connector/


* The simplest way to load data is with SimpleDirectoryReader. This versatile component can load various file types from a folder and convert them into Document objects that LlamaIndex can work with.

* After loading our documents, we need to break them into smaller pieces called Node objects. A Node is just a chunk of text from the original document that’s easier for the AI to work with, while it still has references to the original Document object.The IngestionPipeline helps us create these nodes through two key transformations.

* SentenceSplitter breaks down documents into manageable chunks by splitting them at natural sentence boundaries.
* HuggingFaceEmbedding converts each chunk into numerical embeddings - vector representations that capture the semantic meaning in a way AI can process efficiently or use watsonx.ai embeddings
* For watsonx.ai embeddings - https://docs.llamaindex.ai/en/stable/examples/embeddings/ibm_watsonx/
* Storing and indexing documents - After creating our Node objects we need to index them to make them searchable , as a sample chromadb can e used , Milvus can also be used . Different vector stores: https://docs.llamaindex.ai/en/stable/module_guides/storing/vector_stores/
* vector embeddings - by embedding both the query and nodes in the same vector space, we can find relevant matches. The VectorStoreIndex handles this for us, using the same embedding model we used during ingestion to ensure consistency.
* Querying a VectorStoreIndex with prompts and LLMs - Before we can query our index, we need to convert it to a query interface. The most common conversion options are

* as_retriever: For basic document retrieval, returning a list of NodeWithScore objects with similarity scores
* as_query_engine: For single question-answer interactions, returning a written response
* as_chat_engine: For conversational interactions that maintain memory across multiple messages, returning a written response using chat history and indexed context

* The query engine is more common for agent-like interactions.

### Response Processing:

* Under the hood, the query engine doesn’t only use the LLM to answer the question but also uses a ResponseSynthesizer as a strategy to process the response. Once again, this is fully customisable but there are three main strategies that work well out of the box:

* refine: create and refine an answer by sequentially going through each retrieved text chunk. This makes a separate LLM call per Node/retrieved chunk.
* compact (default): similar to refining but concatenating the chunks beforehand, resulting in fewer LLM calls.
* tree_summarize: create a detailed answer by going through each retrieved text chunk and creating a tree structure of the answer.
* Take fine-grained control of your query workflows with the low-level composition API (https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/usage_pattern/#low-level-composition-api). This API lets you customize and fine-tune every step of the query process to match your exact needs, which also pairs great with Workflows (https://docs.llamaindex.ai/en/stable/module_guides/workflow/)
* The language model won’t always perform in predictable ways, so we can’t be sure that the answer we get is always correct. We can deal with this by evaluating the quality of the answer.

### Evaluation and observability:
* LlamaIndex provides built-in evaluation tools to assess response quality. These evaluators leverage LLMs to analyze responses across different dimensions. Let’s look at the three main evaluators available:

* FaithfulnessEvaluator: Evaluates the faithfulness of the answer by checking if the answer is supported by the context.
* AnswerRelevancyEvaluator: Evaluate the relevance of the answer by checking if the answer is relevant to the question.
* CorrectnessEvaluator: Evaluate the correctness of the answer by checking if the answer is correct.

### Even without direct evaluation, we can gain insights into how our system is performing through observability. This is especially useful when we are building more complex workflows and want to understand how each component is performing. (LlamaTrace)


### Using Tools in LlamaIndex
* Defining a clear set of Tools is crucial to performance.clear tool interfaces are easier for LLMs to use.Much like a software API interface for human engineers, they can get more out of the tool if it’s easy to understand how it works.
* There are `four` main types of `tools` in `LlamaIndex`:

* FunctionTool (f(x)) - convert any python function into a tool that an agent can use. It automatically figures out how the function works.
* SearchEngine - A tool that let's agent use query engines.Since agents are built on query engines, they can also use other agents as tools.
* ToolSpecs - Set of tools created by the community, which often include tools for specific services like Gmail.
* Utility Tools - Special tools that help handle large amounts of data from other tools


### Creating a FunctionTool
* A FunctionTool provides a simple way to wrap any Python function and make it available to an agent. You can pass either a synchronous or asynchronous function to the tool, along with optional name and description parameters. The name and description are particularly important as they help the agent understand when and how to use the tool effectively.

### Creating a QueryEngineTool
* The QueryEngine we defined in the previous unit can be easily transformed into a tool using the QueryEngineTool class.

### ToolSpecs:
* Think of ToolSpecs as collections of tools that work together harmoniously - like a well-organized professional toolkit. Just as a mechanic’s toolkit contains complementary tools that work together for vehicle repairs, a ToolSpec combines related tools for specific purposes. For example, an accounting agent’s ToolSpec might elegantly integrate spreadsheet capabilities, email functionality, and calculation tools to handle financial tasks with precision and efficiency.

### Model Context Protocol (MCP) in LlamaIndex

* LlamaIndex also allows using MCP tools through a ToolSpec on the LlamaHub (https://llamahub.ai/l/tools/llama-index-tools-mcp?from=). You can simply run an MCP server and start using it through the following implementation.

### Utility Tools
* Oftentimes, directly querying an API can return an excessive amount of data, some of which may be irrelevant, overflow the context window of the LLM, or unnecessarily increase the number of tokens that you are using.

* OnDemandToolLoader: This tool turns any existing LlamaIndex data loader (BaseReader class) into a tool that an agent can use. The tool can be called with all the parameters needed to trigger load_data from the data loader, along with a natural language query string. During execution, we first load data from the data loader, index it (for instance with a vector store), and then query it ‘on-demand’. All three of these steps happen in a single tool call.
* LoadAndSearchToolSpec: The LoadAndSearchToolSpec takes in any existing Tool as input. As a tool spec, it implements to_tool_list, and when that function is called, two tools are returned: a loading tool and then a search tool. The load Tool execution would call the underlying Tool, and the index the output (by default with a vector index). The search Tool execution would take in a query string as input and call the underlying index.

* key points:
1.  `QueryEngine` is a component that finds and retrieves relevant information as part of the RAG process.
2.  `FunctionTools` wrap Python functions to make them accessible to agents.
3. `Toolspecs` allow the community to share and reuse tools.
4. To create a tool only `function` is required. The name and description default to the name and docstring from the provided function

### Using Agents in LlamaIndex:

* An Agent is a system that leverages an AI model to interact with its environment to achieve a user-defined objective. It combines reasoning, planning, and action execution (often via external tools) to fulfil tasks.

* LlamaIndex supports three main types of reasoning agents:

* `Function Calling Agents` - These work with AI models that can call specific functions.
* `ReAct Agents` - These can work with any AI that does chat or text endpoint and deal with complex reasoning tasks. ReAct agents are also good at complex reasoning tasks and can work with any LLM that has chat or text completion capabilities. They are more verbose, and show the reasoning behind certain actions that they take.
* `Advanced Custom Agents` - These use more complex methods to deal with more complex tasks and workflows.

### Agentic workflows in LlamaIndex:

* A workflow in LlamaIndex provides a structured way to organize your code into sequential and manageable steps.Such a workflow is created by defining Steps which are triggered by Events, and themselves emit Events to trigger further steps

* Workflows offer several key benefits:
    * Clear organization of code into discrete steps
    * Event-driven architecture for flexible control flow
    * Type-safe communication between steps
    * Built-in state management
    * Support for both simple and complex agent interactions
* workflows strike a great balance between the autonomy of agents while maintaining control over the overall workflow.



Reference Links:
https://github.com/huggingface/agents-course/tree/main/units/en/unit2/llama-index
https://medium.com/@ashgadag/llamaindex-agentic-rag-leveraging-ibm-watsonx-ai-4dbf9b5fda2d
https://www.ibm.com/think/tutorials/llamaindex-rag



