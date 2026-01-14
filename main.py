import load_env

from fastapi import FastAPI
from routers import business, chat, leads, reps, referrals

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running!"}

# Include routers
app.include_router(business.router)
app.include_router(chat.router)
app.include_router(leads.router)
app.include_router(reps.router)
app.include_router(referrals.router)