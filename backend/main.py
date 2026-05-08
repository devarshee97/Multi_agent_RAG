from fastapi import FastAPI, UploadFile, File, Form, Request
import os
import shutil
import uuid
from fastapi.templating import Jinja2Templates
from RAG.run_pipeline import run_pipeline
from fastapi.responses import HTMLResponse


app = FastAPI()

# Temporary upload folder
TEMP_UPLOAD_DIR = "temp_uploads"

templates = Jinja2Templates(
    directory="templates"
)

os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/query")
def query_documents(
    files: list[UploadFile] = File(...),
    question: str = Form(...)
):

    saved_paths = []

    try:

        # Save uploaded files temporarily
        for file in files:

            unique_filename = (
                f"{uuid.uuid4()}_{file.filename}"
            )

            temp_path = os.path.join(
                TEMP_UPLOAD_DIR,
                unique_filename
            )

            with open(temp_path, "wb") as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer
                )

            saved_paths.append(temp_path)

        # Run your RAG pipeline
        result = run_pipeline(
            file_paths=saved_paths,
            query=question
        )

        return result

    finally:

        # Cleanup temporary files
        for path in saved_paths:

            if os.path.exists(path):

                os.remove(path)