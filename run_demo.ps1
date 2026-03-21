Write-Host "=== MDM Vanna AI Demo Startup ===" -ForegroundColor Cyan
Write-Host "Starting Backend API on port 8000..." -ForegroundColor Yellow
Start-Process "powershell" -ArgumentList "-NoExit", "-Command", "cd backend; echo 'Starting FastAPI...'; uvicorn main:app --reload --port 8000"

Write-Host "Starting Frontend GUI..." -ForegroundColor Yellow
Start-Process "powershell" -ArgumentList "-NoExit", "-Command", "cd frontend; echo 'Starting Vite...'; npm run dev"

Write-Host "Servers are spinning up in new windows." -ForegroundColor Green
Write-Host ""
Write-Host "Please open http://localhost:5173 once Vite is ready." -ForegroundColor Cyan
Write-Host "Then follow the instructions in DEMO_VIDEO_GUIDE.md to record the demo."
