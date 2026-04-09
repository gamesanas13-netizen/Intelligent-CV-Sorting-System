#!/usr/bin/env python3
"""
Intelligent CV Sorting System - Professional Edition
Simulates enterprise-level CV evaluation systems.
"""

import argparse
import json
import sys
import os
from pathlib import Path
from src.main import CVSorter

def create_sample_job_profile():
    """Create sample job profile for testing"""
    job_profile = {
        "position": "Senior Data Scientist",
        "min_exp": 5,
        "education": "master",
        "skills": ["python", "machine learning", "sql", "aws", "pandas", "scikit-learn"],
        "languages": ["english", "french"],
        "industry": "tech"
    }
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    with open(config_dir / "job_profiles.json", "w") as f:
        json.dump(job_profile, f, indent=2)
    
    print(f" Created sample job profile: {config_dir / 'job_profiles.json'}")

def main():
    parser = argparse.ArgumentParser(description="🏆 AI-Powered CV Sorting System")
    parser.add_argument("cv_folder", help="Folder containing CVs (PDF/DOCX)")
    parser.add_argument("--job-profile", "-j", default="config/job_profiles.json",
                       help="Job profile JSON file")
    parser.add_argument("--create-sample", "-s", action="store_true",
                       help="Create sample job profile")
    
    args = parser.parse_args()
    
    # Create sample profile if requested
    if args.create_sample:
        create_sample_job_profile()
        return
    
    # Validate inputs
    if not os.path.exists(args.cv_folder):
        print(f" CV folder not found: {args.cv_folder}")
        sys.exit(1)
    
    if not os.path.exists(args.job_profile):
        print(f" Job profile not found: {args.job_profile}")
        print("Run with --create-sample to generate one")
        sys.exit(1)
    
    # Run sorting
    print(" Starting Intelligent CV Sorting System...")
    sorter = CVSorter(args.job_profile)
    results = sorter.process_and_rank(args.cv_folder)
    sorter.display_results(results)
    
    print(f"\n Analysis complete! Check 'data/output/' for full reports")

if __name__ == "__main__":
    main()