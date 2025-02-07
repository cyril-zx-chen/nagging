import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api import app

# Load environment variables
load_dotenv()

# Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("src/static/index.html")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True  # Enable auto-reload during development
    ) 