from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import google.generativeai as genai

# GANTI dengan API key kamu
GENAI_API_KEY = "AIzaSyAX1YinRFNMHeE106fkakMwXc0Y3racMHk"

if GENAI_API_KEY == "ISI_API_KEY_KAMU_DI_SINI":
    raise ValueError("Belum isi API key Gemini. Ganti dulu di kode ya.")

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
        # baca bytes audio
        audio_bytes = await file.read()

        # pakai model audio-understanding, sesuaikan dengan model yang kamu pakai di Google AI
        model = genai.GenerativeModel("gemini-2.5-pro")

        response = model.generate_content(
            [
                {
                    "mime_type": file.content_type or "audio/wav",
                    "data": audio_bytes,
                },
                # kamu bisa tambahin prompt text kalau mau:
                # "Tolong transcribe audio ini ke teks bahasa Indonesia yang rapi."
            ]
        )

        return {"text": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
