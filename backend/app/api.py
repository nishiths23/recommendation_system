from operator import contains
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.requests import Request
import os
from fastapi.templating import Jinja2Templates

from app.model import router
from app.users import router as user_router

app = FastAPI()

origins = [
            "http://localhost:5000",
            "localhost:5000",
            "0.0.0.0:" + str(os.environ.get('PORT', 5000)),
        ]

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # print(str(request.url.hostname))
    # if 'api' in str(request.url) and (request.url.hostname != 'localhost' and request.url.hostname != '0.0.0.0' and request.url.hostname != 'nishith-rec-sys.herokuapp'):
    #     return JSONResponse(status_code=403, content={
    #         'status': 'unauthorised'
    #     })
    return await call_next(request)


app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

app.include_router(router, prefix='/api')
app.include_router(user_router, prefix='/api')

# With the following code we connect React front with FastAPI backend

templates = Jinja2Templates(directory="../frontend/")

@app.get("/prediction/{full_path:path}")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response('.', scope)
        return response

app.mount('/', SPAStaticFiles(directory='../frontend/', html=True), name='web')


