![Python](https://img.shields.io/badge/Python-3.11-blue)
![Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent-purple)
![RAG](https://img.shields.io/badge/RAG-ChromaDB-green)
![LLM](https://img.shields.io/badge/LLM-Gemini%20%7C%20Groq-orange)
![Status](https://img.shields.io/badge/Status-Active-success)




🚀 Autonomous Multi-Agent Code Intelligence System

An autonomous AI system that analyzes software repositories using multi-agent reasoning, RAG, AST parsing, and LLM orchestration to detect bugs, security issues, and suggest fixes.

🧠 Overview

This project demonstrates a real-world Agentic AI system that combines:

Multi-Agent Systems

Retrieval-Augmented Generation (RAG)

Static Code Analysis (AST)

Tool-driven reasoning

Reflection-based validation

Unlike basic AI apps, this system mimics modern AI engineering pipelines.

🏗️ Architecture Diagram
```text
Repository Code
      ↓
Code Ingestion
      ↓
Chunking + Embeddings
      ↓
Chroma Vector Database
      ↓
Planner Agent
     /      \
Security Agent   Bug Agent
     \      /
   Analysis Tools
(AST, Static Checks, Security Scans)
        ↓
Reflection Agent
        ↓
Fix Agent (Patch Suggestions)
        ↓
Final Analysis Report
```
⚙️ Features

🔹 Multi-Agent Architecture

Planner Agent (decision maker)

Security Agent (vulnerability detection)

Bug Agent (logic & syntax issues)

Reflection Agent (validation layer)

Fix Agent (patch suggestions)

🔹 Retrieval-Augmented Generation (RAG)

Semantic code retrieval using embeddings

Efficient analysis of large repositories

Powered by ChromaDB

🔹 AST-Based Code Analysis

Syntax error detection

Function & structure extraction

Static analysis independent of LLM

🔹 Tool-Driven Agents

Agents use deterministic tools:

AST parser (syntax validation)

SQL injection detection

Hardcoded secret detection

Infinite loop detection

🔹 Multi-LLM Routing

Primary: Gemini API

Fallback: Groq (LLaMA models)

Ensures reliability and cost efficiency.

🔹 Reflection Agent

Validates findings

Removes false positives

Reduces hallucinations

🔹 Fix Agent (Patch-Based)

Suggests minimal fixes (not full rewrite)

Provides:

Issue

Fix suggestion

Explanation

🔄 Agent Workflow
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
```text
Language:
Python

AI & LLM:
Gemini API, Groq (LLaMA), Prompt Engineering, RAG

Architecture:
Multi-Agent Systems, Agentic Workflow, Tool-Based Agents

Vector DB:
ChromaDB

Code Analysis:
AST Parsing, Static Analysis
```

▶️ Getting Started
```text
1️⃣ Clone Repository

git clone <https://github.com/anujpundora/repo-intelligence-ai>
cd repo-intelligence-ai

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Setup Environment Variables
Create .env file:

GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

4️⃣ Run the Project
python main.py
📊 Example Output
Security Findings:
No vulnerabilities detected.
```
Bug Findings:
Syntax error in authentication module.

Reflection:
Verified issue → indentation error

Fix Suggestion:
```text
- Fix indentation in login function
- Ensure proper block structure
⚠️ Edge Cases Handled

Empty retrieval results

Infinite agent loops

LLM malformed JSON responses

Token limit issues

False positives (via reflection agent)
```
🚀 Future Improvements

GitHub PR integration

AST-based automatic patching

Web UI dashboard

Multi-language support

CI/CD integration

🎯 Why This Project Stands Out
```text
This system goes beyond basic AI apps by combining:

Multi-agent orchestration

RAG + semantic search

AST-based static analysis

Reflection-based validation

Patch-based fix generation

👉 Making it closer to real-world AI engineering systems
```
📌 One-Line Description

Autonomous multi-agent AI system for repository analysis using RAG, AST parsing, and LLM reasoning to detect and fix code issues.

⭐ If You Like This Project

Give it a ⭐ on GitHub!

🔥 Next Upgrade (Optional)

If you want to make this even more impressive:

Add UI (Streamlit)

Add GitHub integration (auto PR review)

Add CI/CD scanning

