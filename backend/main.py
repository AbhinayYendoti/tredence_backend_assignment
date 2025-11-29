from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import rooms, autocomplete
from websocket_handler import websocket_endpoint

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pair Programming API",
    description="Real-time collaborative coding platform",
    version="1.0.0"
)

# CORS middleware - allow all origins for development
# In production, you'd want to restrict this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rooms.router)
app.include_router(autocomplete.router)

@app.get("/")
def root():
    return {
        "message": "Pair Programming API",
        "version": "1.0.0",
        "endpoints": {
            "rooms": "/rooms",
            "autocomplete": "/autocomplete",
            "websocket": "/ws/{room_id}"
        }
    }

@app.websocket("/ws/{room_id}")
async def websocket_route(websocket: WebSocket, room_id: str):
    await websocket_endpoint(websocket, room_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


