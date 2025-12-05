from fastapi import FastAPI
from controller import router as pf_router

app = FastAPI()

# Include your AI router
app.include_router(pf_router)

# Optional root route
@app.get("/")
async def root():
    return {"status": "success", "message": "API is running"}
