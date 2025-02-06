from azure.ai.inference.models import UserMessage
import requests
from utils.parser import Parser
from utils.AI import ChatClient
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def root(link: str):
    apikey = 'a078893d0e089678f25e590c2533dbf10cb4817b'
    params = {
        'url': link.strip(" "),
        'apikey': apikey,
        'js_render': 'true',
        'premium_proxy': 'true',
    }
    
    response = requests.get('https://api.zenrows.com/v1/', params=params)

    if response.status_code != 200:
        return {'status': False, 'content': f'zenrows scraper returned {response.status_code}'}
        
    return {
        "status":True
        }

"""if __name__ == "__main__":
    parser = Parser("html.html")
    personalData = parser.getData()
    AI = ChatClient()
    aiResponse = AI.getCompletion(userMessage=str(personalData), product="A backup raid system")

    print(aiResponse)"""
