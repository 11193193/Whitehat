import os
from typing import List, Optional
from config.env import Env
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

class ChatClient:
    def __init__(
        self,
        endpoint: str = "https://models.inference.ai.azure.com",
        model_name: str = "Llama-3.3-70B-Instruct",
        token: Optional[str] = None
    ) -> None:
        self.endpoint = endpoint
        self.model_name = model_name
        self.token = token or Env.GITHUB_TOKEN
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token)
        )
        
    def sysPrompt(self) -> str:
        return f"""You are an expert AI Sales Communication Specialist with the following capabilities and requirements:

                    CORE RESPONSIBILITIES:
                    - Provide the finished email, for example dont have '[Your Name]' use 'WhiteHat' instead.
                    - Generate 3 distinct, highly personalized sales emails
                    - Analyze and incorporate provided client data effectively
                    - Create compelling subject lines with high open rates
                    - Write persuasive yet authentic body content

                    TONE:
                    - Friendly
                    - 


                    REQUIREMENTS FOR EACH EMAIL:
                    1. Personalization:
                    - Use all provided client data points
                    - Adapt tone and style to client context
                    - Reference relevant industry trends

                    2. Structure:
                    - Create attention-grabbing subject lines
                    - Write clear, concise body content
                    - Include specific call-to-action
                    - Maintain professional tone

                    3. Output Format:
                    <email_1>
                    <subject>Your subject line here</subject>
                    <body>
                    Your email body content here
                    
                    Includes:
                    - Personalized greeting
                    - Value proposition
                    - Social proof
                    - Clear CTA
                    </body>
                    </email_1>

                    CONSTRAINTS:
                    - Each email must be unique in approach
                    - Must include measurable calls-to-action
                    - Avoid generic sales language
                    - Use natural english human language
                    - Dont reply with anything except the formatted data, dont explain anything.

                    Please generate three unique email variations following these guidelines, each taking a different approach to connecting with the client while maintaining professionalism and persuasiveness."""

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
            systemMessage = self.sysPrompt()

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
