from fastapi import FastAPI
from dotenv import load_dotenv

from app.routes.planner import router as planner_router
from app.routes.stream import router as stream_router

load_dotenv()

app = FastAPI(
    title="Yatra Planner API",
    description="Aggregate travel data from multiple sources to provide single plan with SSE support",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {
        "app": "Yatra Planner API",
        "version": "1.0.0",
        "endpoints": {
            "POST /plan/": "Create an aggregated travel plan",
            "POST /stream/plan": "Stream a travel plan using server-sent events",
        }
    }

app.include_router(planner_router)
app.include_router(stream_router)