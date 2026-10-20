# System Architecture & Folder Hierarchy

```text
Atlas_of_Tesseract_City/ (__marinus__)
├── README.md                  # Root workspace overview & GitHub-style documentation
├── CHANGELOG.md               # Keep-a-Changelog autonomous version & batch history
├── INGESTION_CHRONICLE.md     # Temporal truth ledger tracking source timestamps
├── AGENTS.md                  # Master dense machine specification
├── TODO                       # Priority task queue (erased as completed)
├── Questions.md               # User escalation rules firewall
├── GEMINI.md                  # Alias pointer
├── .clinerules                # IDE rules pointer
├── YYYY-MM-DD_HH-mm-ss.md     # Timestamped monolithic snapshots per cycle
├── [MASTER_MONOLITH] Tesseract City Wiki.md # Companion markdown for NotebookLM
├── [MASTER_MONOLITH] Tesseract City Wiki    # Persistent Google Doc (.gdoc) for NotebookLM
│
├── Input/                     # Drop zone for incoming notes, scripts, images
│
├── Output/                    # Immutable history organized by ingestion date
│   └── YYYY-MM-DD/            # Archived original source files
│
├── Wiki/                      # Standalone hostable website & GitHub Pages root
│   ├── index.html             # Website home portal & master registry
│   ├── css/style.css          # Tesseract City cyberpunk typography & layout
│   ├── js/wiki.js             # Client scripts, code downloaders, search engine
│   ├── templates/article.html # Canonical page template
│   ├── Images/                # Web-optimized image assets (1200px max)
│   ├── graph.json             # Interactive 2D knowledge graph dataset
│   ├── search-index.json      # Client-side full-text search index
│   └── .github/workflows/     # deploy-wiki.yml for GitHub Pages
│
├── Docs/                      # Dynamic system documentation (Overwritten with latest app specs)
│   ├── Overview.md            # High-level system overview & pillars
│   ├── Architecture.md        # Folder hierarchy & subsystem data flows
│   ├── User_Guide.md          # Step-by-step operator workflows
│   └── MCP_and_Memory.md      # Model Context Protocol & Mem0 cognitive memory
│
├── .github/                   # Autonomous agent configuration & skills
│   ├── agents/atlas.agent.md  # Titan Atlas persona & voice
│   ├── copilot-instructions.md# VS Code Copilot alignment
│   ├── instructions/          # Domain instructions
│   └── Skills/                # Modular skills (synthesis, mermaid, code, github)
│
└── .vscode/                   # Developer workspace configuration
    ├── settings.json          # IDE settings
    ├── tasks.json             # Pipeline runners
    ├── mcp.json               # Model Context Protocol servers & lifecycle hooks
    └── tasks/run_pipeline.py  # Automation script
```
