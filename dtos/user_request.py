from pydantic import BaseModel
from fastapi import Request


class LogInRequest(BaseModel):
    userId: str
    userPwd: str


class ReqAccessDto:
    accessIP: str
    userAgent: str

    def __init__(self, request: Request):
        self.accessIP = request.client.host
        self.userAgent = request.headers.get("user-agent", "Unknown")
