# Repo Intelligence AI

**Repo Intelligence AI** is an agentic AI system designed to analyze entire software repositories, detect potential issues, and assist developers with automated code insights.

Instead of analyzing code file-by-file manually, this system ingests a repository, builds a semantic index of the codebase, and uses a **multi-agent architecture** to retrieve, analyze, and reason about code.

The goal is to create an **AI-powered code intelligence system** capable of assisting with bug detection, security analysis, and code understanding at the repository level.

---

# Project Architecture

The system is built as a modular AI pipeline:

```
Repository
   │
   ▼
Ingestion Pipeline
   │
   ▼
Code Chunking
   │
   ▼
Vector Index (Chroma)
   │
   ▼
Planner Agent (Controller)
   │
   ▼
Specialist Agents
   │
 ┌──────────────┬──────────────┐
 ▼              ▼
Security Agent  Bug Agent
   │
   ▼
Final Analysis Report
```

The **Planner Agent** acts as the orchestrator, dynamically choosing tools and delegating tasks to specialized agents.

---

# Key Features

## Multi-LLM Integration

The system integrates multiple large language models through a routing layer.

Supported providers:

* Gemini
* Groq (LLaMA)

The router automatically selects the available provider and falls back if one fails.

This architecture provides:

* reliability
* provider redundancy
* flexible model usage

---

## Retrieval Augmented Generation (RAG)

The project implements a **repository-level RAG pipeline**.

Steps:

1. Code files are scanned and loaded
2. Files are chunked into manageable segments
3. Chunks are embedded into vector representations
4. Stored in a vector database
5. Retrieved based on semantic similarity

The vector store enables the agent system to retrieve **relevant code context** before performing analysis.

Vector storage is implemented using **Chroma**.

---

## Multi-Agent Architecture

The system uses a hierarchical agent design.

### Planner Agent (Controller)

Responsibilities:

* receives the user task
* retrieves relevant code using the vector store
* decides which specialist agent should analyze the code
* maintains shared context memory
* orchestrates the analysis workflow

The planner follows a reasoning loop:

```
Think → Act → Observe → Iterate
```

---

### Security Agent

Analyzes retrieved code chunks for potential security vulnerabilities.

Examples of checks:

* unsafe authentication logic
* insecure token handling
* potential injection vulnerabilities
* insecure data handling

Outputs:

* vulnerability description
* explanation
* severity level

---

### Bug Agent

Detects logical errors and possible code bugs.

Examples:

* incorrect logic flow
* missing edge case handling
* invalid assumptions in code
* potential runtime issues

Outputs:

* bug description
* reasoning
* affected code sections

---

# Shared Context Memory

Agents collaborate using a **shared context state**.

The planner maintains structured memory:

```
context = {
  retrieved_chunks
  security_findings
  bug_findings
}
```

This allows agents to build upon previous results and improves multi-agent reasoning.

---

# Tool-Based Agent System

Agents interact with the environment through tools.

Example tools:

* `query_chunks` – retrieves relevant code from the vector database
* `security_agent` – analyzes security vulnerabilities
* `bug_agent` – analyzes logical bugs

The planner dynamically selects tools during execution.

---

# Agent Loop

The Planner Agent executes tasks through an iterative loop:

```
1. Understand the task
2. Decide which tool to use
3. Execute tool
4. Observe result
5. Update shared context
6. Continue until finished
```

This design enables **autonomous reasoning and task orchestration**.

---

# Ingestion Pipeline

The ingestion layer prepares repository data for analysis.

Components:

* Repository Cloner
* Code Scanner
* File Loader
* Code Chunker

Supported languages include:

* Python
* JavaScript
* TypeScript
* C/C++
* Go
* Rust
* Java

Large repositories are filtered to ignore unnecessary directories like:

```
node_modules
.git
dist
build
__pycache__
```

---

# Vector Database

The project uses **Chroma** as the vector database.

Chroma stores embeddings of code chunks and enables semantic retrieval.

This allows the system to search for code concepts such as:

```
authentication logic
database queries
token generation
```

instead of simple keyword matching.

---

# Project Structure

```
repo-intelligence-ai
│
├── app
│   ├── agents
│   │   ├── planner_agent.py
│   │   ├── tools.py
│   │   ├── agent_state.py
│   │   └── specialists
│   │       ├── security_agent.py
│   │       └── bug_agent.py
│   │
│   ├── indexing
│   │   ├── code_loader.py
│   │   └── vector_store.py
│   │
│   ├── tools
│   │   ├── repo_cloner.py
│   │   └── code_scanner.py
│   │
│   └── llm
│       ├── gemini_client.py
│       ├── groq_client.py
│       └── llm_router.py
│
├── chroma_db
├── repos
├── main.py
└── README.md
```

---

# Running the Project

Install dependencies:

```
pip install -r requirements.txt
```

Set API keys in `.env`:

```
GEMINI_API_KEY=your_key
GROQ_API_KEY=your_key
```

Run the agent:

```
python main.py
```

---

# Current Status

The system currently supports:

* repository ingestion
* vector-based code retrieval
* planner agent orchestration
* multi-agent analysis
* shared context memory

---

# Future Improvements

Planned features:

* Fix Suggestion Agent
* AST-based code analysis
* performance analysis agent
* GitHub PR review integration
* automated patch generation

---

# Vision

The long-term goal is to create an **AI-powered repository intelligence system** capable of understanding large codebases, detecting issues automatically, and assisting developers with intelligent code insights.
