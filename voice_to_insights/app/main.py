from fastapi import FastAPI
import nest_asyncio
from app.api.routes import router

nest_asyncio.apply()

app = FastAPI(title="Voice to Insights API")
app.include_router(router)
