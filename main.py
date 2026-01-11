import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from note_management_agent import run_agent

app = FastAPI()
templates = Jinja2Templates(directory="pages")

# Request model
class AgentRequest(BaseModel):
    """Request model for agent invocation"""
    prompt: str

# Response model

class AgentResponse(BaseModel):
    """Response model for agent invocation"""
    agent_response: str

@app.get("/")
async def home(request: Request):
    """serve the main html interface"""
    return templates.TemplateResponse("index.html", context={"request": request})

@app.post("/agent")
async def invoke_agent(request: AgentRequest):
    """invoke an agent with prompt"""
    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="prompt can not be empty")
        result=run_agent(request.prompt)
        return AgentResponse(agent_response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error invoking agent: {str(e)}")
#uvicorn.run(app, host="0.0.0.0", port=8000)



