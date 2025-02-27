from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Prompt(Base):
    __tablename__ = 'prompts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    introText = Column(String, nullable=False)
    coreResponsibilities = Column(String, nullable=False)
    tone = Column(String, nullable=False)
    requirements = Column(String, nullable=False)
    constraints = Column(String, nullable=False)

    def __init__(self, introText: str, coreResponsibilities: str, tone: str, requirements: str, constraints: str):
        self.introText = introText
        self.coreResponsibilities = coreResponsibilities
        self.tone = tone
        self.requirements = requirements
        self.constraints = constraints

class Database:
    def __init__(self, db_name: str = "sqlite:///prompts.db"):
        self.engine = create_engine(db_name)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def defaultPrompt(self) -> dict:
        return {
            "introText": "You are an expert AI Sales Communication Specialist with the following capabilities and requirements:",
            "coreResponsibilities": """CORE RESPONSIBILITIES:
                    - Provide the finished email, for example dont have '[Your Name]' use 'WhiteHat' instead.
                    - Generate 3 distinct, highly personalized sales emails
                    - Analyze and incorporate provided client data effectively
                    - Create compelling subject lines with high open rates
                    - Write persuasive yet authentic body content""",
            "tone": """TONE:
                    - Friendly""",
            "requirements": """REQUIREMENTS FOR EACH EMAIL:
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
                    </email_1>""",
            "constraints": """CONSTRAINTS:
                    - Each email must be unique in approach
                    - Must include measurable calls-to-action
                    - Avoid generic sales language
                    - Use natural english human language
                    - Dont reply with anything except the formatted data, dont explain anything."""
        }

    def getPrompt(self) -> dict:
        session = self.Session()
        prompt = session.query(Prompt).filter_by(id=1).first()
        if prompt:
            return {
                "introText": prompt.introText,
                "coreResponsibilities": prompt.coreResponsibilities,
                "tone": prompt.tone,
                "requirements": prompt.requirements,
                "constraints": prompt.constraints
            }
        else: 
            newPrompt = Prompt(**self.defaultPrompt())
            session.add(newPrompt)
            session.commit()
            return {
                "introText": newPrompt.introText,
                "coreResponsibilities": newPrompt.coreResponsibilities,
                "tone": newPrompt.tone,
                "requirements": newPrompt.requirements,
                "constraints": newPrompt.constraints
            }

    def updatePrompt(self, newPrompt: dict):
        session = self.Session()
        prompt = session.query(Prompt).filter_by(id=1).first()
        
        if prompt:
            prompt.introText = newPrompt.get("introText", prompt.introText)
            prompt.coreResponsibilities = newPrompt.get("coreResponsibilities", prompt.coreResponsibilities)
            prompt.tone = newPrompt.get("tone", prompt.tone)
            prompt.requirements = newPrompt.get("requirements", prompt.requirements)
            prompt.constraints = newPrompt.get("constraints", prompt.constraints)
            session.commit()
        else:
            newPromptEntry = Prompt(**newPrompt)
            session.add(newPromptEntry)
            session.commit() 