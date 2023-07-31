# 当前路径加入系统变量 ------------------------------------
import os
import sys

root_path = os.getcwd()
# print(root_path)
sys.path.append(root_path)
# -----------------------------------------------------
# Fundamental
import uvicorn
import fastapi
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from api.api_v1 import api_router
from lcu import lcu

app = fastapi.FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json", debug=False)


@app.on_event("startup")
async def _():
    await lcu.run()


# 配置跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 配置子路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# Start uvicorn server
if __name__ == '__main__':
    uvicorn.run(app='main:app',
                host=settings.HOST,
                port=settings.PORT,
                reload=False,
                server_header=False,
                )
