import pandas as pd
import numpy as np
import json
from typing import List, Dict, Tuple, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sentence_transformers import SentenceTransformer
import re
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class CareerRecommendationPipeline:
    def __init__(self, data_path: str = "data/"):
        """Initialize the AI pipeline with data loading and model setup"""
        self.data_path = data_path
        self.career_skills_df = None
        self.salary_demand_df = None
        self.courses_df = None
        self.job_posts_df = None
        self.peer_profiles_df = None
        self.career_keywords_df = None
        self.qa_data = None
        
        # Load all datasets
        self._load_datasets()
        
        # Initialize models
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.scaler = StandardScaler()
        
        # Preprocess data for faster inference
        self._preprocess_data()
    
    def _load_datasets(self):
        """Load all required datasets"""
        try:
            self.career_skills_df = pd.read_csv(f"{self.data_path}career_skills.csv")
            self.salary_demand_df = pd.read_csv(f"{self.data_path}salary_demand.csv")
            self.courses_df = pd.read_csv(f"{self.data_path}courses.csv")
            self.job_posts_df = pd.read_csv(f"{self.data_path}job_posts.csv")
            self.peer_profiles_df = pd.read_csv(f"{self.data_path}peer_profiles.csv")
            self.career_keywords_df = pd.read_csv(f"{self.data_path}career_keywords.csv")
            
            with open(f"{self.data_path}qa_dataset.json", 'r') as f:
                self.qa_data = json.load(f)
                
            print("All datasets loaded successfully!")
        except Exception as e:
            print(f"Error loading datasets: {e}")
            raise
    
    def _preprocess_data(self):
        """Preprocess data for efficient matching"""
        # Create career-skill vectors for similarity matching
        self.career_skill_vectors = {}
        self.skill_embeddings = {}
        
        # Get unique skills and create embeddings
        all_skills = self.career_skills_df['skill'].unique()
        skill_texts = [skill.lower() for skill in all_skills]
        self.skill_embeddings = dict(zip(all_skills, self.sentence_model.encode(skill_texts)))
        
        # Create career profiles
        for career in self.career_skills_df['career'].unique():
            career_skills = self.career_skills_df[
                self.career_skills_df['career'] == career
            ]['skill'].tolist()
            
            # Create career profile text
            career_profile = f"{career} requires skills: {', '.join(career_skills)}"
            self.career_skill_vectors[career] = self.sentence_model.encode(career_profile)
    
    def skill_matching(self, user_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Match user skills to career paths and return match percentages
        
        Args:
            user_skills: List of user's skills
            
        Returns:
            List of career matches with percentages
        """
        if not user_skills:
            return []
        
        # Convert user skills to embeddings
        user_skill_texts = [skill.lower() for skill in user_skills]
        user_embeddings = self.sentence_model.encode(user_skill_texts)
        
        career_matches = []
        
        for career, career_embedding in self.career_skill_vectors.items():
            # Calculate similarity between user skills and career requirements
            similarities = []
            
            # Get required skills for this career
            career_skills = self.career_skills_df[
                self.career_skills_df['career'] == career
            ]
            
            required_skills = career_skills[career_skills['is_required'] == True]['skill'].tolist()
            all_career_skills = career_skills['skill'].tolist()
            
            # Calculate skill overlap
            user_skill_set = set([skill.lower() for skill in user_skills])
            career_skill_set = set([skill.lower() for skill in all_career_skills])
            required_skill_set = set([skill.lower() for skill in required_skills])
            
            # Calculate match percentage
            if career_skill_set:
                skill_overlap = len(user_skill_set.intersection(career_skill_set))
                total_skills = len(career_skill_set)
                skill_match_percentage = (skill_overlap / total_skills) * 100
                
                # Bonus for required skills
                required_overlap = len(user_skill_set.intersection(required_skill_set))
                if required_skills:
                    required_match_percentage = (required_overlap / len(required_skills)) * 100
                    skill_match_percentage = (skill_match_percentage + required_match_percentage) / 2
                
                # Add semantic similarity bonus
                if user_embeddings.size > 0:
                    semantic_similarity = cosine_similarity(
                        user_embeddings.mean(axis=0).reshape(1, -1),
                        career_embedding.reshape(1, -1)
                    )[0][0]
                    semantic_bonus = semantic_similarity * 10  # Scale to percentage
                    skill_match_percentage = min(100, skill_match_percentage + semantic_bonus)
                
                career_matches.append({
                    'career': career,
                    'match_percentage': round(skill_match_percentage, 1),
                    'matched_skills': list(user_skill_set.intersection(career_skill_set)),
                    'missing_skills': list(career_skill_set - user_skill_set),
                    'required_missing': list(required_skill_set - user_skill_set)
                })
        
        # Sort by match percentage
        career_matches.sort(key=lambda x: x['match_percentage'], reverse=True)
        return career_matches[:10]  # Return top 10 matches
    
    def gap_analysis(self, user_skills: List[str], target_career: str) -> Dict[str, Any]:
        """
        Analyze skill gaps for a specific career
        
        Args:
            user_skills: List of user's skills
            target_career: Target career to analyze
            
        Returns:
            Gap analysis results
        """
        if target_career not in self.career_skills_df['career'].values:
            return {"error": "Career not found"}
        
        # Get career requirements
        career_requirements = self.career_skills_df[
            self.career_skills_df['career'] == target_career
        ]
        
        user_skill_set = set([skill.lower() for skill in user_skills])
        
        # Categorize skills
        required_skills = career_requirements[career_requirements['is_required'] == True]
        optional_skills = career_requirements[career_requirements['is_required'] == False]
        
        # Analyze gaps
        required_missing = []
        optional_missing = []
        user_has = []
        
        for _, skill_row in career_requirements.iterrows():
            skill = skill_row['skill']
            if skill.lower() in user_skill_set:
                user_has.append({
                    'skill': skill,
                    'difficulty': skill_row['difficulty'],
                    'importance': skill_row['importance'],
                    'is_required': skill_row['is_required']
                })
            else:
                if skill_row['is_required']:
                    required_missing.append({
                        'skill': skill,
                        'difficulty': skill_row['difficulty'],
                        'importance': skill_row['importance']
                    })
                else:
                    optional_missing.append({
                        'skill': skill,
                        'difficulty': skill_row['difficulty'],
                        'importance': skill_row['importance']
                    })
        
        # Calculate completion percentage
        total_required = len(required_skills)
        required_covered = len([s for s in user_has if s['is_required']])
        completion_percentage = (required_covered / total_required * 100) if total_required > 0 else 0
        
        return {
            'target_career': target_career,
            'completion_percentage': round(completion_percentage, 1),
            'user_has': user_has,
            'required_missing': sorted(required_missing, key=lambda x: x['importance'], reverse=True),
            'optional_missing': sorted(optional_missing, key=lambda x: x['importance'], reverse=True),
            'total_skills_needed': len(career_requirements),
            'skills_covered': len(user_has)
        }
    
    def resume_analysis(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze resume and provide career fit analysis
        
        Args:
            resume_text: Resume text content
            
        Returns:
            Career fit analysis results
        """
        if not resume_text.strip():
            return {"error": "Empty resume text"}
        
        # Clean and preprocess resume text
        cleaned_text = self._clean_text(resume_text)
        
        # Extract skills from resume
        extracted_skills = self._extract_skills_from_text(cleaned_text)
        
        # Get career matches based on extracted skills
        career_matches = self.skill_matching(extracted_skills)
        
        # Analyze keyword frequency for each career
        career_keyword_analysis = {}
        for career in self.career_keywords_df['career'].unique():
            career_keywords = self.career_keywords_df[
                self.career_keywords_df['career'] == career
            ]
            
            keyword_matches = 0
            total_keywords = len(career_keywords)
            matched_keywords = []
            
            for _, keyword_row in career_keywords.iterrows():
                keyword = keyword_row['keyword'].lower()
                if keyword in cleaned_text.lower():
                    keyword_matches += 1
                    matched_keywords.append({
                        'keyword': keyword_row['keyword'],
                        'frequency': keyword_row['frequency_percentage'],
                        'importance': keyword_row['importance_score']
                    })
            
            keyword_fit_percentage = (keyword_matches / total_keywords * 100) if total_keywords > 0 else 0
            
            career_keyword_analysis[career] = {
                'fit_percentage': round(keyword_fit_percentage, 1),
                'matched_keywords': matched_keywords,
                'total_keywords': total_keywords
            }
        
        # Combine skill matching and keyword analysis
        final_analysis = []
        for match in career_matches[:5]:  # Top 5 matches
            career = match['career']
            skill_match = match['match_percentage']
            keyword_analysis = career_keyword_analysis.get(career, {})
            keyword_fit = keyword_analysis.get('fit_percentage', 0)
            
            # Weighted combination (70% skills, 30% keywords)
            combined_fit = (skill_match * 0.7) + (keyword_fit * 0.3)
            
            final_analysis.append({
                'career': career,
                'overall_fit': round(combined_fit, 1),
                'skill_match': skill_match,
                'keyword_fit': keyword_fit,
                'matched_skills': match['matched_skills'],
                'missing_skills': match['missing_skills'][:5],  # Top 5 missing
                'matched_keywords': keyword_analysis.get('matched_keywords', [])[:5]
            })
        
        return {
            'extracted_skills': extracted_skills,
            'career_fits': sorted(final_analysis, key=lambda x: x['overall_fit'], reverse=True),
            'resume_summary': {
                'total_words': len(cleaned_text.split()),
                'skills_found': len(extracted_skills),
                'sentiment': self._analyze_sentiment(cleaned_text)
            }
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove special characters and normalize whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from text using pattern matching and NLP"""
        # Get all available skills
        all_skills = set(self.career_skills_df['skill'].str.lower().tolist())
        
        # Tokenize text
        words = word_tokenize(text)
        
        # Find skill matches
        found_skills = []
        for skill in all_skills:
            if skill in text:
                # Find the original case version
                original_skill = self.career_skills_df[
                    self.career_skills_df['skill'].str.lower() == skill
                ]['skill'].iloc[0]
                found_skills.append(original_skill)
        
        # Remove duplicates and return
        return list(set(found_skills))
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of text"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        else:
            return "Neutral"
    
    def get_learning_path(self, target_career: str, user_skills: List[str]) -> Dict[str, Any]:
        """
        Generate learning path for target career
        
        Args:
            target_career: Target career
            user_skills: Current user skills
            
        Returns:
            Learning path with courses
        """
        gap_analysis = self.gap_analysis(user_skills, target_career)
        
        if "error" in gap_analysis:
            return gap_analysis
        
        # Get missing skills
        missing_skills = gap_analysis['required_missing'] + gap_analysis['optional_missing'][:3]
        
        # Find relevant courses
        learning_path = {
            'target_career': target_career,
            'current_completion': gap_analysis['completion_percentage'],
            'phases': []
        }
        
        # Create learning phases
        phases = [
            {'name': 'Foundation', 'level': 'Beginner', 'skills': []},
            {'name': 'Intermediate', 'level': 'Intermediate', 'skills': []},
            {'name': 'Advanced', 'level': 'Advanced', 'skills': []}
        ]
        
        # Categorize missing skills by difficulty
        for skill_info in missing_skills:
            skill = skill_info['skill']
            difficulty = skill_info['difficulty']
            
            if difficulty == 'Beginner':
                phases[0]['skills'].append(skill_info)
            elif difficulty == 'Intermediate':
                phases[1]['skills'].append(skill_info)
            else:
                phases[2]['skills'].append(skill_info)
        
        # Find courses for each phase
        for phase in phases:
            if phase['skills']:
                phase_skills = [s['skill'] for s in phase['skills']]
                courses = self.courses_df[
                    (self.courses_df['skill'].isin(phase_skills)) & 
                    (self.courses_df['level'] == phase['level'])
                ].head(3)
                
                phase['courses'] = courses.to_dict('records')
                learning_path['phases'].append(phase)
        
        return learning_path
    
    def get_job_market_insights(self, career: str) -> Dict[str, Any]:
        """Get job market insights for a career"""
        if career not in self.salary_demand_df['career'].values:
            return {"error": "Career not found"}
        
        career_data = self.salary_demand_df[
            self.salary_demand_df['career'] == career
        ].iloc[0]
        
        # Get recent job posts
        recent_jobs = self.job_posts_df[
            self.job_posts_df['title'].str.contains(career, case=False, na=False)
        ].head(5)
        
        return {
            'career': career,
            'salary_range': {
                'min': career_data['min_salary'],
                'max': career_data['max_salary'],
                'avg': career_data['avg_salary']
            },
            'demand_index': career_data['demand_index'],
            'growth_rate': career_data['growth_rate'],
            'top_countries': career_data['top_countries'].split(', '),
            'remote_friendly': career_data['remote_friendly'],
            'recent_jobs': recent_jobs.to_dict('records')
        }
    
    def peer_benchmarking(self, user_skills: List[str], target_career: str) -> Dict[str, Any]:
        """Compare user profile with peers in the same career"""
        if target_career not in self.peer_profiles_df['career'].values:
            return {"error": "Career not found"}
        
        # Get peer profiles for the career
        peers = self.peer_profiles_df[
            self.peer_profiles_df['career'] == target_career
        ]
        
        if peers.empty:
            return {"error": "No peer data available"}
        
        user_skill_set = set([skill.lower() for skill in user_skills])
        
        # Analyze peer skills
        peer_skill_analysis = []
        for _, peer in peers.iterrows():
            peer_skills = [s.strip().lower() for s in peer['skills'].split(',')]
            peer_skill_set = set(peer_skills)
            
            skill_overlap = len(user_skill_set.intersection(peer_skill_set))
            total_peer_skills = len(peer_skill_set)
            
            peer_skill_analysis.append({
                'experience_years': peer['experience_years'],
                'education': peer['education'],
                'salary': peer['salary'],
                'skill_count': total_peer_skills,
                'skill_overlap': skill_overlap,
                'skills': peer_skills
            })
        
        # Calculate statistics
        avg_experience = peers['experience_years'].mean()
        avg_salary = peers['salary'].mean()
        avg_skill_count = peers['skills'].apply(lambda x: len(x.split(','))).mean()
        
        # Find most common skills among peers
        all_peer_skills = []
        for _, peer in peers.iterrows():
            all_peer_skills.extend([s.strip().lower() for s in peer['skills'].split(',')])
        
        from collections import Counter
        skill_frequency = Counter(all_peer_skills)
        most_common_skills = skill_frequency.most_common(10)
        
        # Find skills user is missing that peers have
        peer_skill_set = set(all_peer_skills)
        missing_common_skills = list(peer_skill_set - user_skill_set)
        
        return {
            'target_career': target_career,
            'peer_statistics': {
                'avg_experience_years': round(avg_experience, 1),
                'avg_salary': round(avg_salary, 0),
                'avg_skill_count': round(avg_skill_count, 1),
                'total_peers': len(peers)
            },
            'most_common_skills': most_common_skills,
            'missing_common_skills': missing_common_skills[:5],
            'peer_profiles': peer_skill_analysis[:5]  # Top 5 for display
        }
    
    def chatbot_response(self, question: str) -> Dict[str, Any]:
        """Get chatbot response for career-related questions"""
        question_lower = question.lower()
        
        # Simple keyword matching for now
        best_match = None
        best_score = 0
        
        for qa in self.qa_data:
            # Calculate similarity score
            qa_question = qa['question'].lower()
            qa_tags = [tag.lower() for tag in qa['tags']]
            
            # Check for keyword matches
            score = 0
            for word in question_lower.split():
                if word in qa_question:
                    score += 2
                if word in qa_tags:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = qa
        
        if best_match and best_score > 0:
            return {
                'answer': best_match['answer'],
                'category': best_match['category'],
                'confidence': min(100, best_score * 10)
            }
        else:
            return {
                'answer': "I'm sorry, I don't have a specific answer for that question. Could you try rephrasing it or ask about career guidance, skills, learning paths, or job market insights?",
                'category': 'General',
                'confidence': 0
            }

# Example usage and testing
if __name__ == "__main__":
    # Initialize pipeline
    pipeline = CareerRecommendationPipeline()
    
    # Test skill matching
    test_skills = ["Python", "SQL", "Machine Learning", "Statistics"]
    matches = pipeline.skill_matching(test_skills)
    print("Skill Matches:", matches[:3])
    
    # Test gap analysis
    gap = pipeline.gap_analysis(test_skills, "Data Scientist")
    print("Gap Analysis:", gap)
