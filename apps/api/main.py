from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import webhook, messages

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E3 CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook.router)
app.include_router(messages.router)

@app.get("/")
def root():
    return {"message": "The E3 CRM API! is running."}
