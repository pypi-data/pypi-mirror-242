from abc import ABC, abstractmethod

# Imports from this package
from .response import EmbeddingResponse

class EmbeddingModel(ABC):
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Model name.
        """
        
        pass
    
    @abstractmethod
    def embed(
            self, 
            texts: list[str],
            return_original: bool = False
        ) -> EmbeddingResponse:
        """Embeds the given texts.
        
        Parameters
        ----------
        texts : list[str]
            The texts to embed.
        return_original : bool, optional
            Whether to return the original response, by default False.
            
        Returns
        -------
        EmbeddingResponse
            - vectors: The embeddings of the given texts.
            - original: The original response.
        """
        
        pass
