from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import verify_firebase_token

router = APIRouter()

@router.get("/messages")
async def get_messages(
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    user_data = await verify_firebase_token(authorization)
    
    user = db.query(models.User).filter(
        models.User.firebase_uid == user_data["uid"]
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    messages = db.query(models.Message).filter(
        models.Message.unit_id == user.unit_id
    ).order_by(models.Message.received_at.desc()).all()

    return [
        {
            "id": m.id,
            "phone": m.phone,
            "content": m.content,
            "received_at": m.received_at,
            "unit_id": m.unit_id
        }
        for m in messages
    ]