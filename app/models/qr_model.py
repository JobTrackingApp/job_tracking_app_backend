from pydantic import BaseModel

class QRCodeResponse(BaseModel):
    job_id: str
    qr_token: str