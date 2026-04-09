from typing import Dict, List
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.feature_extractor import CVFeatures

class CVScorer:
    def __init__(self):
        self.weights = {
            'experience': 0.25,
            'education': 0.20,
            'skills': 0.30,
            'languages': 0.15,
            'companies': 0.05,
            'industry': 0.05
        }
    
    def score_cv(self, features: CVFeatures, job_profile: Dict) -> Dict:
        """Calculate comprehensive job-fit score"""
        scores = {}
        
        # Experience score (normalized 0-10 years optimal)
        exp_score = min(features.years_experience / max(job_profile.get('min_exp', 3), 1), 2.0)
        scores['experience'] = exp_score * self.weights['experience']
        
        # Education score
        edu_mapping = {'phd': 5, 'master': 4, 'bachelor': 3, 'bac': 2}
        candidate_edu = edu_mapping.get(features.education_level, 1)
        required_edu = edu_mapping.get(job_profile.get('education', 'bachelor'), 3)
        scores['education'] = min(candidate_edu / required_edu, 1.0) * self.weights['education']
        
        # Skills match (semantic similarity)
        scores['skills'] = self._calculate_skill_match(
            features.technical_skills, job_profile.get('skills', [])
        ) * self.weights['skills']
        
        # Languages match
        scores['languages'] = self._calculate_language_match(
            features.languages, job_profile.get('languages', [])
        ) * self.weights['languages']
        
        # Stability score (optimal 3-7 companies)
        stability_score = 1.0 - abs(features.companies_count - 5) / 10
        scores['companies'] = max(0, stability_score) * self.weights['companies']
        
        # Industry match
        scores['industry'] = 1.0 if features.industry == job_profile.get('industry') else 0.5
        scores['industry'] *= self.weights['industry']
        
        # Final score
        final_score = sum(scores.values())
        
        return {
            'final_score': round(final_score * 100, 1),
            'breakdown': scores,
            'features': features
        }
    
    def _calculate_skill_match(self, candidate_skills: List[str], required_skills: List[str]) -> float:
        """Calculate skill matching score"""
        if not required_skills:
            return 0.8
        
        matches = len(set(candidate_skills) & set(required_skills))
        return min(matches / len(required_skills), 1.0)
    
    def _calculate_language_match(self, candidate_langs: List[str], required_langs: List[str]) -> float:
        """Calculate language matching score"""
        if not required_langs:
            return 0.8
        
        matches = len(set(candidate_langs) & set(required_langs))
        return min(matches / len(required_langs), 1.0)