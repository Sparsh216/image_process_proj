from pydantic import BaseModel

class UploadResponse(BaseModel):
    request_id: str

class StatusResponse(BaseModel):
    request_id: str
    status: str
    output_csv_url: str = None
