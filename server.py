import os
import re
import csv
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Casa Companion - Vision Site")

# ---------------------------------------------------------------------------
# CORS middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Permissions-Policy middleware (microphone + autoplay)
# ---------------------------------------------------------------------------

@app.middleware("http")
async def add_permissions_policy(request: Request, call_next):
    response = await call_next(request)
    response.headers["Permissions-Policy"] = "microphone=(*), autoplay=(*), camera=()"
    return response

# ---------------------------------------------------------------------------
# Static file serving
# ---------------------------------------------------------------------------

# Mount /static for CSS, JS, fonts, etc.
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount /images for image assets (referenced from root index.html)
if os.path.isdir("images"):
    app.mount("/images", StaticFiles(directory="images"), name="images")

# Mount /audio for audio assets
if os.path.isdir("audio"):
    app.mount("/audio", StaticFiles(directory="audio"), name="audio")

# ---------------------------------------------------------------------------
# Root — serve index.html from repo root
# ---------------------------------------------------------------------------

@app.get("/")
async def serve_index():
    # Serve latest version (v5 if exists, otherwise v4/current)
    for candidate in ["index-v5.html", "index.html"]:
        if os.path.exists(candidate):
            return FileResponse(candidate)
    raise HTTPException(status_code=404, detail="index.html not found")

@app.get("/v4")
async def serve_v4():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    raise HTTPException(status_code=404, detail="v4 not found")

@app.get("/v5")
async def serve_v5():
    if os.path.exists("index-v5.html"):
        return FileResponse("index-v5.html")
    raise HTTPException(status_code=404, detail="v5 not found")

# ---------------------------------------------------------------------------
# POST /api/waitlist — email capture
# ---------------------------------------------------------------------------

WAITLIST_FILE = "waitlist.csv"
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class WaitlistRequest(BaseModel):
    email: str
    name: Optional[str] = None


@app.post("/api/waitlist")
async def waitlist(payload: WaitlistRequest):
    email = payload.email.strip().lower()
    name = (payload.name or "").strip()

    if not EMAIL_REGEX.match(email):
        raise HTTPException(status_code=422, detail="Invalid email address.")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    file_exists = os.path.isfile(WAITLIST_FILE)
    with open(WAITLIST_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["email", "name", "timestamp"])
        writer.writerow([email, name, timestamp])

    return JSONResponse({"success": True, "message": "You're on the list!"})

# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}
