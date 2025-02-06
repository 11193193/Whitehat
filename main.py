import logging
from pydantic import BaseModel
from azure.ai.inference.models import UserMessage
import requests
from utils.parser import Parser
from config.env import Env
from utils.AI import ChatClient
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from colorama import init

init(autoreset=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScanRequest(BaseModel):
    link: str
    product: str

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="styles"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/scan")
async def scan_url(request: ScanRequest):
    logger.info(f"Received scan request for URL: {request.link}")
    apikey = Env.ZENROWS_API_KEY
    params = {
        'url': request.link.strip(" "),
        'apikey': apikey,
        'js_render': 'true',
        'premium_proxy': 'true',
    }
    
    response = requests.get('https://api.zenrows.com/v1/', params=params)

    logger.info(f"ZenRows API response status: {response.status_code}")

    if response.status_code != 200:
        logger.error(f"ZenRows API error: {response.status_code}")
        return {'status': False, 'content': f'zenrows scraper returned {response.status_code}'}

    parser = Parser(response.text)
    personal_data = parser.getData()
    logger.info(f"Parsed data: {personal_data}")
    
    aiClient = ChatClient()
    ai_response = aiClient.getCompletion(
        userMessage=str(personal_data), 
        product=request.product
    )

    logger.info("Successfully generated AI response")

    emails = []
    emailParts = ai_response.split('<email_')
    
    for part in emailParts[1:]:
        emailData = {}
        
        subjectStart = part.find('<subject>') + 9
        subjectEnd = part.find('</subject>')
        emailData['subject'] = part[subjectStart:subjectEnd].strip()
        
        bodyStart = part.find('<body>') + 6
        bodyEnd = part.find('</body>')
        emailData['body'] = part[bodyStart:bodyEnd].strip()
        
        emails.append(emailData)
    
    return {
        "status": True,
        "content": emails
    }

