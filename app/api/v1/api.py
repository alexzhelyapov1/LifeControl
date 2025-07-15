from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, spheres, locations, records, dashboard, admin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(spheres.router, prefix="/spheres", tags=["Spheres"])
api_router.include_router(locations.router, prefix="/locations", tags=["Locations"])
api_router.include_router(records.router, prefix="/records", tags=["Records"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])