from faster_whisper import WhisperModel

def get_transcription(file_path: str) -> str:
    model_size = "large-v2"
    model = WhisperModel(
        model_size,
        device="cuda",
        compute_type="float16"
    )

    segments, _ = model.transcribe(file_path, beam_size=5)
    transcription = "".join(segment.text for segment in segments)
    return transcription.strip()
