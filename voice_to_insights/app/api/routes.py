import uuid
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.transcription import get_transcription
from app.services.insights import analyze_text
from app.services.sentiment import sentiment_analysis
from app.store.memory import results_store

router = APIRouter()

@router.post("/process_audio")
async def process_audio():
    session_id = str(uuid.uuid4())

    voice_path = "/kaggle/input/test3-voice/test6.mp3"

    transcript = get_transcription(voice_path)
    insights_json = await analyze_text(transcript)
    sentiment_json = sentiment_analysis(transcript)

    results_store[session_id] = {
        "status": "completed",
        "results": {
            "transcript": transcript,
            "insights": insights_json,
            "sentiment": sentiment_json
        }
    }

    return JSONResponse({
        "session_id": session_id,
        "status": "processing",
        "message": "Audio path received. Processing started."
    })

@router.get("/results/{session_id}")
async def get_results(session_id: str):
    if session_id not in results_store:
        return JSONResponse({"error": "Session not found"}, status_code=404)

    return JSONResponse({
        "session_id": session_id,
        "results": results_store[session_id]["results"],
        "processing_status": results_store[session_id]["status"]
    })
