from fastapi import FastAPI, Query, Form, File, UploadFile, Request
from fastapi.responses import JSONResponse, HTMLResponse
from book.models import Book
from book.serializers import get_book_response
import os
from fastapi.templating import Jinja2Templates

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

@app.get("/")
def read_root():
    name = "Paul"
    return {"message": "Hello Mr. {}".format(name)}


@app.get("/test")
def read_test():
    return {"message" : "Test Success !!!"}


# this is PATH PARAMETER

@app.get("/items/{item_id}")
def read_item(item_id : int, q : str = None):
    return {"item_id" : item_id, "q" : q}



# this is QUERY PARAMETER

@app.get("/items")
def read_item(item_id : int = None, q : str = None):
    return {"item_id" : item_id, "q" : q}



# Query Parameter Validation

@app.get("/qpv")
def query_param_valid(q : str = Query(None, min_length = 3, max_length = 5)):
    return { "Res" : q }



# Models

@app.post("/create_item")
def create_new_item(item : Book):
    return {"message" : "Book Created Successfully", "data" : get_book_response(item)}



# Getting Obj or Dict as payload

@app.post("/dict_payload")
def dict_payload_api(item : dict):
    if(str(item['id']) == "0"):
        return { "message" : "Created Successfully", "data" : item }
    else:
        return { "message" : "Updated Successfully", "data" : item }



# submit Form

@app.post("/submit_form")
def submit_form(username : str = Form(...), password : str = Form(...)):
    res = {
        "username" : username,
        "password" : password
    }
    return { "message" : "Form Submitted Successfully", "data" : res }



# Upload File

UPLOAD_FOLDER = "media_uploads"


@app.post("/upload_file/")
async def upload_file_func(file : UploadFile = File(...)):

    os.makedirs(UPLOAD_FOLDER, exist_ok = True)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return JSONResponse(content = { "message" : "File Uploaded Successfully", "filename" : file.filename,"content_type" : file.content_type })




# Jinja 2 Templates

templates = Jinja2Templates(directory="templates")

@app.get("/index", response_class = HTMLResponse)
def html_index(request : Request):
    return templates.TemplateResponse("index.html", {"request" : request, "title" : "Welcome", "message" : "Hello Mr.Paul, I'm Jarvis, Your AI Assistant"} )

