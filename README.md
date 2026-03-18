🚀 Autonomous Multi-Agent Code Intelligence System

An Agentic AI system that analyzes software repositories to detect bugs, security vulnerabilities, and code issues using multi-agent reasoning, Retrieval-Augmented Generation (RAG), AST-based analysis, and tool-driven workflows.

🧠 Overview

This project demonstrates how modern AI systems combine LLMs, vector search, and static analysis to build an autonomous code review system.

The system:

Understands repository code using semantic search (RAG)

Uses a Planner Agent to orchestrate analysis

Runs specialized agents for bug & security detection

Verifies results using a Reflection Agent

Suggests fixes using a Fix Agent

🏗️ Architecture
Repository
   ↓
Code Ingestion
   ↓
Chunking + Embeddings
   ↓
Chroma Vector DB
   ↓
Planner Agent
   ↓
Security Agent + Bug Agent
   ↓
Reflection Agent
   ↓
Fix Agent
   ↓
Final Report
⚙️ Features
🔹 Multi-Agent Architecture

Planner Agent (decision making)

Security Agent (vulnerability detection)

Bug Agent (logic & syntax issues)

Reflection Agent (validation layer)

Fix Agent (patch suggestions)

🔹 Retrieval-Augmented Generation (RAG)

Repository → chunking → embeddings → vector DB

Semantic search for relevant code retrieval

🔹 AST-Based Code Analysis

Syntax error detection

Function & structure extraction

Static analysis without LLM dependency

🔹 Tool-Driven Agents

Agents use tools instead of only LLM reasoning:

Syntax checker (AST)

Infinite loop detection

SQL injection detection

Hardcoded secret detection

🔹 Multi-LLM Routing

Primary: Google Gemini

Fallback: Groq (LLaMA models)

🔹 Reflection Layer

Validates findings

Removes false positives

Combines results into final report

🔹 Fix Suggestions (Patch-Based)

Suggests minimal fixes (not full rewrite)

Provides explanation + patch

## 🔄 Agent Workflow

```text
Step 1 → query_chunks (retrieve relevant code)
Step 2 → security_agent (detect vulnerabilities)
Step 3 → bug_agent (detect logical issues)
Step 4 → reflection_agent (validate results)
Step 5 → fix_agent (suggest fixes)
Step 6 → finish (final output)
```
📁 Project Structure
```text
repo-intelligence-ai
│
├── app
│   ├── agents
│   │   ├── planner_agent.py
│   │   ├── specialists
│   │   │   ├── security_agent.py
│   │   │   ├── bug_agent.py
│   │   │   ├── reflection_agent.py
│   │   │   └── fix_agent.py
│   │
│   ├── llm
│   │   ├── gemini_client.py
│   │   ├── groq_client.py
│   │   └── llm_router.py
│   │
│   ├── tools
│   │   ├── ast_parser.py
│   │   ├── query_chunks.py
│   │   └── analysis
│   │       ├── security_tools.py
│   │       └── bug_tools.py
│   │
│   ├── ingestion
│   │   ├── loader.py
│   │   └── chunker.py
│
└── main.py
```
🛠️ Tech Stack

Languages:
Python

AI & LLM:
Gemini API, Groq (LLaMA), Prompt Engineering, RAG

AI Architecture:
Multi-Agent Systems, Agentic Workflow, Tool-based Agents

Vector Database:
ChromaDB

Code Analysis:
AST Parsing, Static Analysis

Backend (Optional Extension):
FastAPI

▶️ How to Run
1️⃣ Clone Repository
git clone <your-repo-url>
cd repo-intelligence-ai
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Set Environment Variables

Create .env file:

GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
4️⃣ Run the Project
python main.py
5️⃣ What Happens Internally

Repository is scanned

Code is chunked & embedded

Stored in ChromaDB

Planner agent starts execution

Agents analyze + verify + suggest fixes

📊 Example Output
Security Findings:
No vulnerabilities detected.

Bug Findings:
Syntax error in authentication module.

Reflection:
Verified issue → indentation error

Fix Suggestion:
- Fix indentation in login function
- Ensure proper block structure
⚠️ Edge Cases Handled

Empty retrieval results

Repeated agent loops

LLM malformed JSON responses

Token limit issues

False positives (handled by reflection agent)

🚀 Future Improvements

GitHub PR integration (auto review)

AST-based code patching

UI dashboard for results

Multi-language support

CI/CD integration

🎯 Project Goals

This project demonstrates how to build:

Autonomous AI agents

Tool-driven reasoning systems

Hybrid LLM + static analysis pipelines

Scalable AI architectures

⭐ Why This Project Is Unique

Unlike basic AI projects, this system combines:

Multi-agent orchestration

RAG + vector search

AST-based analysis

Reflection-based validation

Fix suggestion system

👉 Making it closer to real-world AI engineering systems

📌 One-Line Description

An autonomous multi-agent AI system that analyzes software repositories using RAG, AST parsing, and LLM reasoning to detect bugs, security issues, and suggest fixes.