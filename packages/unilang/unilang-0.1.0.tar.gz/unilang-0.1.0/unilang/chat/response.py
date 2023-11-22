from typing import Optional, Any
from pydantic import BaseModel

# Imports from this package
from .message import ChatMessage

class ChatResponse(BaseModel):
    
    message: ChatMessage
    original: Optional[Any] = None
