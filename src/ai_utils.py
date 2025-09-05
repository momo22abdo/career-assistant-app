import json
import numpy as np
from sentence_transformers import SentenceTransformer, util
import spacy
import pdfplumber
import os
import requests

# Load models
model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load('en_core_web_sm')

# LinkedIn Jobs API setup (via RapidAPI)
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
if not RAPIDAPI_KEY:
    raise ValueError("Set RAPIDAPI_KEY environment variable")
RAPIDAPI_HOST = "linkedin-public-profiles.p.rapidapi.com"
BASE_URL = "https://linkedin-public-profiles.p.rapidapi.com/v1/linkedin-public-jobs"

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

# In-memory cache
careers = {}
career_embeddings = {}

def fetch_jobs(keyword="software", location="USA", limit=50):
    """Fetch job listings from LinkedIn Jobs API via RapidAPI."""
    jobs = []
    params = {
        "keywords": keyword,
        "location": location,
        "page": 1,
        "limit": 25  # Max per page
    }
    while len(jobs) < limit:
        try:
            response = requests.get(BASE_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            jobs.extend(data.get('jobs', []))
            if not data.get('has_more', False) or len(jobs) >= limit:
                break
            params['page'] += 1
        except requests.RequestException as e:
            print(f"Error fetching jobs: {e}")
            break
    return jobs[:limit]

def extract_career_data(jobs):
    """Extract career data (title, skills, salary, etc.) from job listings."""
    career_data = {}
    for job in jobs:
        title = job.get('job_position', 'Unknown')
        # Parse skills from job description (basic keyword extraction)
        description = job.get('job_description', '')
        doc = nlp(description)
        skills = [ent.text for ent in doc.ents if ent.label_ in ['SKILL', 'ORG', 'PRODUCT']]
        # Deduplicate and filter skills
        skills = list(set(skills) & set(['Python', 'SQL', 'JavaScript', 'Java', 'Machine Learning',
                                        'AWS', 'Docker', 'React', 'Git', 'Agile']))  # Add more as needed
        salary = job.get('salary', '0')  # Parse or estimate if string
        salary = int(salary.replace('$', '').replace(',', '').split('-')[0]) if salary and '$' in salary else 100000
        career_data[title] = {
            'skills': skills,
            'average_salary': salary,
            'demand': 'High' if job.get('applicants', 0) > 50 else 'Medium',  # Example logic
            'top_countries': [job.get('job_location', 'USA')]
        }
    return career_data

# Precompute career data
jobs = fetch_jobs()
careers = extract_career_data(jobs)
for title, data in careers.items():
    skill_str = ' '.join(data['skills'])
    if skill_str:
        career_embeddings[title] = model.encode(skill_str)

# Minimal FAQ for chatbot (MVP; replace with xAI Grok API in Phase 5)
faq = [
    {"question": "Which career suits me if I love AI?", "answer": "AI Engineer or Machine Learning Engineer. Focus on Python, TensorFlow, and neural networks."},
    {"question": "How to become a Software Engineer?", "answer": "Learn Python or Java, data structures, algorithms, and Git. Practice on LeetCode."},
    {"question": "What skills are needed for Data Scientist?", "answer": "Python, SQL, machine learning, statistics, and data visualization (e.g., Tableau)."}
]
faq_embeddings = np.array([model.encode(q['question']) for q in faq])

def match_skills(user_skills):
    """Match user skills to careers using cosine similarity."""
    user_skill_str = ' '.join(user_skills)
    user_emb = model.encode(user_skill_str)
    matches = []
    for career, emb in career_embeddings.items():
        similarity = util.cosine_similarity(user_emb.reshape(1, -1), emb.reshape(1, -1))[0][0]
        matches.append((career, similarity * 100))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:5]

def gap_analysis(user_skills, target_career):
    """Identify missing skills for a target career."""
    if target_career not in careers:
        raise ValueError(f"Career '{target_career}' not found")
    required = set(careers[target_career]['skills'])
    user_set = set(user_skills)
    missing = list(required - user_set)
    return missing

def analyze_resume(pdf_path, target_career):
    """Parse resume PDF and analyze fit for target career."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError("PDF file not found")
    with pdfplumber.open(pdf_path) as pdf:
        text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    doc = nlp(text)
    extracted_skills = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT']]
    match_percent = (len(set(extracted_skills) & set(careers[target_career]['skills'])) /
                    len(careers[target_career]['skills']) * 100 if careers[target_career]['skills'] else 0)
    suggestions = gap_analysis(extracted_skills, target_career)
    return extracted_skills, match_percent, suggestions

def chatbot_query(user_query):
    """Answer career-related questions using FAQ embeddings."""
    query_emb = model.encode(user_query)
    similarities = util.cosine_similarity(query_emb.reshape(1, -1), faq_embeddings)[0]
    best_idx = np.argmax(similarities)
    if similarities[best_idx] > 0.5:
        return faq[best_idx]['answer']
    return "Sorry, I don't have an answer for that. Try rephrasing!"

if __name__ == "__main__":
    # Test skill matching
    user_skills = ["Python", "SQL", "Machine Learning"]
    print("Skill Matches:", match_skills(user_skills))
    # Resume parsing requires a PDF; test manually with temp.pdf