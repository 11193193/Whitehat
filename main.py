from azure.ai.inference.models import UserMessage
import requests
from utils.parser import Parser
from utils.AI import ChatClient

url = 'https://uk.linkedin.com/in/joe-gannon'
apikey = 'a078893d0e089678f25e590c2533dbf10cb4817b'
params = {
    'url': url,
    'apikey': apikey,
    'js_render': 'true',
    'premium_proxy': 'true',
}
"""
response = requests.get('https://api.zenrows.com/v1/', params=params)

print(response.text)"""
if __name__ == "__main__":
    parser = Parser("html.html")
    personalData = parser.getData()
    AI = ChatClient()
    aiResponse = AI.getCompletion(userMessage=str(personalData), product="A backup raid system")

    print(aiResponse)
