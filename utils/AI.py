import os
from typing import List, Optional
from config.env import Env
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from utils.database import Database

class ChatClient:
    def __init__(
        self,
        endpoint: str = "https://models.inference.ai.azure.com",
        model_name: str = "Llama-3.3-70B-Instruct",
        token: Optional[str] = None,
        db: Database = None
    ) -> None:
        self.endpoint = endpoint
        self.model_name = model_name
        self.token = token or Env.GITHUB_TOKEN
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token)
        )
        self.db = db
        
    def sysPrompt(self) -> str:
        return self.db.getPrompt()

    def getCompletion(
        self,
        product: Optional[str],
        userMessage: str,
        systemMessage: Optional[str] = None,
        temperature: float = 1.0,
        topP: float = 1.0,
        maxTokens: int = 1000
    ) -> str:
        if systemMessage is None:
            promptSections = self.db.getPrompt()
            systemMessage = f"{promptSections['introText']}\n{promptSections['coreResponsibilities']}\n{promptSections['tone']}\n{promptSections['requirements']}\n{promptSections['constraints']}"

        messages = [
            SystemMessage(content=systemMessage),
            UserMessage(content=f"You are going to attempt to sell the product: {product}, Here is the data of the user: {userMessage}")
        ]
        response = self.client.complete(
            messages=messages,
            temperature=temperature,
            top_p=topP,
            max_tokens=maxTokens,
            model=self.model_name
        )

        return response.choices[0].message.content
