# Architecture

Personal AI OS is organized as independently deployable services around a shared configuration layer. Clients such as the robot UI, mobile app, and dashboard communicate with a supervisor agent or service APIs; they do not own assistant state.

The first bounded context is long-term memory. Its API is deliberately independent of any LLM framework so that LangGraph and LangChain can be added as consumers without coupling persistence to an orchestration library.

## Intended flow

```text
Client → Supervisor / agent workflow → Memory Service → PostgreSQL + pgvector
                                  ↘ Model Service → Ollama
```

Short-term conversational state will live in LangGraph checkpoints. The Memory Service owns durable semantic, episodic, procedural, and preference memories.
