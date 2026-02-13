from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from config import Base
from routers import auth, google_auth, users


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Authentication API", 
    version="1.0.0",
    description="API with Google OAuth and JWT authentication"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(google_auth.router, prefix="/auth", tags=["Google Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to User Authentication API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
