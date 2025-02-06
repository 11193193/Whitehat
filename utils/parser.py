from bs4 import BeautifulSoup
from typing import List, Optional, Dict, Any
from config.types import Types as t


class Parser:
    def __init__(self, content: str) -> None:
        self.soup = BeautifulSoup(content, "html.parser")

    def _read(self, tag: Optional[str] = None, class_: Optional[str] = None) -> List:
        if tag is None and class_ is None:
            return []
        try:
            if tag and class_:
                return self.soup.find_all(tag, class_=class_)
            if tag:
                return self.soup.find_all(tag)
            if class_:
                return self.soup.find_all(class_=class_)
        except Exception as exc:
            return []
        return []

    def _returnCompanies(self) -> List[str]:
        companies = self._read(class_=t._type_company())
        return [company.get_text(strip=True) for company in companies]

    def _returnName(self) -> str:
        nameElements = self._read("h1", class_=t._type_name())
        return nameElements[0].get_text(strip=True) if nameElements else ""

    def _returnBio(self) -> str:
        bioElements = self._read("h2", class_=t._type_bio())
        return bioElements[0].get_text(strip=True) if bioElements else ""

    def _returnAbout(self) -> str:
        aboutElements = self._read("div", class_=t._type_about_container())

        for element in aboutElements:
            if element.find('p'):
                return element.find('p').get_text(strip=True)
        return ""

    def _returnLocation(self) -> str:
        locationElements = self._read("div", class_=t._type_location_container())
        if locationElements:
            span = locationElements[0].find('span')
            return span.get_text(strip=True) if span else ""
        return ""

    def _returnArticles(self) -> List[Dict[str, str]]:
        articles = []
        articleElements = self._read("div", class_=t._type_article_card())
        
        for article in articleElements:
            titleElement = article.find("h3", class_=t._type_article_title())
            descElement = article.find("p", class_=t._type_article_description())
            
            if titleElement and descElement:
                articles.append({
                    "title": titleElement.get_text(strip=True),
                    "description": descElement.get_text(strip=True)
                })
        
        return articles

    def _returnExperience(self) -> List[Dict[str, str]]:
        experiences = []
        experienceItems = self._read("li", class_=t._type_experience_item())
        
        for item in experienceItems:
            title = item.find("span", class_=t._type_experience_title())
            company = item.find("span", class_=t._type_experience_subtitle())
            dateRange = item.find("span", class_=t._type_experience_date())
            description = item.find("div", class_=t._type_experience_text())
            
            if title and company:
                exp = {
                    "title": title.get_text(strip=True),
                    "company": company.get_text(strip=True),
                    "date": dateRange.get_text(strip=True) if dateRange else "",
                    "description": description.get_text(strip=True) if description else ""
                }
                experiences.append(exp)
        
        return experiences

    def _returnSkills(self) -> List[str]:
        skills = []
        skillItems = self._read("li", class_=t._type_skill_item())
        
        for item in skillItems:
            skillLink = item.find('a')
            if skillLink:
                skills.append(skillLink.get_text(strip=True))
        
        return skills
    
    def getData(self) -> Dict[str, Any]:
        try:      
            return {
                "name": self._returnName(),
                "companies": self._returnCompanies(),
                "bio":self._returnBio(),
                "about" : self._returnAbout(),
                "location" : self._returnLocation(),
                "articles" : self._returnArticles(),
                "experience" : self._returnExperience(),
                "skills" : self._returnSkills()
            }
        except Exception as e:
            return []