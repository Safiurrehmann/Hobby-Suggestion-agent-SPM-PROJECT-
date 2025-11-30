# Hobby Engagement Agent (Unified)

A FastAPI-based natural-language agent that helps users with:
- Hobby suggestions  
- Weekly hobby planning  
- General hobby guidance  

The backend integrates with OpenAI's GPT models and exposes a unified `/agent` endpoint.

---

## Features

- Unified GPT-powered hobby engagement agent  
- JSON-only structured responses  
- Auto intent detection  
- Weekly hobby plan generation  
- Natural-language hobby suggestions  
- FastAPI backend  
- Health-check endpoint  

---

## Requirements

You need the following installed:

- Python 3.9+
- pip
- (Optional) Virtual environment tool
- OpenAI API Key

Install dependencies:

```bash
pip install fastapi uvicorn openai pydantic
```

---

## Environment Setup

Set your OpenAI API key in environment variables.

### Linux / macOS
```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Windows (PowerShell)
```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

---

## Running the Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

If your Python file has a different name, replace `main` accordingly.

Server will be available at:

```
http://127.0.0.1:8000
```

---

## API Endpoints

### 1. POST /agent

Unified endpoint for all hobby tasks.

**Sample Request:**

```json
{
  "messages": [
    { "role": "user", "content": "Suggest a hobby for evenings." }
  ]
}
```

**Sample Response:**

```json
{
  "agent_name": "hobby-engagement-agent",
  "status": "success",
  "data": {
    "response": "{ JSON returned by the model }"
  }
}
```

---

### 2. GET /health

Basic health check endpoint.

**Sample Response:**

```json
{
  "agent_name": "hobby-engagement-agent",
  "status": "success",
  "data": { "status": "ok" }
}
```

---

## Testing with Postman or Thunder Client

### POST /agent
- Method: POST  
- URL: `http://127.0.0.1:8000/agent`  
- Body → Raw JSON:

```json
{
  "messages": [
    { "role": "user", "content": "Give me a 7-day plan to learn sketching." }
  ]
}
```

### GET /health
- Method: GET  
- URL: `http://127.0.0.1:8000/health`

---

## Project Structure

```
/project
│── main.py
│── requirements.txt
│── README.md
```

---

## Notes

- The agent always responds in JSON due to the enforced system prompt.
- Do not commit your OpenAI API key.
- Use `--reload` during development for automatic reload.


Project Structure
/project
│── main.py
│── requirements.txt
│── README.md
