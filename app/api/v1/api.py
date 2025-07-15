from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, spheres, locations

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(spheres.router, prefix="/spheres", tags=["Spheres"])
api_router.include_router(locations.router, prefix="/locations", tags=["Locations"])