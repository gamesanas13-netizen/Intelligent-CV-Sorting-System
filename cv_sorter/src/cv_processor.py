import os
import pdfplumber
import docx
import re
from typing import Dict, List, Optional
import spacy
from pathlib import Path

class CVProcessor:
    def __init__(self):
        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_fr = spacy.load("fr_core_news_sm")
        
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOCX files"""
        file_path = Path(file_path)
        text = ""
        
        try:
            if file_path.suffix.lower() == '.pdf':
                with pdfplumber.open(file_path) as pdf:
                    text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
            elif file_path.suffix.lower() == '.docx':
                doc = docx.Document(file_path)
                text = '\n'.join(para.text for para in doc.paragraphs)
            
            return self.clean_text(text)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\;\:\-\$\$\$\$\{\}\!\?\€\$\%\&]', '', text)
        return text.strip().lower()
    
    def process_folder(self, folder_path: str) -> Dict[str, Dict]:
        """Process all CVs in a folder"""
        cv_data = {}
        folder = Path(folder_path)
        
        for cv_file in folder.glob("*.*"):
            if cv_file.suffix.lower() in ['.pdf', '.docx']:
                print(f"Processing {cv_file.name}...")
                text = self.extract_text(str(cv_file))
                if text:
                    cv_data[cv_file.name] = {
                        'text': text,
                        'filename': cv_file.name,
                        'path': str(cv_file)
                    }
        
        return cv_data