"""
Enhanced Resume Analyzer with ATS-style scoring and improved career fit analysis
"""

import re
import json
import pandas as pd
from collections import defaultdict, Counter
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class EnhancedResumeAnalyzer:
    def __init__(self, career_skills_df, career_keywords_df):
        self.career_skills_df = career_skills_df
        self.career_keywords_df = career_keywords_df
        self.stop_words = set(stopwords.words('english'))
        
        # Enhanced skill dictionaries
        self.technical_skills = self._build_technical_skills_dict()
        self.soft_skills = self._build_soft_skills_dict()
        self.certifications = self._build_certifications_dict()
        
        # ATS keywords and patterns
        self.action_verbs = self._build_action_verbs_list()
        self.quantification_patterns = self._build_quantification_patterns()
    
    def _build_technical_skills_dict(self):
        """Build comprehensive technical skills dictionary with categories"""
        return {
            'programming_languages': [
                'Python', 'Java', 'JavaScript', 'C++', 'C#', 'R', 'SQL', 'Scala', 'Go', 'Rust',
                'TypeScript', 'PHP', 'Ruby', 'Swift', 'Kotlin', 'MATLAB', 'SAS', 'VBA'
            ],
            'data_science': [
                'Machine Learning', 'Deep Learning', 'Neural Networks', 'Natural Language Processing',
                'Computer Vision', 'Data Mining', 'Statistical Analysis', 'Predictive Modeling',
                'Time Series Analysis', 'A/B Testing', 'Hypothesis Testing', 'Regression Analysis',
                'Classification', 'Clustering', 'Dimensionality Reduction', 'Feature Engineering'
            ],
            'frameworks_libraries': [
                'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn',
                'Plotly', 'Keras', 'OpenCV', 'NLTK', 'SpaCy', 'React', 'Angular', 'Vue.js',
                'Django', 'Flask', 'Spring', 'Express.js', 'Bootstrap', 'jQuery'
            ],
            'databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Oracle', 'SQL Server', 'Redis',
                'Cassandra', 'DynamoDB', 'Neo4j', 'Elasticsearch', 'InfluxDB'
            ],
            'cloud_platforms': [
                'AWS', 'Azure', 'Google Cloud Platform', 'GCP', 'Docker', 'Kubernetes',
                'Terraform', 'Jenkins', 'GitLab CI/CD', 'GitHub Actions'
            ],
            'tools_software': [
                'Git', 'Jupyter', 'Tableau', 'Power BI', 'Excel', 'SPSS', 'Stata',
                'Apache Spark', 'Hadoop', 'Airflow', 'Linux', 'Unix', 'Windows'
            ]
        }
    
    def _build_soft_skills_dict(self):
        """Build comprehensive soft skills dictionary with importance weights"""
        return {
            'communication': {
                'skills': ['Communication', 'Public Speaking', 'Presentation', 'Writing', 'Documentation'],
                'weight': 0.9
            },
            'leadership': {
                'skills': ['Leadership', 'Team Management', 'Project Management', 'Mentoring', 'Coaching'],
                'weight': 0.8
            },
            'problem_solving': {
                'skills': ['Problem Solving', 'Critical Thinking', 'Analytical Thinking', 'Troubleshooting'],
                'weight': 0.9
            },
            'collaboration': {
                'skills': ['Teamwork', 'Collaboration', 'Cross-functional', 'Stakeholder Management'],
                'weight': 0.8
            },
            'adaptability': {
                'skills': ['Adaptability', 'Flexibility', 'Learning Agility', 'Innovation', 'Creativity'],
                'weight': 0.7
            },
            'organization': {
                'skills': ['Organization', 'Time Management', 'Prioritization', 'Attention to Detail'],
                'weight': 0.7
            }
        }
    
    def _build_certifications_dict(self):
        """Build certifications dictionary"""
        return {
            'data_science': [
                'Certified Data Scientist', 'Google Data Analytics', 'IBM Data Science',
                'Microsoft Certified: Azure Data Scientist', 'AWS Certified Machine Learning'
            ],
            'cloud': [
                'AWS Certified Solutions Architect', 'Azure Fundamentals', 'Google Cloud Professional',
                'Kubernetes Certified Administrator', 'Docker Certified Associate'
            ],
            'project_management': [
                'PMP', 'Scrum Master', 'Agile Certified', 'Six Sigma', 'ITIL'
            ]
        }
    
    def _build_action_verbs_list(self):
        """Build list of strong action verbs for ATS scoring"""
        return [
            'achieved', 'analyzed', 'built', 'created', 'designed', 'developed', 'implemented',
            'improved', 'increased', 'led', 'managed', 'optimized', 'reduced', 'solved',
            'streamlined', 'transformed', 'automated', 'collaborated', 'delivered', 'executed'
        ]
    
    def _build_quantification_patterns(self):
        """Build regex patterns for quantification detection"""
        return [
            r'\d+%',  # Percentages
            r'\$\d+[KMB]?',  # Dollar amounts
            r'\d+[KMB]?\+?\s*(users|customers|records|projects)',  # Scale indicators
            r'\d+\s*(years?|months?)\s*(of\s*)?(experience|exp)',  # Experience duration
            r'\d+\s*(team|people|members)',  # Team size
            r'\d+x\s*(faster|improvement|increase)'  # Multipliers
        ]
    
    def normalize_text(self, text):
        """Enhanced text normalization"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\-\.\(\)\+\#\%\$]', ' ', text)
        
        # Normalize common variations
        text = re.sub(r'\bML\b', 'Machine Learning', text, flags=re.IGNORECASE)
        text = re.sub(r'\bAI\b', 'Artificial Intelligence', text, flags=re.IGNORECASE)
        text = re.sub(r'\bNLP\b', 'Natural Language Processing', text, flags=re.IGNORECASE)
        text = re.sub(r'\bCV\b', 'Computer Vision', text, flags=re.IGNORECASE)
        
        return text
    
    def extract_skills(self, text):
        """Enhanced skill extraction with categorization"""
        text = self.normalize_text(text)
        text_lower = text.lower()
        
        extracted_skills = {
            'technical': defaultdict(list),
            'soft': [],
            'certifications': []
        }
        
        # Extract technical skills by category
        for category, skills in self.technical_skills.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    extracted_skills['technical'][category].append(skill)
        
        # Extract soft skills
        for category, skill_data in self.soft_skills.items():
            for skill in skill_data['skills']:
                if skill.lower() in text_lower:
                    extracted_skills['soft'].append({
                        'skill': skill,
                        'category': category,
                        'weight': skill_data['weight']
                    })
        
        # Extract certifications
        for category, certs in self.certifications.items():
            for cert in certs:
                if cert.lower() in text_lower:
                    extracted_skills['certifications'].append({
                        'certification': cert,
                        'category': category
                    })
        
        return extracted_skills
    
    def calculate_ats_score(self, text, extracted_skills):
        """Calculate ATS-style resume score"""
        text = self.normalize_text(text)
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        
        # 1. Skills Score (0-100)
        total_technical_skills = sum(len(skills) for skills in extracted_skills['technical'].values())
        soft_skills_count = len(extracted_skills['soft'])
        skills_score = min(100, (total_technical_skills * 3 + soft_skills_count * 2) * 2)
        
        # 2. Keywords Score (0-100)
        action_verb_count = sum(1 for verb in self.action_verbs if verb in words)
        keywords_score = min(100, action_verb_count * 8)
        
        # 3. Formatting Score (0-100)
        # Check for proper structure indicators
        structure_indicators = ['experience', 'education', 'skills', 'projects', 'summary']
        structure_score = sum(10 for indicator in structure_indicators if indicator in text.lower())
        
        # Check for quantification
        quantification_count = 0
        for pattern in self.quantification_patterns:
            quantification_count += len(re.findall(pattern, text, re.IGNORECASE))
        
        formatting_score = min(100, structure_score + quantification_count * 5)
        
        # 4. Clarity Score (0-100)
        avg_sentence_length = sum(len(word_tokenize(sent)) for sent in sentences) / max(len(sentences), 1)
        clarity_penalty = max(0, (avg_sentence_length - 20) * 2)  # Penalize overly long sentences
        clarity_score = max(0, 100 - clarity_penalty)
        
        # Overall score
        overall_score = (skills_score * 0.4 + keywords_score * 0.25 + formatting_score * 0.25 + clarity_score * 0.1)
        
        return {
            'skills_score': round(skills_score),
            'keywords_score': round(keywords_score),
            'formatting_score': round(formatting_score),
            'clarity_score': round(clarity_score),
            'overall_score': round(overall_score),
            'breakdown': {
                'technical_skills_found': total_technical_skills,
                'soft_skills_found': soft_skills_count,
                'action_verbs_found': action_verb_count,
                'quantification_instances': quantification_count,
                'avg_sentence_length': round(avg_sentence_length, 1)
            }
        }
    
    def calculate_career_fit(self, extracted_skills, career):
        """Calculate improved career fit with proper weighting"""
        career_skills = self.career_skills_df[self.career_skills_df['career'] == career]
        
        if career_skills.empty:
            return {'fit_score': 0, 'matched_skills': [], 'missing_skills': {'required': [], 'optional': []}}
        
        # Get all user skills (flatten technical skills)
        user_technical_skills = []
        for category, skills in extracted_skills['technical'].items():
            user_technical_skills.extend(skills)
        
        user_soft_skills = [skill['skill'] for skill in extracted_skills['soft']]
        all_user_skills = set([skill.lower() for skill in user_technical_skills + user_soft_skills])
        
        # Categorize career skills by importance
        required_skills = career_skills[career_skills['importance'] >= 7]
        optional_skills = career_skills[career_skills['importance'] < 7]
        
        # Calculate matches
        matched_required = []
        matched_optional = []
        missing_required = []
        missing_optional = []
        
        # Check required skills
        total_required_weight = 0
        matched_required_weight = 0
        
        for _, skill_row in required_skills.iterrows():
            skill_name = skill_row['skill'].lower()
            weight = skill_row['importance']
            total_required_weight += weight
            
            if skill_name in all_user_skills:
                matched_required.append(skill_row['skill'])
                matched_required_weight += weight
            else:
                missing_required.append({
                    'skill': skill_row['skill'],
                    'importance': weight,
                    'category': skill_row.get('category', 'technical')
                })
        
        # Check optional skills
        total_optional_weight = 0
        matched_optional_weight = 0
        
        for _, skill_row in optional_skills.iterrows():
            skill_name = skill_row['skill'].lower()
            weight = skill_row['importance']
            total_optional_weight += weight
            
            if skill_name in all_user_skills:
                matched_optional.append(skill_row['skill'])
                matched_optional_weight += weight
            else:
                missing_optional.append({
                    'skill': skill_row['skill'],
                    'importance': weight,
                    'category': skill_row.get('category', 'technical')
                })
        
        # Calculate weighted fit score
        required_fit = (matched_required_weight / max(total_required_weight, 1)) * 100
        optional_fit = (matched_optional_weight / max(total_optional_weight, 1)) * 100
        
        # Weighted combination (required skills are 3x more important)
        fit_score = (required_fit * 0.75 + optional_fit * 0.25)
        
        return {
            'fit_score': round(fit_score, 1),
            'required_fit': round(required_fit, 1),
            'optional_fit': round(optional_fit, 1),
            'matched_skills': {
                'required': matched_required,
                'optional': matched_optional
            },
            'missing_skills': {
                'required': sorted(missing_required, key=lambda x: x['importance'], reverse=True),
                'optional': sorted(missing_optional, key=lambda x: x['importance'], reverse=True)
            },
            'skill_counts': {
                'required_matched': len(matched_required),
                'required_total': len(required_skills),
                'optional_matched': len(matched_optional),
                'optional_total': len(optional_skills)
            }
        }
    
    def generate_improvement_suggestions(self, ats_score, career_fits, extracted_skills):
        """Generate targeted improvement suggestions"""
        suggestions = {
            'critical': [],
            'important': [],
            'nice_to_have': []
        }
        
        # ATS Score improvements
        if ats_score['skills_score'] < 70:
            suggestions['critical'].append("Add more technical skills relevant to your target roles")
        
        if ats_score['keywords_score'] < 60:
            suggestions['critical'].append("Include more action verbs (achieved, implemented, optimized)")
        
        if ats_score['formatting_score'] < 70:
            suggestions['important'].append("Add quantifiable achievements with numbers and percentages")
        
        # Career-specific suggestions
        if career_fits:
            top_career = career_fits[0]
            missing_required = top_career['missing_skills']['required'][:3]
            
            if missing_required:
                skills_list = [skill['skill'] for skill in missing_required]
                suggestions['critical'].append(f"Learn these critical skills for {top_career['career']}: {', '.join(skills_list)}")
        
        # Certification suggestions
        if len(extracted_skills['certifications']) == 0:
            suggestions['important'].append("Consider getting relevant certifications to strengthen your profile")
        
        # Soft skills suggestions
        soft_skills_count = len(extracted_skills['soft'])
        if soft_skills_count < 3:
            suggestions['important'].append("Highlight more soft skills like leadership, communication, and problem-solving")
        
        return suggestions
    
    def analyze_resume(self, resume_text):
        """Main analysis function with enhanced scoring"""
        # Extract skills
        extracted_skills = self.extract_skills(resume_text)
        
        # Calculate ATS score
        ats_score = self.calculate_ats_score(resume_text, extracted_skills)
        
        # Get top careers from existing data
        available_careers = self.career_skills_df['career'].unique()[:10]  # Top 10 careers
        
        # Calculate career fits
        career_fits = []
        for career in available_careers:
            fit_analysis = self.calculate_career_fit(extracted_skills, career)
            if fit_analysis['fit_score'] > 0:
                career_fits.append({
                    'career': career,
                    **fit_analysis
                })
        
        # Sort by fit score and get top 5
        career_fits = sorted(career_fits, key=lambda x: x['fit_score'], reverse=True)[:5]
        
        # Generate improvement suggestions
        suggestions = self.generate_improvement_suggestions(ats_score, career_fits, extracted_skills)
        
        # Resume summary
        word_count = len(resume_text.split())
        sentence_count = len(sent_tokenize(resume_text))
        
        return {
            'ats_score': ats_score,
            'extracted_skills': extracted_skills,
            'career_fits': career_fits,
            'improvement_suggestions': suggestions,
            'resume_summary': {
                'word_count': word_count,
                'sentence_count': sentence_count,
                'technical_skills_count': sum(len(skills) for skills in extracted_skills['technical'].values()),
                'soft_skills_count': len(extracted_skills['soft']),
                'certifications_count': len(extracted_skills['certifications']),
                'sentiment': self._analyze_sentiment(resume_text)
            }
        }
    
    def _analyze_sentiment(self, text):
        """Analyze resume sentiment"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'
