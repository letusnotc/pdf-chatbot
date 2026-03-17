# Run Script for Agentic PDF Chatbot

# Start Backend
Write-Host "Starting Backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd server; .\venv\Scripts\activate; python main.py"

# Start Frontend
Write-Host "Starting Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "Setup initiated. Check the newly opened terminals." -ForegroundColor Yellow
