# Atlas of Tesseract City — System Overview

**Atlas of Tesseract City** is a private, autonomous knowledge base and intelligence engine residing directly within Google Drive (`__marinus__`).

## 🌌 Core Philosophy & Purpose
The system orchestrates multi-agent knowledge engineering:
- Ingests raw media assets, documents, notes, code scripts, and color palettes from the **Input/** queue.
- Synthesizes Wikipedia-grade interconnected HTML articles with Mermaid.js architecture diagrams and bidirectional backlinks.
- Employs an **Incremental Short-Turn Pipeline**: writes synthesized articles to Google Drive immediately per turn, avoiding single-point-of-failure loops.
- Employs an **Activity Log Memory Engine**: inspects cycle logs and historical archives to prevent repetitive resizing loops and gracefully recover from Gemini 503 high-demand interruptions.
- Guarantees **Zero Orphaned Media**: 100% of processed graphics, heraldic emblems, color swatches, screenshots, and infographics are cataloged and embedded.
- Bridges to **External Knowledge Sinks**: mirrors content to Google NotebookLM via persistent in-place Google Docs & companion markdown, Notion via rich semantic blocks, and GitHub Pages.

## 🏛️ Invariant Guardrails
1. **Titan Atlas**: Embodying cosmic stewardship and deterministic execution.
2. **Deterministic Rules Hierarchy**: Strict compliance with AGENTS.md, .clinerules, and .github/ directives.
3. **Security Shield**: Sensitive credentials (API tokens, private keys) are automatically scrubbed; borderline ambiguous files remain in Input while questions are escalated to Questions.md.
4. **Non-Destructive Evolution**: Wiki pages are continuously synthesized and enriched—never deleted or blanked.
