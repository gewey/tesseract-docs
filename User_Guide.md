# Atlas User Manual & Operator Guide

### 1. Ingesting Files & Assets
- Drop files, documents, scripts, or graphics into **Input/** (or drag-and-drop into the Activity Console).
- Atlas will analyze the content, synthesize Wikipedia-grade articles in **Wiki/**, and immediately archive sources to **Output/YYYY-MM-DD/**.
- **Short-Turn Resilience**: Large batches of files are processed in short incremental turns. Finished turns are committed to Drive immediately; if a high-demand error occurs, completed work is never repeated.

### 2. Activity Log Memory & Loop Protection
- If an upstream model spike occurs (e.g. Gemini 503 high demand), the Log Memory Engine checks the console logs and output archive at the start of every cycle.
- Already-archived images and processed documents are automatically recognized, preventing redundant resizing or duplicate operations.

### 3. Assigning Priority Tasks
- Add bulleted items to the root **TODO** file.
- Atlas executes tasks in **TODO** *before* ingesting files in Input, erasing completed tasks upon verified execution.

### 4. Answering Questions & Rule Escalations
- Check **Questions.md**. When Atlas encounters ambiguous data or potential credentials, it escalates an inquiry.
- Add your answer below `A:`. That answer becomes a permanent binding operational rule!

### 5. Google NotebookLM & Notion Sinks
- **NotebookLM**: Open the Integrations modal to connect the persistent Master Google Doc (`[MASTER_MONOLITH] Tesseract City Wiki`) or companion markdown file. The Drive pointer remains constant, enabling in-place source syncing.
- **Notion**: Mirror synthesized knowledge directly into Notion using semantic blocks (headers, callouts, code blocks, bulleted lists).
