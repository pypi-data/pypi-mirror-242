import os
from typing import Optional
from pydantic import BaseModel

class QianfanAuth(BaseModel):
    """Qianfan authentication information."""
    
    access_key: Optional[str] 
    secret_key: Optional[str]

qianfan_auth = QianfanAuth(
    access_key=os.getenv("QIANFAN_ACCESS_KEY"),
    secret_key=os.getenv("QIANFAN_SECRET_KEY")
)
