from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import requests
from datetime import timedelta

from database import get_db
import models
import schema
import security

router = APIRouter()

GOOGLE_TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"

@router.post("/google", response_model=schema.Token)
async def google_auth(request: schema.GoogleAuthRequest, db: Session = Depends(get_db)):
 
    try:
      
        response = requests.get(f"{GOOGLE_TOKEN_INFO_URL}?id_token={request.token}")
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token"
            )
        
        google_info = response.json()
        google_id = google_info.get("sub")
        email = google_info.get("email")
        name = google_info.get("name")
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by Google"
            )
        
       
        user = db.query(models.User).filter(models.User.email == email).first()
        
        if not user:
           
            user = models.User(
                email=email,
                name=name,
                google_id=google_id,
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
          
            if not user.google_id:
                user.google_id = google_id
                db.commit()
        
        
        access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google authentication service unavailable"
        )