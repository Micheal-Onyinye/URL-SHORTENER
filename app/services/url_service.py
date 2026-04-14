import random
import string
from sqlalchemy.orm import Session
from app.models.model import URL
from app.core.config import BASE_URL
from datetime import datetime, timedelta, timezone



def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



def create_short_url(db: Session, original_url: str):

    
    short_code = generate_short_code()

    existing = db.query(URL).filter(URL.original_url == original_url).first()

    if existing:
        return {
            "short_code": existing.short_code,
            "original_url": existing.original_url,
            "message": "URL already exists"
        }

    
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    
    expires_in_days = 7

    new_url = URL(
        original_url=original_url,
        short_code=short_code,
        expires_at=datetime.now(timezone.utc) + timedelta(days=expires_in_days)
)
    

    
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    #
    return {
        "short_url": f"{BASE_URL}/{new_url.short_code}",
        "original_url": new_url.original_url
    }