import os
import secrets
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

from database import supabase

load_dotenv()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verify a JWT token and return the email."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None

def get_user_by_email(email: str):
    """Get user from database by email."""
    try:
        response = supabase.table("users").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def create_user(email: str, password: str, first_name: str, last_name: str):
    """Create a new user in the database."""
    try:
        hashed_password = get_password_hash(password)
        user_data = {
            "email": email,
            "password_hash": hashed_password,
            "first_name": first_name,
            "last_name": last_name,
            "is_verified": False,
            "created_at": datetime.utcnow().isoformat()
        }
        
        response = supabase.table("users").insert(user_data).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def authenticate_user(email: str, password: str):
    """Authenticate a user with email and password."""
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user["password_hash"]):
        return False
    return user

def generate_reset_token() -> str:
    """Generate a secure reset token."""
    return secrets.token_urlsafe(32)

def store_reset_token(email: str, token: str):
    """Store password reset token in database."""
    try:
        expires_at = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
        reset_data = {
            "email": email,
            "token": token,
            "expires_at": expires_at.isoformat(),
            "used": False
        }
        
        # First, delete any existing tokens for this email
        supabase.table("password_resets").delete().eq("email", email).execute()
        
        # Insert new token
        response = supabase.table("password_resets").insert(reset_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error storing reset token: {e}")
        return None

def verify_reset_token(token: str) -> Optional[str]:
    """Verify password reset token and return email if valid."""
    try:
        response = supabase.table("password_resets").select("*").eq("token", token).eq("used", False).execute()
        
        if not response.data:
            return None
            
        reset_record = response.data[0]
        expires_at = datetime.fromisoformat(reset_record["expires_at"].replace('Z', '+00:00'))
        
        if datetime.utcnow().replace(tzinfo=expires_at.tzinfo) > expires_at:
            return None
            
        return reset_record["email"]
    except Exception as e:
        print(f"Error verifying reset token: {e}")
        return None

def mark_reset_token_used(token: str):
    """Mark reset token as used."""
    try:
        supabase.table("password_resets").update({"used": True}).eq("token", token).execute()
    except Exception as e:
        print(f"Error marking token as used: {e}")

def update_user_password(email: str, new_password: str):
    """Update user password."""
    try:
        hashed_password = get_password_hash(new_password)
        response = supabase.table("users").update({"password_hash": hashed_password}).eq("email", email).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error updating password: {e}")
        return None

def send_reset_email(email: str, reset_token: str):
    """Send password reset email."""
    try:
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        
        if not all([smtp_host, smtp_user, smtp_password]):
            print("SMTP configuration not complete")
            return False
        
        # Create reset URL
        reset_url = f"{frontend_url}/reset-password?token={reset_token}"
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = email
        msg['Subject'] = "Password Reset Request"
        
        body = f"""
        Hello,
        
        You have requested to reset your password. Please click the link below to reset your password:
        
        {reset_url}
        
        This link will expire in 1 hour.
        
        If you did not request this password reset, please ignore this email.
        
        Best regards,
        Your App Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
