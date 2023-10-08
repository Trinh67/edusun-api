from fastapi import APIRouter

from app.api.v1 import health, config, common, user, job_post

v1_router = APIRouter()

v1_router.include_router(health.router, prefix="/health", tags=['Health Check'])
v1_router.include_router(common.router, prefix="/common", tags=['Common'])
v1_router.include_router(user.router, prefix="/users", tags=['Users'])
v1_router.include_router(config.router, prefix="/configs", tags=['Configs'])
v1_router.include_router(job_post.router, prefix="/job-posts", tags=['Job Posts'])

