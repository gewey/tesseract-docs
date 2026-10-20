# Model Context Protocol (MCP) & Mem0 Cognitive Memory

Titan Atlas incorporates the Model Context Protocol (MCP) to connect external intelligence systems and long-term memory.

## Configuration (`.vscode/mcp.json`)
The workspace configuration defines HTTP MCP servers and automated lifecycle hooks:
- `cycle_start`: Automated queries (e.g. Mem0 `search_memories`) to load historical architectural context into the agent's prompt.
- `turn_start` / `turn_end`: Granular short-turn lifecycle triggers.
- `cycle_end`: Automated recording (e.g. Mem0 `add_memory` to persist batch summaries; Notion `sync_wiki_pages` to mirror pages).

## Injected Cognitive Context
Memories returned by MCP servers are injected directly into the Gemini prompt under `## 🧠 Mem0 / MCP Long-Term Memories Injected`, ensuring the model never suffers from amnesia across restarts.
