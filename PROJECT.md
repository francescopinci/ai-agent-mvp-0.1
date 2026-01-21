# Project Context for Claude Code

## Overview

Cross-border (Italy ↔ USA) tax optimization assistant MVP. Streamlit chatbot that collects user information through conversation and generates a qualitative tax strategy report.

Stack: Python, Streamlit, OpenAI API, tiktoken.

## Architecture

| File | Responsibility |
|------|----------------|
| `app.py` | Entry point, session state initialization, UI rendering |
| `config.py` | All constants: models, token limits, prompts, welcome message |
| `orchestrator.py` | Main flow control: handles user messages, LLM calls, status management, summarization/finalization triggers |
| `llm.py` | OpenAI API wrapper with retry logic |
| `status_parser.py` | Parses `STATUS: INTAKE/READY` from LLM responses |
| `summarization.py` | Summarization trigger logic and execution |
| `context_builder.py` | Token threshold checks, message trimming |
| `token_counter.py` | Token counting using tiktoken |

## Session State

Stored in `st.session_state`:
- `summary` - accumulated conversation summary (opaque text)
- `recent_messages` - list of `{role, content}` dicts
- `status` - `""`, `"INTAKE"`, or `"READY"`
- `error` - error message to display
- `turns_since_summarization` - counter for summarization trigger
- `final_report` - generated report (when status is READY)

## Data Flow

1. User input via `st.chat_input` in `app.py`
2. `app.py` appends user message to `recent_messages`, calls `orchestrator.handle_user_message()`
3. `orchestrator` formats prompt with summary, calls LLM via `llm.py`
4. `status_parser` extracts status from response
5. `orchestrator` updates state, checks summarization triggers
6. If `STATUS: READY`, runs finalization (final summarization + report generation)

## Boundaries

- **State mutations**: Only `orchestrator.py` mutates session state (besides initialization in `app.py`)
- **Summary handling**: Treat summary as opaque text. No validation, parsing, or interpretation.
- **LLM authority**: The LLM decides lifecycle via status header. Code never overrides semantic decisions.
- **Prompts**: Defined in `config.py`. Prompt content/optimization is out of scope for code changes.

## Task Instructions

When working on this codebase:
1. Only modify files directly related to the assigned task
2. Do not refactor, improve, or "clean up" code outside the task scope
3. Do not add features, abstractions, or error handling beyond what is requested
4. Do not modify prompts unless explicitly asked
5. Preserve existing patterns and code style
