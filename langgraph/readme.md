https://github.com/IBM/watsonx-developer-hub/tree/main/agents

https://github.ibm.com/Dheeraj-Arremsetty/Langgraph-Agents-wx.ai/tree/main

we are using langraph library (one of the many options beside Bee/CrewAI)
https://blog.langchain.dev/langgraph-multi-agent-workflows/
https://github.com/IBM/watson-machine-learning-samples/blob/master/cloud/notebooks[…]port%20for%20tools%20to%20perform%20simple%20calculations.ipynb
https://www.ibm.com/new/announcements/build-and-deploy-agents-to-watsonx-ai-from-your-ide


if there’s a high-level comparison somewhere of key differences between BeeAI’s approach to agents vs. other frameworks like LangGraph, CrewAI, LlamaIndex?

We've heard feedback that langgraph often is powerful, but sometimes too low level. Crew.ai is often very easy to get started, but too opinionated for production use cases.
BeeAI framework is trying to be in the goldilocks zone, where we are attempting to be at the right level of abstraction to make it easy to get started, but be less opinionated to support more complex use cases.

the challenge with existing agent frameworks is they're either too rigid or too complex:
CrewAI is great for beginners but quickly falls apart in production - it forces you into predefined workflows and lacks flexibility
LangGraph gives you ultimate low-level control, but requires writing tons of code for even simple agent interactions
LlamaIndex is mostly focused on document retrieval, not dynamic agent reasoning
BeeAI is designed to be the "just right" framework:
Flexible enough for complex, real-world AI workflows
Simple enough that you can get started quickly
Modular by design, so you can plug and play components
Our north star is giving developers a framework that adapts to their needs, not forcing them to adapt to the framework's limitations. We're still very much evolving, and eager to hear from developers about what they actually need in an agent framework!

https://www.relari.ai/blog/ai-agent-framework-comparison-langgraph-crewai-openai-swarm

https://github.ibm.com/conversational-ai/langgraph-mcp

https://developer.ibm.com/tutorials/awb-handle-remote-tool-calling-model-context-protocol/

https://www.ibm.com/watsonx/developer/agents/quickstart/


https://python.langchain.com/docs/integrations/chat/ibm_watsonx/


https://github.ibm.com/tech-garage-canada/agentic-ai-pilot

