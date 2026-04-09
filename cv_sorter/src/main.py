import json
import pandas as pd
from pathlib import Path
from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns
from src.cv_processor import CVProcessor
from src.feature_extractor import FeatureExtractor
from src.scorer import CVScorer
from src.report_generator import ReportGenerator

class CVSorter:
    def __init__(self, job_profile_path: str):
        self.processor = CVProcessor()
        self.extractor = FeatureExtractor()
        self.scorer = CVScorer()
        self.report_gen = ReportGenerator()
        
        with open(job_profile_path, 'r') as f:
            self.job_profile = json.load(f)
    
    def process_and_rank(self, cv_folder: str) -> List[Dict]:
        """Main processing pipeline"""
        print("🔍 Processing CVs...")
        
        # 1. Extract text from all CVs
        cv_texts = self.processor.process_folder(cv_folder)
        
        # 2. Extract features and score
        results = []
        for filename, data in cv_texts.items():
            print(f"Analyzing {filename}...")
            
            features = self.extractor.extract_features(data['text'])
            scores = self.scorer.score_cv(features, self.job_profile)
            
            results.append({
                **scores,
                'filename': filename,
                'features': features
            })
        
        # 3. Sort by score
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        # 4. Generate reports
        self.report_gen.generate_full_report(results, self.job_profile)
        
        return results
    
    def display_results(self, results: List[Dict]):
        """Display ranked results"""
        print("\n" + "="*80)
        print("🏆 TOP CANDIDATES RANKING")
        print("="*80)
        
        for i, result in enumerate(results[:10], 1):
            print(f"\n#{i} | {result['filename']}")
            print(f"   Score: {result['final_score']}/100")
            print(f"   Experience: {result['features'].years_experience:.1f} years")
            print(f"   Education: {result['features'].education_level}")
            print(f"   Skills: {', '.join(result['features'].technical_skills[:3])}")