from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from sources.frontend import renderer

auth_router = APIRouter()


@auth_router.get("/login_page", response_class=HTMLResponse)
async def read_renderer():
    return renderer.render('login.html')
