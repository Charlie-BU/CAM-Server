from robyn import Robyn, ALLOW_CORS
from robyn.robyn import Response
from subRouters.v1.user import userRouterV1
from subRouters.v1.service import serviceRouterV1
from subRouters.v1.api import apiRouterV1
from subRouters.v1.ai import aiRouterV1
from database.database import initialize_database
from subRouters.v1.sub_application import subApplicationRouterV1

import json
import os
from dotenv import load_dotenv

load_dotenv()
PORT = int(os.getenv("PORT") or 1024)
CORS_ORIGINS = json.loads(os.getenv("CORS_ORIGINS") or '["http://localhost:9000"]')

app = Robyn(__file__)

app.startup_handler(initialize_database)

app.include_router(userRouterV1)
app.include_router(serviceRouterV1)
app.include_router(apiRouterV1)
app.include_router(aiRouterV1)
app.include_router(subApplicationRouterV1)

# 生产环境需要注释：使用nginx解决跨域问题
ALLOW_CORS(app, origins=CORS_ORIGINS)


@app.exception
def handle_exception(error):
    return Response(status_code=500, headers={}, description=f"error msg: {error}")


@app.get("/")
async def index():
    return "OK"


if __name__ == "__main__":
    app.start(host="0.0.0.0", port=PORT)
