from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from schemas import UserSignUp, UserSignIn, ForgotPassword, ResetPassword, Token, UserResponse, MessageResponse
from auth_utils import (
    authenticate_user, 
    create_user, 
    get_user_by_email, 
    create_access_token, 
    verify_token,
    generate_reset_token,
    store_reset_token,
    verify_reset_token,
    mark_reset_token_used,
    update_user_password,
    send_reset_email,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()
security = HTTPBearer()

@router.post("/signup", response_model=MessageResponse)
async def sign_up(user: UserSignUp):
    """Sign up a new user."""
    # Check if user already exists
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = create_user(user.email, user.password, user.first_name, user.last_name)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    return MessageResponse(
        message="User created successfully. Please sign in.",
        success=True
    )

@router.post("/signin", response_model=Token)
async def sign_in(user: UserSignIn):
    """Sign in a user."""
    authenticated_user = authenticate_user(user.email, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user["email"]}, 
        expires_delta=access_token_expires
    )
    
    # Prepare user response
    user_response = UserResponse(
        id=authenticated_user["id"],
        email=authenticated_user["email"],
        first_name=authenticated_user["first_name"],
        last_name=authenticated_user["last_name"],
        created_at=authenticated_user["created_at"],
        is_verified=authenticated_user["is_verified"]
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(request: ForgotPassword):
    """Request password reset."""
    # Check if user exists
    user = get_user_by_email(request.email)
    if not user:
        # Don't reveal whether email exists or not for security
        return MessageResponse(
            message="If the email exists, a password reset link has been sent.",
            success=True
        )
    
    # Generate reset token
    reset_token = generate_reset_token()
    
    # Store reset token
    if not store_reset_token(request.email, reset_token):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate reset token"
        )
    
    # Send reset email
    if not send_reset_email(request.email, reset_token):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send reset email"
        )
    
    return MessageResponse(
        message="If the email exists, a password reset link has been sent.",
        success=True
    )

@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(request: ResetPassword):
    """Reset password using token."""
    # Verify reset token
    email = verify_reset_token(request.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Update password
    if not update_user_password(email, request.new_password):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update password"
        )
    
    # Mark token as used
    mark_reset_token_used(request.token)
    
    return MessageResponse(
        message="Password updated successfully",
        success=True
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user information."""
    token = credentials.credentials
    email = verify_token(token)
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user["id"],
        email=user["email"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        created_at=user["created_at"],
        is_verified=user["is_verified"]
    )

@router.post("/verify-token", response_model=MessageResponse)
async def verify_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify if the provided token is valid."""
    token = credentials.credentials
    email = verify_token(token)
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return MessageResponse(
        message="Token is valid",
        success=True
    )
