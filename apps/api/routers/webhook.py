from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
import models
import os
router = APIRouter()
import urllib.request
import json
import asyncio

EVOLUTION_URL = os.getenv("EVOLUTION_URL", "")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")

@router.post("/webhook/{unit_id}")
async def receive_message(unit_id: int, request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    try:
        data = body.get("data", {})
        message_type = body.get("event", "")

        if message_type != "messages.upsert":
            return {"status": "ignored"}

        phone = data.get("key", {}).get("remoteJid", "")
        content = data.get("message", {}).get("conversation", "")

        if not content or not phone:
            return {"status": "ignored"}

        # Persistir mensagem
        msg = models.Message(
            phone=phone,
            content=content,
            unit_id=unit_id
        )
        db.add(msg)
        db.commit()

        # Auto-resposta
        if content.strip().lower() == "oi":
            unit = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
            if unit:
                payload = json.dumps({
                    "number": phone,
                    "text": "Oi! Aqui é o Atendente da E3"
                }).encode("utf-8")
                req = urllib.request.Request(
                    f"{EVOLUTION_URL}/message/sendText/{unit.evolution_instance}",
                    data=payload,
                    headers={
                        "apikey": EVOLUTION_API_KEY,
                        "Content-Type": "application/json"
                    },
                    method="POST"
                )
                await asyncio.to_thread(urllib.request.urlopen, req)

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "detail": str(e)}