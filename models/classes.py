from pydantic import BaseModel
from typing import List


class PasswordRequest(BaseModel):
    password:str

class ResponseErrorDetails(BaseModel):
    rule: str
    message: str

class PasswordResponse(BaseModel):
    valid: bool
    notvalid: List[ResponseErrorDetails]