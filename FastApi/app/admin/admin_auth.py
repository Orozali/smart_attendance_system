from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import async_session_maker
from app.models.user import User
from app.core.security import verify_password  # Function to verify passwords

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """Handles user login and session management."""
        form = await request.form()
        username, password = form["username"], form["password"]

        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalar_one_or_none()
            role = user.role
            if not user or not verify_password(password, user.password) or role != "ADMIN":
                return False

            request.session.update({"user_id": user.id, "role": user.role})

        return True

    async def logout(self, request: Request) -> bool:
        """Clears the session on logout."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Checks if a user is authenticated."""
        user_id = request.session.get("user_id")

        if not user_id:
            return False

        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            return user is not None

authentication_backend = AdminAuth(secret_key="your_secret_key")
