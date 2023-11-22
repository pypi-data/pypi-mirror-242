import qianfan

# Imports from this package
from unilang.auth import qianfan_auth
from ..base import EmbeddingModel
from ..response import EmbeddingResponse
from .model_names import QianfanEmbeddingModelName

class QianfanEmbeddingModel(EmbeddingModel):
    
    def __init__(
            self,
            name: QianfanEmbeddingModelName = QianfanEmbeddingModelName.EMBEDDING_V1,
        ):
        
        self._name = name
        self._model = qianfan.Embedding(
            ak=qianfan_auth.access_key,
            sk=qianfan_auth.secret_key,
            model=name
        )
    
    @property
    def name(self) -> QianfanEmbeddingModelName:
        
        return self._name
        
    def embed(
            self, 
            texts: list[str], 
            return_original: bool = False
        ) -> EmbeddingResponse:
        
        # Get the original response
        original_response = self._model.do(texts=texts)
        
        # Extract the embedding vectors
        data = original_response["data"]
        embedding_vectors = list(map(lambda item: item["embedding"], data))
        
        return EmbeddingResponse(
            vectors=embedding_vectors,
            original=original_response if return_original else None
        )
    