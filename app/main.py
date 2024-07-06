from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
import uuid
import csv
from database import SessionLocal, engine
import models, crud
from schemas import UploadResponse, StatusResponse
from celery_worker import process_images
import config

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/upload", response_model=UploadResponse)
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    request_id = str(uuid.uuid4())
    
    # Create entry in requests table
    db = SessionLocal()
    crud.create_request(db, request_id)
    db.commit()
    
    # Queue image processing task
    background_tasks.add_task(process_images, request_id, file)
    
    return {"request_id": request_id}

@app.get("/status/{request_id}", response_model=StatusResponse)
async def get_status(request_id: str):
    db = SessionLocal()
    request = crud.get_request_by_id(db, request_id=request_id)
    return {"request_id": request.request_id, "status": request.status, "output_csv_url": request.output_csv_url}
