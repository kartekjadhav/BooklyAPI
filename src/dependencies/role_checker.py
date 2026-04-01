from fastapi import Depends, HTTPException, status
from typing import List
from .get_current_user import get_current_user
from src.models.UserModel import Users

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: Users = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted to perform this action"
        )