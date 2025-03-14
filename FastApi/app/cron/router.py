from fastapi import WebSocket, APIRouter, Depends, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
import websockets
import asyncio

from app.cron.insightface import process_frame
from app.core.database import get_db
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ws_router = APIRouter()


@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_bytes()
    
            result = await process_frame(data, db)
            await websocket.send_json(result)
    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        print(f"🚨 WebSocket Error: {e}")
        await websocket.send_json({"error": str(e)})


