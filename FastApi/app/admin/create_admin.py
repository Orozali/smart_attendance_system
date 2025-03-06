from app.core.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

existing_admin = db.query(User).filter(User.username == "admin").first()
if not existing_admin:
    hashed_password = pwd_context.hash("admin")
    admin_user = User(username="admin", password=hashed_password, role="ADMIN")
    
    db.add(admin_user)
    db.commit()
    print("✅ Admin user created successfully.")
else:
    print("⚠️ Admin user already exists.")

db.close()
