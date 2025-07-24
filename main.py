import uvicorn
from fastapi import FastAPI
from database import engine, Base
from app.routers import chat



app = FastAPI()

app.include_router(chat.router)

@app.get("/")
def check_api():
    return {"Response":"Api Online!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)