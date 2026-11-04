# Agent design

The planned supervisor will be a LangGraph workflow. It will coordinate specialized agents such as personal assistance, morning briefing, and reflection while keeping workflow state separate from durable memory.

Each agent receives narrowly scoped tools. Model selection and Ollama access will move behind the Model Service so local and hosted models can be changed without rewriting agent logic.
