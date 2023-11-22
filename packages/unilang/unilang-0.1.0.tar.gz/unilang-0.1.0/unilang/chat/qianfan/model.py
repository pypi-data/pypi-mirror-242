import qianfan

# Imports from this package
from unilang.auth import qianfan_auth
from ..base import ChatModel
from .model_names import QianfanChatModelName
from ..response import ChatResponse
from ..message import ChatMessage, AssistantMessage

class QianfanChatModel(ChatModel):
    
    def __init__(
            self,
            name: QianfanChatModelName = QianfanChatModelName.ERNIE_BOT_TURBO,
            temperature: float = 0.1,
        ) -> None:
        
        self._name = name
        self._model = qianfan.ChatCompletion(
            ak=qianfan_auth.access_key,
            sk=qianfan_auth.secret_key,
            model=name, 
            temperature=temperature
        )
   
    @property
    def name(self) -> QianfanChatModelName:
        
        return self._name
    
    def involke(
            self, 
            messages: list[ChatMessage],
            return_original: bool = False
        ) -> ChatResponse:
        
        # Get response from Qianfan
        original_response = self._model.do(
            messages=list(map(lambda message: message.to_dict(), messages)),
            stream=False
        )
        
        # Extract the content
        content = original_response["result"]
        
        # Create assistant message
        assistant_message = AssistantMessage(content=content)
        
        # Create chat response
        chat_response = ChatResponse(
            message=assistant_message,
            original=original_response if return_original else None
        )
        
        return chat_response
    
    async def ainvolke(
            self, 
            messages: list[ChatMessage],
            return_original: bool = False
        ) -> ChatResponse:
        
        # Get response from Qianfan
        original_response = await self._model.ado(
            messages=list(map(lambda message: message.to_dict(), messages)),
            stream=False
        )
        
        # Extract the content
        content = original_response["result"]
        
        # Create assistant message
        assistant_message = AssistantMessage(content=content)
        
        # Create chat response
        chat_response = ChatResponse(
            message=assistant_message,
            original=original_response if return_original else None
        )
        
        return chat_response
    