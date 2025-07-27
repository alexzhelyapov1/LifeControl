#!/usr/bin/env python3
"""
Script to initialize database and create admin user
"""
import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import async_engine
from app.crud.user import user as user_crud
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# Import all models to ensure they are registered
from app.models.user import User
from app.models.sphere import Sphere
from app.models.location import Location
from app.models.accounting_record import AccountingRecord

async def init_db():
    """Initialize database and create admin user"""
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as db:
        # Check if admin user already exists
        admin_user = await user_crud.get_by_login(db, login="admin")
        
        if not admin_user:
            # Create admin user
            admin_data = UserCreate(
                login="admin",
                password="admin123",
                description="Administrator user"
            )
            
            admin_user = await user_crud.create(db, obj_in=admin_data)
            
            # Set admin privileges
            admin_user.is_admin = True
            await db.commit()
            await db.refresh(admin_user)
            
            print("✅ Admin user created successfully!")
            print(f"   Login: admin")
            print(f"   Password: admin123")
            print(f"   Is Admin: {admin_user.is_admin}")
        else:
            print("ℹ️  Admin user already exists")
            print(f"   Login: {admin_user.login}")
            print(f"   Is Admin: {admin_user.is_admin}")

if __name__ == "__main__":
    print("🚀 Initializing database...")
    asyncio.run(init_db())
    print("✅ Database initialization completed!") 