from typing import Optional, Any
from pydantic import BaseModel

class EmbeddingResponse(BaseModel):
    
    vectors: list[list[float]]
    original: Optional[Any] = None
