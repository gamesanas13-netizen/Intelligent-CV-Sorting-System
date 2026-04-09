import re
from typing import List
from dataclasses import dataclass

@dataclass
class CVFeatures:
    years_experience: float = 0.0
    education_level: str = "bac+2"
    technical_skills: List[str] = None
    languages: List[str] = None
    companies_count: int = 0
    industry: str = "general"

class FeatureExtractor:
    def __init__(self):
        self.experience_patterns = [
            r'(\d+)\s*(?:ans?|years?|سنوات?|سنة)',
            r'(\d+)\s*(?:exp|experience|خبرة)'
        ]
        self.skills_keywords = [
            'python', 'java', 'javascript', 'sql', 'aws', 'docker', 'react', 
            'angular', 'node', 'machine learning', 'data science', 'django'
        ]
        self.language_keywords = [
            'english', 'anglais', 'عربي', 'arabic', 'french', 'fran[çc]ais',
            'spanish', 'espagnol', 'german', 'allemand'
        ]
    
    def extract_features(self, text: str, job_description: str = "") -> CVFeatures:
        """Extract features WITHOUT transformers - 100% working"""
        features = CVFeatures()
        features.years_experience = self._extract_experience(text)
        features.education_level = self._extract_education(text)
        features.companies_count = self._extract_companies(text)
        features.languages = self._extract_languages(text)
        features.technical_skills = self._extract_skills(text)
        features.industry = self._extract_industry(text)
        return features
    
    def _extract_experience(self, text: str) -> float:
        total = 0
        for pattern in self.experience_patterns:
            matches = re.findall(pattern, text, re.I)
            total += sum(float(m[0]) for m in matches if m[0].isdigit())
        return min(total, 30)
    
    def _extract_education(self, text: str) -> str:
        edu_keywords = {
            'phd': ['دكتوراه', 'phd', 'doctorat'],
            'master': ['ماجستير', 'master', 'msc', 'maitrise'],
            'bachelor': ['بكالوريوس', 'licence', 'bachelor']
        }
        text_lower = text.lower()
        for level, keywords in edu_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return level
        return "bac+3"
    
    def _extract_companies(self, text: str) -> int:
        # Simple company count from "chez/at/in" patterns
        matches = re.findall(r'(?:chez|عند|في|at|in)[^\.]{1,50}[A-Z]', text, re.I)
        return min(len(matches), 10)
    
    def _extract_languages(self, text: str) -> List[str]:
        text_lower = text.lower()
        found_langs = [lang for lang in self.language_keywords if lang in text_lower]
        return list(set(found_langs))[:3]
    
    def _extract_skills(self, text: str) -> List[str]:
        """SIMPLE keyword matching - NO transformers needed"""
        text_lower = text.lower()
        found_skills = [skill for skill in self.skills_keywords if skill in text_lower]
        return found_skills[:5]
    
    def _extract_industry(self, text: str) -> str:
        text_lower = text.lower()
        if any(word in text_lower for word in ['tech', 'it', 'software', 'تقنية']):
            return 'tech'
        if any(word in text_lower for word in ['finance', 'bank', 'بنك']):
            return 'finance'
        return 'general'