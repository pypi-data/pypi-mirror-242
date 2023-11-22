from pydantic import BaseModel

# Imports from this package
from .role import ChatRole

class ChatMessage(BaseModel):
    
    role: ChatRole
    content: str
    
    def to_dict(self) -> dict:
        """Converts the message to a dictionary.
        
        Returns
        -------
        dict
            The message as a dictionary.
        """
        
        return {
            "role": self.role.value,
            "content": self.content
        }

class SystemMessage(ChatMessage):
    
    role: ChatRole = ChatRole.SYSTEM
    
class UserMessage(ChatMessage):
    
    role: ChatRole = ChatRole.USER
    
class AssistantMessage(ChatMessage):
        
    role: ChatRole = ChatRole.ASSISTANT
