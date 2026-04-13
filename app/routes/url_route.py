from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import url
from app.schemas.url import URLCreate
from app.services.url_service import create_short_url
from fastapi.responses import RedirectResponse
from app.core.redis import redis_client
from app.models.model import URL
from datetime import datetime, timezone

router = APIRouter(prefix="/url", tags=["url"])

@router.post("/shorten")
def shorten_url(url: URLCreate, db: Session = Depends(get_db)):
  short_url = create_short_url(db, str(url.original_url))
  return {"short_url": short_url}





@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):

    # 🔹 1. Check Redis first
    cached_url = redis_client.get(short_code)

    if cached_url:
        return RedirectResponse(cached_url)

    # 🔹 2. If not in Redis → check DB
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if url.expires_at and url.expires_at < datetime.now(timezone.utc):
     return {"error": "This link has expired"}

    if not url:
        return {"error": "URL not found"}

    # 🔹 3. Store in Redis for next time
    redis_client.setex(short_code, 3600, url.original_url)  # Expire after 1 hour

    # 🔹 4. Redirect
    print("REDIRECT HIT")
    return RedirectResponse(url.original_url)