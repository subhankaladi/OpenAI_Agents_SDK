# from fastapi import FastAPI
# from pydantic import BaseModel
# from agents import Agent, Runner
# from dotenv import load_dotenv
# from dataclasses import dataclass
# from agents import function_tool
# from typing import Optional
# from fastapi.middleware.cors import CORSMiddleware


# load_dotenv()

# app = FastAPI(title="Agent API", description="API for running AI agents")

# class AgentRequest(BaseModel):
#     input_text: str

# class AgentResponse(BaseModel):
#     final_output: str
#     success: bool
#     error: Optional[str] = None

# @dataclass
# class AgentHooks():
#     async def on_start(ctx, agent): 
#         print("Main Agent Start")
    
#     async def on_end(ctx, agent, output):
#         print("Agent end")

#     async def on_handoff(ctx, agent, source):
#         print("handoff ho gya")

#     async def on_tool_start(ctx, agent, tool):
#         print("tool start ho gya")

#     async def on_tool_end(ctx, agent, tool, result):
#         print("bhai jaan tool end ho gya")

# @function_tool
# def weather(city: str):
#     return f"today {city} weather is cloudy with 30C"

# # Initialize the agent once (not on every request)
# agent = Agent(
#     name="Assistant",
#     instructions="You are a helpful assistant",
#     tools=[weather],
#     hooks=AgentHooks,
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Ya specific origins add kar sakte hain
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# async def root():
#     return {"message": "Agent API is running"}

# @app.post("/run-agent", response_model=AgentResponse)
# async def run_agent(request: AgentRequest):
#     try:
#         # Run the agent asynchronously
#         result = await Runner.run(
#             agent,
#             input=request.input_text
#         )
        
#         return AgentResponse(
#             final_output=result.final_output,
#             success=True
#         )
        
#     except Exception as e:
#         return AgentResponse(
#             final_output="",
#             success=False,
#             error=str(e)
#         )

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "agent_loaded": True}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agents import Agent, Runner
from dotenv import load_dotenv
from dataclasses import dataclass
from agents import function_tool
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio

load_dotenv()

app = FastAPI(title="Agent API", description="API for running AI agents with real-time events")

class AgentRequest(BaseModel):
    input_text: str

class AgentResponse(BaseModel):
    final_output: str
    success: bool
    error: Optional[str] = None
    events: Optional[list] = None

@dataclass
class AgentHooks:
    events: list
    
    def __init__(self):
        self.events = []
    
    async def on_start(self, ctx, agent): 
        print("Main Agent Start")
        self.events.append({
            "type": "agent_start",
            "message": "Agent processing started",
            "timestamp": asyncio.get_event_loop().time()
        })
    
    async def on_end(self, ctx, agent, output):
        print("Agent end")
        self.events.append({
            "type": "agent_end", 
            "message": "Agent processing completed",
            "timestamp": asyncio.get_event_loop().time()
        })

    async def on_handoff(self, ctx, agent, source):
        print("handoff ho gya")
        self.events.append({
            "type": "handoff",
            "message": f"Agent handoff from {source}",
            "timestamp": asyncio.get_event_loop().time()
        })

    async def on_tool_start(self, ctx, agent, tool):
        print("tool start ho gya")
        self.events.append({
            "type": "tool_start",
            "message": f"Tool '{tool.name}' execution started", 
            "tool_name": tool.name,
            "timestamp": asyncio.get_event_loop().time()
        })

    async def on_tool_end(self, ctx, agent, tool, result):
        print("bhai jaan tool end ho gya")
        self.events.append({
            "type": "tool_end",
            "message": f"Tool '{tool.name}' execution completed",
            "tool_name": tool.name, 
            "result": str(result)[:100] + "..." if len(str(result)) > 100 else str(result),
            "timestamp": asyncio.get_event_loop().time()
        })

@function_tool
def weather(city: str):
    """Get weather information for a city"""
    return f"Today {city} weather is cloudy with 30°C temperature. Humidity: 65%, Wind: 15 km/h"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Agent API is running with real-time events"}

@app.post("/run-agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    try:
        # Create new hooks instance for this request
        hooks = AgentHooks()
        
        # Initialize the agent with hooks
        agent = Agent(
            name="Assistant",
            instructions="You are a helpful assistant. When users ask about weather, use the weather tool to provide accurate information.",
            tools=[weather],
            hooks=hooks,
        )
        
        print(f"Processing request: {request.input_text}")
        
        # Run the agent asynchronously
        result = await Runner.run(
            agent,
            input=request.input_text
        )
        
        print(f"Agent completed. Events captured: {len(hooks.events)}")
        
        return AgentResponse(
            final_output=result.final_output,
            success=True,
            events=hooks.events
        )
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return AgentResponse(
            final_output="",
            success=False,
            error=str(e)
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "agent_loaded": True,
        "tools_available": ["weather"],
        "events_enabled": True
    }

# Optional: Add a streaming endpoint for real-time events
@app.post("/run-agent-stream")
async def run_agent_stream(request: AgentRequest):
    async def event_generator():
        try:
            hooks = AgentHooks()
            
            agent = Agent(
                name="Assistant",
                instructions="You are a helpful assistant. When users ask about weather, use the weather tool to provide accurate information.",
                tools=[weather],
                hooks=hooks,
            )
            
            # Send initial event
            yield f"data: {json.dumps({'type': 'start', 'message': 'Processing started'})}\n\n"
            
            result = await Runner.run(agent, input=request.input_text)
            
            # Send all events
            for event in hooks.events:
                yield f"data: {json.dumps(event)}\n\n"
            
            # Send final result
            yield f"data: {json.dumps({'type': 'complete', 'final_output': result.final_output})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")