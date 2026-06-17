from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import User
from routes.auth import get_current_user, UserResponse
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

class UserUpdateInput(BaseModel):
    favorite_team: str | None = None
    notifications_enabled: bool | None = None
    whatsapp_enabled: bool | None = None
    whatsapp_phone: str | None = None
    whatsapp_apikey: str | None = None
    daily_digest_enabled: bool | None = None
    preferred_language: str | None = None

@router.put("/preferences", response_model=UserResponse)
def update_user_preferences(
    update_data: UserUpdateInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Updates the preferences of the logged-in user.
    """
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update_data.favorite_team is not None:
        user.favorite_team = update_data.favorite_team
    
    if update_data.notifications_enabled is not None:
        user.notifications_enabled = update_data.notifications_enabled

    if update_data.whatsapp_enabled is not None:
        user.whatsapp_enabled = update_data.whatsapp_enabled

    if update_data.whatsapp_phone is not None:
        user.whatsapp_phone = update_data.whatsapp_phone

    if update_data.whatsapp_apikey is not None:
        user.whatsapp_apikey = update_data.whatsapp_apikey

    if update_data.daily_digest_enabled is not None:
        user.daily_digest_enabled = update_data.daily_digest_enabled

    if update_data.preferred_language is not None:
        user.preferred_language = update_data.preferred_language

    db.commit()
    db.refresh(user)
    print(f"Preferences updated for user {user.email}.")
    return user
