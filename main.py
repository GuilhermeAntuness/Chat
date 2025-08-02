import uvicorn
from fastapi import FastAPI
from database import engine, Base
from app.routers import chat
from mongodb_database import mongo_client

app = FastAPI()

@app.get("/")
def check_api():
    return {"response": "Api Online!"}

app.include_router(chat.router)

mongo_client.admin.command('ping')

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5002, reload=True)


