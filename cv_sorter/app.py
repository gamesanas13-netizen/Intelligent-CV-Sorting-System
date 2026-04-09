import os
import json
from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
from pathlib import Path
from werkzeug.utils import secure_filename
import pandas as pd  # ← FIXED: Import pandas here
from src.cv_processor import CVProcessor
from src.feature_extractor import FeatureExtractor
from src.scorer import CVScorer
from src.report_generator import ReportGenerator

app = Flask(__name__)
app.secret_key = 'cv-sorter-super-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

# Create directories
for folder in ['uploads', 'static/results', 'templates', 'config']:
    Path(folder).mkdir(exist_ok=True, parents=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        # Get job profile from form
        job_data = {
            'position': request.form.get('job_title', 'Software Developer'),
            'min_exp': int(request.form.get('min_exp', 3)),
            'skills': request.form.get('skills', 'python').split(','),
            'languages': request.form.get('languages', 'english').split(',')
        }
        
        # Save uploaded CVs
        uploaded_files = []
        for file in request.files.getlist('cv_files'):
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_files.append(filename)
        
        if not uploaded_files:
            flash('Please upload at least one CV!', 'error')
            return redirect(url_for('index'))
        
        print(f"📤 Processing {len(uploaded_files)} CVs...")
        
        # Process CVs
        processor = CVProcessor()
        extractor = FeatureExtractor()
        scorer = CVScorer()
        cv_texts = processor.process_folder(app.config['UPLOAD_FOLDER'])
        
        results = []
        for filename, data in cv_texts.items():
            print(f"   Analyzing {filename}...")
            features = extractor.extract_features(data['text'])
            scores = scorer.score_cv(features, job_data)
            results.append({
                **scores,
                'filename': filename,
                'features': features
            })
        
        # Sort results
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        # Save results
        output_dir = Path('static/results')
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        csv_file = output_dir / f"cv_ranking_{timestamp}.csv"
        
        df = pd.DataFrame([{
            'Filename': r['filename'],
            'Score': r['final_score'],
            'Experience (years)': r['features'].years_experience,
            'Education': r['features'].education_level,
            'Skills': ', '.join(r['features'].technical_skills),
            'Languages': ', '.join(r['features'].languages)
        } for r in results])
        
        df.to_csv(csv_file, index=False)
        
        flash(f'✅ Success! Analyzed {len(results)} CVs. Download ready!', 'success')
        return render_template('results.html', results=results[:12], csv_file=str(csv_file))
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    filepath = Path('static/results') / filename
    if filepath.exists():
        return send_file(str(filepath), as_attachment=True)
    return "File not found", 404

@app.route('/create-sample-job')
def create_sample_job():
    sample_job = {
        "position": "Senior Python Developer",
        "min_exp": 5,
        "skills": ["python", "django", "docker", "aws", "sql"],
        "languages": ["english", "french"]
    }
    (Path('config') / 'job_profiles.json').write_text(json.dumps(sample_job, indent=2))
    flash('✅ Sample job profile created!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🚀 Starting CV Sorter Web App...")
    print("🌐 Open: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)