# Fundamental
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
from ws import ws

router = APIRouter()


@router.websocket("/ws")
async def ws_handle(websocket: WebSocket):
    try:
        """
        ws连接进来后，等待lcuapi连接，无论成功与否都要返回前端结果
        """
        await websocket.accept()
        ws.connect(ws=websocket)  # 连接前端websocket
        while True:
            msg = await websocket.receive_text()
    except:
        ws.disconnect()
