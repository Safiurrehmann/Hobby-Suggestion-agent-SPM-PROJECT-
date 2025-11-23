from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import openai

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Hobby Engagement Agent",
    description="Part of Smart Living & Environment Agents System",
    version="2.0.0"
)

# ---------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------
class HobbySuggestRequest(BaseModel):
    interests: str
    mood: Optional[str] = None
    time_available: Optional[int] = None


class WeeklyPlanRequest(BaseModel):
    hobby: str
    hours_per_day: float
    expertise_level: str  # beginner / intermediate / advanced


class AgentResponse(BaseModel):
    agent_name: str
    status: str
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


# ---------------------------------------------------------
# Helper to call OpenAI
# ---------------------------------------------------------
def call_openai(prompt: str) -> str:
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a structured hobby planning assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Error: {e}"


# ---------------------------------------------------------
# 1️⃣ Hobby Suggestion API
# ---------------------------------------------------------
@app.post("/hobby/suggest", response_model=AgentResponse)
async def suggest_hobby(req: HobbySuggestRequest):

    prompt = (
        f"Based on the following info, suggest 3 hobbies in JSON format:\n"
        f"Interests: {req.interests}\n"
        f"Mood: {req.mood}\n"
        f"Time Available: {req.time_available} minutes\n"
        f"Output format:\n"
        f"[\n"
        f"  {{\"title\": \"\", \"description\": \"\", \"time_minutes\": 0}},\n"
        f"  ...\n"
        f"]"
    )


    result = call_openai(prompt)

    return AgentResponse(
        agent_name="hobby-engagement-agent",
        status="success",
        data={"suggestions": result}
    )


# ---------------------------------------------------------
# 2️⃣ Weekly Hobby Plan API (new feature)
# ---------------------------------------------------------
@app.post("/hobby/weekly-plan", response_model=AgentResponse)
async def weekly_hobby_plan(req: WeeklyPlanRequest):

    prompt = f"""
Create a detailed 7-day weekly training and development plan for the hobby: {req.hobby}.

User information:
- Expertise Level: {req.expertise_level}
- Hours available per day: {req.hours_per_day}

Requirements:
- Make the plan progressive.
- Include for each day:
    1. Skill goals
    2. Tasks or exercises
    3. Practice routines
    4. Explanation of why the day's plan helps growth
- Keep it motivating.
- Output strictly in JSON format as an array of objects, like this:

[
  {{
    "day": "Day 1",
    "date": "",
    "skill_goals": "",
    "tasks": ["task1", "task2"],
    "practice_routines": ["routine1", "routine2"],
    "why_it_helps": ""
  }},
  ...
]

Do NOT include any text outside the JSON array.
"""

    result = call_openai(prompt)

    return AgentResponse(
        agent_name="hobby-engagement-agent",
        status="success",
        data={"weekly_plan": result}
    )


# ---------------------------------------------------------
# 3️⃣ Health Check
# ---------------------------------------------------------
@app.get("/health", response_model=AgentResponse)
async def health_check():
    return AgentResponse(
        agent_name="hobby-engagement-agent",
        status="success",
        data={"status": "ok"}
    )
