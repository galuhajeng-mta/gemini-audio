from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import google.generativeai as genai
import os

# Ambil API key dari environment variable
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

if not GENAI_API_KEY:
    raise ValueError("Environment variable GENAI_API_KEY belum di-set.")

genai.configure(api_key=GENAI_API_KEY)

app = FastAPI(
    title="Gemini Audio API",
    description="API kecil buat transcribe audio pake Gemini",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Gemini audio API is running"}

@app.post("/audio-transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()

        model = genai.GenerativeModel("gemini-2.5-pro")

        response = model.generate_content(
            [
                {
                    "mime_type": file.content_type or "audio/wav",
                    "data": audio_bytes,
                },
            ]
        )

        return {"text": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
