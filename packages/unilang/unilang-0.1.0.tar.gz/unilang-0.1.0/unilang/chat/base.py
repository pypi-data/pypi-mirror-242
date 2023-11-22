from abc import ABC, abstractmethod
from enum import StrEnum

# Imports from this package
from .response import ChatResponse
from .message import ChatMessage

class ChatModel(ABC):
    
    @property
    @abstractmethod
    def name(self) -> StrEnum:
        """Model name.
        """
        
        pass
    
    @abstractmethod
    def involke(
            self, 
            messages: list[ChatMessage],
            return_original: bool = False
        ) -> ChatResponse:
        """Get a complete response from the chat model.
        If `return_original` is True, the original response will also be returned.

        Parameters
        ----------
        messages : list[ChatMessage]
            The messages to send to the chat model.
        return_original : bool, optional
            Whether to return the original response, by default False.

        Returns
        -------
        ChatResponse
            The response from the chat model.
            The field `original` will be set if `return_original` is True.
        """
        
        pass
    
    @abstractmethod
    async def ainvolke(
            self, 
            messages: list[ChatMessage],
            return_original: bool = False
        ) -> ChatResponse:
        """Get a complete response from the chat model asynchronously.

        Parameters
        ----------
        messages : list[ChatMessage]
            The messages to send to the chat model.
        return_original : bool, optional
            Whether to return the original response, by default False.
            
        Returns
        -------
        ChatResponse
            The response from the chat model.
            The field `original` will be set if `return_original` is True.
        """
        
        pass
    