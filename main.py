import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markitdown import MarkItDown

app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

@app.post("/upload/", response_class=PlainTextResponse)
async def upload_file(request: Request):
    md = MarkItDown()
    print(request)
    form = await request.form()
    file = form["file"]
    with open(file.filename, "wb") as f:
        f.write(await file.read())
    result = md.convert(file.filename)
    os.remove(file.filename)
    return result.text_content
