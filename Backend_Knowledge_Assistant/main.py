# includes database integration also
# includes CORS

import sys
import os

# ALWAYS FIRST: fix Python root path
ROOT_DIR = os.path.abspath("..")
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


from fastapi import FastAPI
from api.routes import router
from db.init_db import init_db   # ✅ add this
from fastapi.middleware.cors import CORSMiddleware   # ✅ ADD THIS

from prometheus_client import generate_latest
from fastapi import Response

# ==========================
# APP INITIALIZATION
# ==========================
app = FastAPI(title="Multi-Agent RAG API")

# ==========================
# ✅ CORS CONFIGURATION
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # React dev server
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# ROUTES
# ==========================
app.include_router(router)

# ✅ runs ONCE when server starts
init_db()

@app.get("/")
def home():
    return {"message": "Knowledge Assistant API is running"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")