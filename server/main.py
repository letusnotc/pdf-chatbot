from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from processor import MultimodalPDFProcessor
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

processor = MultimodalPDFProcessor()

# Storage for uploaded file references
# We store the file objects or names from the Gemini File API
file_store = {}

class ChatRequest(BaseModel):
    message: str
    file_id: Optional[str] = None

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    file_name: Optional[str]
    response: Optional[str]

# Define LangGraph flow
def call_gemini_agent(state: AgentState):
    query = state['messages'][-1]
    file_name = state.get('file_name')
    
    if not file_name:
        return {"response": "Please upload a PDF first."}
    
    # In the new SDK, we can pass the file reference
    # We retrieve the file metadata by name if we only have the name
    try:
        # Re-fetching file object from name to be sure it's valid for content generation
        file_ref = processor.client.files.get(name=file_name)
        
        response = processor.client.models.generate_content(
            model=processor.model_name,
            contents=[
                file_ref,
                f"You are a multimodal agent. Answer based on the provided PDF. Pay attention to tables, images, and the connections between them. \n\nQuery: {query}"
            ]
        )
        return {"response": response.text}
    except Exception as e:
        return {"response": f"Error during agent reasoning: {str(e)}"}

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_gemini_agent)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
agent_app = workflow.compile()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        uploaded_file = await processor.process_pdf(temp_path)
        # Store the file name (e.g. 'files/...')
        file_store[uploaded_file.name] = uploaded_file.name
        return {"file_id": uploaded_file.name, "message": "File processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/chat")
async def chat_with_pdf(request: ChatRequest):
    file_name = file_store.get(request.file_id)
    
    inputs = {
        "messages": [request.message],
        "file_name": file_name
    }
    
    try:
        result = agent_app.invoke(inputs)
        return {"response": result["response"]}
    except Exception as e:
        return {"response": f"Chat processing error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
