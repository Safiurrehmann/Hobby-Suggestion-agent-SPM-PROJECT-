from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import openai

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Hobby Engagement Agent (Unified)",
    description="Natural-language driven agent that performs tasks such as hobby suggestions, weekly plans, etc.",
    version="3.0.0"
)

# ---------------------------------------------------------
# Agent Input Format (similar to OpenAI API)
# ---------------------------------------------------------
class Message(BaseModel):
    role: str
    content: str

class AgentRequest(BaseModel):
    messages: List[Message]

class AgentResponse(BaseModel):
    agent_name: str
    status: str
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


# ---------------------------------------------------------
# Single Agent System Prompt
# ---------------------------------------------------------
SYSTEM_PROMPT = """
You are a unified hobby-engagement agent.

You can perform multiple tasks:
1. Suggest hobbies based on mood, interests, and time availability.
2. Generate detailed 7-day weekly hobby training plans.
3. Provide general hobby guidance or improvements.

You must:
- ALWAYS return structured JSON for the final answer.
- Detect user intent from natural language.

OUTPUT FORMAT (MANDATORY):

{
  "intent": "<detected_intent>",
  "result": <JSON object or array depending on task>
}

Allowed intents:
- "suggest_hobby"
- "weekly_plan"
- "general_advice"

If the user provides insufficient info, ask follow-up questions **inside JSON** like:

{
  "intent": "follow_up",
  "question": "I need to know your mood and time available to suggest hobbies. Please provide these."
}

DO NOT output anything outside JSON.
"""


# ---------------------------------------------------------
# Helper to call OpenAI
# ---------------------------------------------------------
def run_agent(messages: List[Dict[str, str]]) -> str:
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Error: {e}"


# ---------------------------------------------------------
# 🔥 Unified Agent Endpoint
# ---------------------------------------------------------
@app.post("/agent", response_model=AgentResponse)
async def agent(req: AgentRequest):

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend([m.dict() for m in req.messages])

    result = run_agent(messages)

    return AgentResponse(
        agent_name="hobby-engagement-agent",
        status="success",
        data={"response": result}
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
@app.get("/health", response_model=AgentResponse)
async def health_check():
    return AgentResponse(
        agent_name="hobby-engagement-agent",
        status="success",
        data={"status": "ok"}
    )
