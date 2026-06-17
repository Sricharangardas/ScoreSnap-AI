import os
from dotenv import load_dotenv

# Load environment variables on startup
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import engine, Base, SessionLocal
from routes import auth, matches, standings, users, cron
from seed_fixtures import seed_database
from apscheduler.schedulers.background import BackgroundScheduler
from agents.monitor_agent import MonitorAgent

# Create DB tables
Base.metadata.create_all(bind=engine)

# Automatically seed database on startup if empty
db = SessionLocal()
try:
    seed_database()
finally:
    db.close()

app = FastAPI(
    title="ScoreSnap AI Backend",
    description="Agentic AI Football Assistant for FIFA World Cup 2026",
    version="1.0.0"
)

# Enable CORS for React frontend (Vite defaults to port 5173, Vercel for production)
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "https://scoresnap-ai.vercel.app",
    "*" # Fallback for easy API connectivity
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api")
app.include_router(matches.router, prefix="/api")
app.include_router(standings.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(cron.router, prefix="/api")

@app.get("/")
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": os.getenv("TZ", "UTC"),
        "version": "1.0.0",
        "database": "connected"
    }

# Start APScheduler for local background tasks
# It runs when the FastAPI server is running (great for local tests)
scheduler = BackgroundScheduler()

def run_monitor_agent():
    print("[Background Job] Triggering monitor agent...")
    db_session = SessionLocal()
    try:
        MonitorAgent.monitor_matches(db_session)
    except Exception as e:
        print(f"[Background Job Error] Monitor failed: {e}")
    finally:
        db_session.close()

# Run monitoring task every 5 minutes
scheduler.add_job(run_monitor_agent, 'interval', minutes=5)

@app.on_event("startup")
def start_scheduler():
    if os.getenv("RUN_SCHEDULER_IN_APP", "True").lower() == "true":
        print("Starting background scheduler in FastAPI app...")
        scheduler.start()

@app.on_event("shutdown")
def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
