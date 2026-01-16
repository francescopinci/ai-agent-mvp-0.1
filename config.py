# Models
MODEL_CONVERSATIONAL = "gpt-4.1-mini"
MODEL_SUMMARIZATION = "gpt-4.1-mini"
MODEL_FINAL_REPORT = "gpt-4.1-mini"

# Token Limits & Thresholds
MAX_CONTEXT_TOKENS = 32000
TOKEN_THRESHOLD_PERCENT = 0.8

# Turn Limits
MAX_TURNS = 8
TURNS_TO_RETAIN_AFTER_SUMMARIZATION = 3

# Prompts
PROMPT_CONVERSATIONAL = "You are a tax assistant.\n\nContext from conversation so far:\n{summary}"
PROMPT_SUMMARIZATION = "Summarize the following.\n\nPrevious summary:\n{summary}\n\nNew messages:\n{messages}"
PROMPT_FINAL_REPORT = "Generate a report based on:\n{summary}"
