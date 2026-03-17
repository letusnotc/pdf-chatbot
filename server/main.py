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
# We store both the Gemini file name and the local path for image extraction
file_store = {}

class ChatRequest(BaseModel):
    message: str
    file_id: Optional[str] = None

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    file_id: Optional[str]
    response: Optional[str]
    images: Optional[List[str]]

# Define LangGraph flow
def call_gemini_agent(state: AgentState):
    query = state['messages'][-1]
    file_id = state.get('file_id')
    
    if not file_id or file_id not in file_store:
        return {"response": "Please upload a PDF first."}
    
    file_info = file_store[file_id]
    local_path = file_info['local_path']
    
    try:
        file_ref = processor.client.files.get(name=file_id)
        
        prompt = (
            "You are a multimodal agent. Answer based on the provided PDF. "
            "Pay attention to tables, images, and the connections between them. "
            "IMPORTANT: If you discuss a specific table, chart, or image, "
            "ALWAYS mention the page number clearly in the format [PAGE:X]. "
            "This will trigger a visual snippet for the user."
            f"\n\nQuery: {query}"
        )
        
        response = processor.client.models.generate_content(
            model=processor.model_name,
            contents=[file_ref, prompt]
        )
        
        res_text = response.text
        images = []
        
        # Extract page hints and generate base64 snippets
        import re
        page_matches = re.findall(r"\[PAGE:(\d+)\]", res_text)
        if page_matches:
            for page_num in set(page_matches):
                try:
                    img_b64 = processor.extract_page(local_path, int(page_num))
                    if img_b64:
                        images.append(img_b64)
                except Exception as ex:
                    print(f"Failed to extract page {page_num}: {ex}")
        
        return {"response": res_text, "images": images}
    except Exception as e:
        return {"response": f"Error during agent reasoning: {str(e)}", "images": []}

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_gemini_agent)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
agent_app = workflow.compile()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    local_path = os.path.join(upload_dir, file.filename)
    with open(local_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        uploaded_file = await processor.process_pdf(local_path)
        file_store[uploaded_file.name] = {
            "name": uploaded_file.name,
            "local_path": local_path
        }
        return {"file_id": uploaded_file.name, "message": "File processed successfully"}
    except Exception as e:
        if os.path.exists(local_path):
            os.remove(local_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/chat")
async def chat_with_pdf(request: ChatRequest):
    inputs = {
        "messages": [request.message],
        "file_id": request.file_id
    }
    
    try:
        result = agent_app.invoke(inputs)
        return {
            "response": result["response"],
            "images": result.get("images", [])
        }
    except Exception as e:
        return {"response": f"Chat processing error: {str(e)}", "images": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
