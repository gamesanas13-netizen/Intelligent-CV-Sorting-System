# Clone/download all files
mkdir cv_sorter && cd cv_sorter

# Install dependencies
pip install -r requirements.txt

# Download spaCy models
python -m spacy download fr_core_news_sm en_core_web_sm

# Create directories
mkdir -p config data/output src

# Create sample job profile
python run_cv_sorter.py --create-sample
# Put your CVs (PDF/DOCX) in a folder
mkdir test_cvs
# Add your CV files here...

# Run analysis
python run_cv_sorter.py test_cvs/

Processing CVs...
Processing candidate1.pdf...
Processing candidate2.docx...
Analyzing candidate1.pdf...

================================================================================
TOP CANDIDATES RANKING
================================================================================

#1 | john_doe_senior_dev.pdf
   Score: 87.5/100
   Experience: 8.2 years
   Education: master
   Skills: python, django, docker

#2 | marie_dupont_ml.pdf
   Score: 82.3/100
   ...

Reports saved to data/output/
Analysis complete!