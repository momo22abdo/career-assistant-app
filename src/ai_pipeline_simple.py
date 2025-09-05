import pandas as pd
import numpy as np
import json
from typing import List, Dict, Tuple, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from textblob import TextBlob
import warnings
warnings.filterwarnings('ignore')

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
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
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
        
        # Create career profiles using TF-IDF
        career_profiles = []
        for career in self.career_skills_df['career'].unique():
            career_skills = self.career_skills_df[
                self.career_skills_df['career'] == career
            ]['skill'].tolist()
            
            # Create career profile text
            career_profile = f"{career} requires skills: {', '.join(career_skills)}"
            career_profiles.append(career_profile)
            self.career_skill_vectors[career] = career_profile
        
        # Fit TF-IDF vectorizer
        self.career_tfidf_matrix = self.tfidf_vectorizer.fit_transform(career_profiles)
    
    def skill_matching(self, user_skills: List[str], top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Match user skills to career paths and return match percentages with weighted scoring
        
        Args:
            user_skills: List of user's skills
            top_n: Number of top career matches to return (default: 5)
            
        Returns:
            List of career matches with percentages and explainability
        """
        if not user_skills:
            return []
        
        # Normalize user skills and expand with synonyms
        expanded_user_skills = self._expand_skills_with_synonyms(user_skills)
        user_skill_set = set([skill.lower() for skill in expanded_user_skills])
        
        career_matches = []
        
        for i, (career, career_profile) in enumerate(self.career_skill_vectors.items()):
            # Get career skills with categories and weights
            career_skills = self.career_skills_df[
                self.career_skills_df['career'] == career
            ]
            
            if career_skills.empty:
                continue
                
            required_skills = career_skills[career_skills['is_required'] == True]
            all_career_skills = career_skills
            
            if all_career_skills.empty:
                continue
                
            # Calculate weighted skill matching
            weighted_analysis = self._calculate_weighted_matching(
                user_skill_set, all_career_skills, required_skills
            )
            
            # Calculate semantic similarity using TF-IDF
            user_profile = f"User has skills: {', '.join(user_skills)}"
            user_tfidf = self.tfidf_vectorizer.transform([user_profile])
            career_tfidf = self.career_tfidf_matrix[i:i+1]
            semantic_similarity = cosine_similarity(user_tfidf, career_tfidf)[0][0]
            
            # WEIGHTED SCORING ALGORITHM
            # Base score: 60% weighted skills + 25% required skills + 15% semantic
            base_score = (
                (weighted_analysis['weighted_match_percentage'] * 0.6) +    # 60% weighted skills
                (weighted_analysis['required_match_percentage'] * 0.25) +   # 25% required skills
                (semantic_similarity * 100 * 0.15)                         # 15% semantic similarity
            )
            
            # BONUS SCORING - Reward good skill coverage
            bonus_score = 0
            
            # Bonus for having most required skills
            if weighted_analysis['required_matches']:
                required_coverage = weighted_analysis['required_match_percentage']
                if required_coverage >= 80:
                    bonus_score += 15  # Excellent coverage
                elif required_coverage >= 60:
                    bonus_score += 10  # Good coverage
                elif required_coverage >= 40:
                    bonus_score += 5   # Decent coverage
            
            # Bonus for having complementary skills
            if len(weighted_analysis['exact_matches']) >= len(weighted_analysis['required_matches']) * 0.5:
                bonus_score += 5
            
            # Bonus for high semantic similarity
            if semantic_similarity > 0.3:
                bonus_score += 5
            
            # Calculate final score
            final_score = min(100, base_score + bonus_score)
            
            # SAFETY CHECKS - Prevent unrealistic scores
            if len(all_career_skills) < 8 and final_score > 75:
                final_score = min(75, final_score)
            
            if final_score > 90 and weighted_analysis['required_match_percentage'] < 80:
                final_score = min(85, final_score)
            
            if final_score > 70 and weighted_analysis['required_match_percentage'] < 60:
                final_score = min(65, final_score)
            
            career_matches.append({
                'career': career,
                'match_percentage': round(final_score, 1),
                'base_score': round(base_score, 1),
                'bonus_score': round(bonus_score, 1),
                'semantic_similarity': round(semantic_similarity, 3),
                
                # Weighted Analysis Results
                'weighted_match_percentage': round(weighted_analysis['weighted_match_percentage'], 1),
                'required_match_percentage': round(weighted_analysis['required_match_percentage'], 1),
                'category_scores': weighted_analysis['category_scores'],
                
                # Skills Breakdown
                'matched_skills': weighted_analysis['matched_skills_by_category'],
                'missing_skills': weighted_analysis['missing_skills_by_category'],
                'required_missing': weighted_analysis['required_missing_by_category'],
                
                # Summary Statistics
                'total_career_skills': len(all_career_skills),
                'total_required_skills': len(required_skills),
                'skills_covered': len(weighted_analysis['exact_matches']),
                
                # Explainability
                'score_breakdown': weighted_analysis['score_breakdown']
            })
        
        # Sort by match percentage
        career_matches.sort(key=lambda x: x['match_percentage'], reverse=True)
        return career_matches[:top_n]  # Return top N matches
    
    def _calculate_weighted_matching(self, user_skill_set: set, career_skills_df: pd.DataFrame, 
                                   required_skills_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate weighted skill matching with categories"""
        
        # Initialize category tracking
        categories = ['core', 'intermediate', 'supporting', 'soft']
        category_scores = {cat: 0.0 for cat in categories}
        matched_skills_by_category = {cat: [] for cat in categories}
        missing_skills_by_category = {cat: [] for cat in categories}
        required_missing_by_category = {cat: [] for cat in categories}
        
        # Track exact matches and required skills
        exact_matches = set()
        required_matches = set()
        total_weighted_score = 0
        total_possible_weighted_score = 0
        
        # Process each career skill
        for _, skill_row in career_skills_df.iterrows():
            skill_name = skill_row['skill'].lower()
            skill_category = skill_row.get('category', 'intermediate')
            skill_weight = skill_row.get('weight', 0.7)
            is_required = skill_row.get('is_required', False)
            
            # Calculate weighted score for this skill
            skill_weighted_score = skill_weight * 10  # Scale to 0-10
            
            if skill_name in user_skill_set:
                # Skill matched
                exact_matches.add(skill_name)
                total_weighted_score += skill_weighted_score
                matched_skills_by_category[skill_category].append({
                    'skill': skill_row['skill'],
                    'category': skill_category,
                    'weight': skill_weight,
                    'weighted_score': skill_weighted_score
                })
                
                if is_required:
                    required_matches.add(skill_name)
            else:
                # Skill missing
                missing_skills_by_category[skill_category].append({
                    'skill': skill_row['skill'],
                    'category': skill_category,
                    'weight': skill_weight,
                    'weighted_score': skill_weighted_score
                })
                
                if is_required:
                    required_missing_by_category[skill_category].append({
                        'skill': skill_row['skill'],
                        'category': skill_category,
                        'weight': skill_weight,
                        'weighted_score': skill_weighted_score
                    })
            
            total_possible_weighted_score += skill_weighted_score
        
        # Calculate category scores
        for category in categories:
            matched_in_category = len(matched_skills_by_category[category])
            total_in_category = len([s for _, s in career_skills_df.iterrows() 
                                   if s.get('category', 'intermediate') == category])
            
            if total_in_category > 0:
                category_scores[category] = (matched_in_category / total_in_category) * 100
        
        # Calculate overall percentages
        weighted_match_percentage = (total_weighted_score / total_possible_weighted_score * 100) if total_possible_weighted_score > 0 else 0
        required_match_percentage = (len(required_matches) / len(required_skills_df) * 100) if len(required_skills_df) > 0 else 0
        
        # Create score breakdown for explainability
        score_breakdown = {
            'total_weighted_score': round(total_weighted_score, 1),
            'total_possible_weighted_score': round(total_possible_weighted_score, 1),
            'weighted_percentage': round(weighted_match_percentage, 1),
            'required_matches': len(required_matches),
            'total_required': len(required_skills_df),
            'required_percentage': round(required_match_percentage, 1),
            'category_breakdown': {
                cat: {
                    'matched': len(matched_skills_by_category[cat]),
                    'total': len([s for _, s in career_skills_df.iterrows() 
                                if s.get('category', 'intermediate') == cat]),
                    'score': round(category_scores[cat], 1)
                } for cat in categories
            }
        }
        
        return {
            'exact_matches': exact_matches,
            'required_matches': required_matches,
            'weighted_match_percentage': weighted_match_percentage,
            'required_match_percentage': required_match_percentage,
            'category_scores': category_scores,
            'matched_skills_by_category': matched_skills_by_category,
            'missing_skills_by_category': missing_skills_by_category,
            'required_missing_by_category': required_missing_by_category,
            'score_breakdown': score_breakdown
        }
    
    def _expand_skills_with_synonyms(self, user_skills: List[str]) -> List[str]:
        """Expand user skills with synonyms for better matching"""
        expanded_skills = user_skills.copy()
        
        # ENHANCED SKILL SYNONYMS - More comprehensive mapping
        skill_synonyms = {
            # Programming Languages
            "python": ["python", "py", "python3", "python3.8", "python3.9", "python3.10"],
            "sql": ["sql", "mysql", "postgresql", "sqlite", "tsql", "plsql", "database", "db", "rdbms"],
            "java": ["java", "jdk", "jvm", "spring", "maven", "gradle"],
            "javascript": ["javascript", "js", "ecmascript", "es6", "es2015", "es2017", "es2020"],
            "c++": ["c++", "cpp", "c plus plus", "stl", "boost"],
            "c#": ["c#", "csharp", "dotnet", ".net", "asp.net", "entity framework"],
            
            # Data Science & ML
            "machine learning": ["machine learning", "ml", "ai", "artificial intelligence", "deep learning", "neural networks", "predictive modeling"],
            "deep learning": ["deep learning", "neural networks", "cnn", "rnn", "lstm", "transformer", "bert", "gpt"],
            "data science": ["data science", "data scientist", "analytics", "predictive analytics"],
            "statistics": ["statistics", "stats", "statistical analysis", "hypothesis testing", "regression", "correlation", "anova"],
            
            # Data Visualization & Tools
            "data visualization": ["data visualization", "visualization", "viz", "matplotlib", "seaborn", "plotly", "tableau", "powerbi", "d3.js", "ggplot"],
            "visualization": ["visualization", "data visualization", "viz", "charts", "graphs", "dashboards", "data viz"],
            "pandas": ["pandas", "pd", "dataframe", "data manipulation", "data analysis"],
            "numpy": ["numpy", "np", "numerical computing", "arrays", "matrices"],
            "scikit-learn": ["scikit-learn", "sklearn", "machine learning library", "ml library", "scikit"],
            
            # ML/AI Frameworks
            "tensorflow": ["tensorflow", "tf", "deep learning framework", "neural networks", "keras"],
            "pytorch": ["pytorch", "torch", "deep learning", "ml framework", "neural networks"],
            "keras": ["keras", "deep learning", "neural networks", "tensorflow"],
            
            # Web Development
            "react": ["react", "reactjs", "react.js", "jsx", "hooks", "redux", "context"],
            "angular": ["angular", "angularjs", "ng", "angular 2+", "angular material"],
            "vue.js": ["vue", "vue.js", "vuejs", "vue 3", "composition api"],
            "node.js": ["node.js", "nodejs", "node", "express", "npm", "yarn"],
            "html": ["html", "html5", "markup", "semantic html", "accessibility"],
            "css": ["css", "css3", "styling", "responsive design", "flexbox", "grid", "sass", "less"],
            "typescript": ["typescript", "ts", "typed javascript", "type safety"],
            
            # Python Web Frameworks
            "flask": ["flask", "python web framework", "microframework", "wsgi"],
            "django": ["django", "python web framework", "mvt", "admin panel", "orm"],
            "fastapi": ["fastapi", "python web framework", "async", "api", "pydantic"],
            
            # Java Frameworks
            "spring boot": ["spring boot", "spring", "java framework", "dependency injection", "aop"],
            "spring": ["spring", "spring framework", "spring boot", "java framework"],
            
            # DevOps & Cloud
            "docker": ["docker", "containerization", "containers", "dockerfile", "docker compose"],
            "kubernetes": ["kubernetes", "k8s", "container orchestration", "microservices", "deployment"],
            "aws": ["aws", "amazon web services", "ec2", "s3", "lambda", "rds", "cloudfront", "route53"],
            "azure": ["azure", "microsoft azure", "cloud computing", "vm", "blob storage", "functions"],
            "gcp": ["gcp", "google cloud platform", "google cloud", "compute engine", "cloud storage"],
            
            # Big Data
            "hadoop": ["hadoop", "apache hadoop", "big data", "mapreduce", "hdfs", "yarn"],
            "spark": ["spark", "apache spark", "big data", "distributed computing", "dataframes", "streaming"],
            "kafka": ["kafka", "apache kafka", "streaming", "message queue", "event streaming"],
            
            # Databases
            "mongodb": ["mongodb", "nosql", "document database", "mongo", "aggregation"],
            "postgresql": ["postgresql", "postgres", "relational database", "rdbms", "acid"],
            "mysql": ["mysql", "relational database", "rdbms", "maria db", "innodb"],
            "redis": ["redis", "in-memory database", "cache", "key-value store", "data structures"],
            
            # Infrastructure & Tools
            "terraform": ["terraform", "infrastructure as code", "iac", "hashicorp", "provisioning"],
            "jenkins": ["jenkins", "ci/cd", "continuous integration", "automation", "pipeline"],
            "git": ["git", "github", "gitlab", "version control", "vcs", "source control"],
            "linux": ["linux", "unix", "ubuntu", "centos", "debian", "red hat", "shell"],
            
            # Testing
            "selenium": ["selenium", "web testing", "automated testing", "browser automation", "webdriver"],
            "junit": ["junit", "java testing", "unit testing", "test framework", "tdd"],
            "pytest": ["pytest", "python testing", "unit testing", "test framework", "fixtures"],
            
            # Design & UX
            "figma": ["figma", "ui design", "ux design", "prototyping", "design tools", "collaboration"],
            "adobe xd": ["adobe xd", "ux design", "prototyping", "design tools", "wireframing"],
            "sketch": ["sketch", "ui design", "mac design tool", "prototyping", "design systems"],
            
            # Project Management
            "agile": ["agile", "scrum", "kanban", "project management", "iterative", "adaptive"],
            "scrum": ["scrum", "agile methodology", "sprint planning", "standup", "retrospective"],
            "jira": ["jira", "project management", "issue tracking", "agile tools", "atlassian"],
            
            # Specialized Skills
            "etl": ["etl", "extract transform load", "data pipeline", "data integration", "data processing"],
            "data modeling": ["data modeling", "database design", "schema design", "normalization", "erd"],
            "api": ["api", "rest api", "graphql", "web services", "endpoints", "microservices"],
            "microservices": ["microservices", "microservice architecture", "distributed systems", "service mesh"],
            "ci/cd": ["ci/cd", "continuous integration", "continuous deployment", "devops", "automation"],
            "mlops": ["mlops", "machine learning operations", "model deployment", "model monitoring", "ml infrastructure"]
        }
        
        # Expand skills with synonyms
        for skill in user_skills:
            skill_lower = skill.lower()
            
            # Direct synonym lookup
            if skill_lower in skill_synonyms:
                for synonym in skill_synonyms[skill_lower]:
                    if synonym not in expanded_skills:
                        expanded_skills.append(synonym)
            
            # Fuzzy matching for partial matches
            for canonical_skill, synonyms in skill_synonyms.items():
                # Check if user skill is contained in any canonical skill
                if skill_lower in canonical_skill or canonical_skill in skill_lower:
                    for synonym in synonyms:
                        if synonym not in expanded_skills:
                            expanded_skills.append(synonym)
                
                # Check if user skill matches any synonym
                for synonym in synonyms:
                    if skill_lower in synonym or synonym in skill_lower:
                        for all_synonyms in synonyms:
                            if all_synonyms not in expanded_skills:
                                expanded_skills.append(all_synonyms)
        
        return expanded_skills
    
    def _parse_user_skills(self, user_skills_input: str) -> List[Dict[str, str]]:
        """
        Parse user skills input and extract skill names and levels
        
        Args:
            user_skills_input: Raw user input (can include skill levels)
            
        Returns:
            List of dictionaries with skill name and level
        """
        parsed_skills = []
        
        # Split by newlines or commas
        if "\n" in user_skills_input:
            skills_list = [skill.strip() for skill in user_skills_input.split("\n") if skill.strip()]
        else:
            skills_list = [skill.strip() for skill in user_skills_input.split(",") if skill.strip()]
        
        for skill_input in skills_list:
            skill_input = skill_input.strip()
            if not skill_input:
                continue
            
            # Check if user specified a level (e.g., "Python (Advanced)", "SQL - Intermediate")
            skill_name = skill_input
            skill_level = None
            
            # Pattern 1: "Skill (Level)" - handles parentheses format
            import re
            paren_match = re.match(r'(.+?)\s*\(\s*(Beginner|Intermediate|Advanced)\s*\)', skill_input, re.IGNORECASE)
            if paren_match:
                skill_name = paren_match.group(1).strip()
                skill_level = paren_match.group(2).strip()
            else:
                # Pattern 2: "Skill - Level" or "Skill : Level" - handles dash and colon formats
                dash_match = re.match(r'(.+?)\s*[-:]\s*(Beginner|Intermediate|Advanced)', skill_input, re.IGNORECASE)
                if dash_match:
                    skill_name = dash_match.group(1).strip()
                    skill_level = dash_match.group(2).strip()
            
            # If no level specified, use intelligent default
            if not skill_level:
                skill_level = self._determine_skill_level(skill_name, "")
            
            parsed_skills.append({
                'skill': skill_name,
                'level': skill_level
            })
        
        return parsed_skills
    
    def gap_analysis(self, user_skills: List[str], target_career: str) -> Dict[str, Any]:
        """
        Analyze skill gaps for a specific career with improved logic
        
        Args:
            user_skills: List of user's skills
            target_career: Target career to analyze
            
        Returns:
            Gap analysis results with proper calculations and soft skills
        """
        if target_career not in self.career_skills_df['career'].values:
            return {"error": "Career not found"}
        
        # Get career requirements
        career_requirements = self.career_skills_df[
            self.career_skills_df['career'] == target_career
        ]
        
        # Get soft skills for this career and add them to requirements
        soft_skills = self._get_soft_skills_for_career(target_career)
        career_requirements = pd.concat([career_requirements, soft_skills], ignore_index=True)
        
        # Parse user skills to extract names and levels
        if isinstance(user_skills, str):
            parsed_user_skills = self._parse_user_skills(user_skills)
        else:
            # If it's already a list, convert to the expected format
            parsed_user_skills = [{'skill': skill, 'level': self._determine_skill_level(skill, "")} for skill in user_skills]
        
        # Create a mapping of expanded skill names to original skill info
        skill_mapping = {}
        for skill_info in parsed_user_skills:
            skill_name = skill_info['skill']
            # Get synonyms for this skill
            synonyms = self._get_skill_synonyms(skill_name)
            for synonym in synonyms:
                skill_mapping[synonym.lower()] = skill_info
        
        user_skill_set = set(skill_mapping.keys())
        
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
                # User has this skill - get the skill info from our mapping
                user_skill_info = skill_mapping[skill.lower()]
                
                if user_skill_info and isinstance(user_skill_info, dict):
                    # ALWAYS respect user-provided level
                    skill_level = user_skill_info.get('level', skill_row['difficulty'])
                else:
                    skill_level = self._determine_skill_level(skill, skill_row['difficulty'])
                
                user_has.append({
                    'skill': skill,
                    'difficulty': skill_level,
                    'importance': skill_row['importance'],
                    'is_required': skill_row['is_required'],
                    'category': skill_row.get('category', 'technical')
                })
            else:
                # User missing this skill
                if skill_row['is_required']:
                    required_missing.append({
                        'skill': skill,
                        'difficulty': skill_row['difficulty'],
                        'importance': skill_row['importance'],
                        'category': skill_row.get('category', 'technical')
                    })
                else:
                    optional_missing.append({
                        'skill': skill,
                        'difficulty': skill_row['difficulty'],
                        'importance': skill_row['importance'],
                        'category': skill_row.get('category', 'technical')
                    })
        
        # Calculate completion percentages using importance-weighted formula
        total_required_importance = required_skills['importance'].sum()
        user_required_importance = sum([s['importance'] for s in user_has if s['is_required']])
        
        # Main completion percentage (required skills only)
        completion_percentage = (user_required_importance / total_required_importance * 100) if total_required_importance > 0 else 0
        
        # Separate progress tracking for required vs optional
        total_required = len(required_skills)
        total_optional = len(optional_skills)
        required_covered = len([s for s in user_has if s['is_required']])
        optional_covered = len([s for s in user_has if not s['is_required']])
        
        # Required skills completion percentage
        required_completion = (required_covered / total_required * 100) if total_required > 0 else 0
        
        # Optional skills coverage percentage
        optional_coverage = (optional_covered / total_optional * 100) if total_optional > 0 else 0
        
        # Ensure counters are never negative
        required_missing_count = max(0, total_required - required_covered)
        optional_missing_count = max(0, total_optional - optional_covered)
        
        return {
            'target_career': target_career,
            'completion_percentage': round(completion_percentage, 1),
            'required_completion': round(required_completion, 1),
            'optional_coverage': round(optional_coverage, 1),
            'user_has': user_has,
            'required_missing': sorted(required_missing, key=lambda x: x['importance'], reverse=True),
            'optional_missing': sorted(optional_missing, key=lambda x: x['importance'], reverse=True),
            'total_skills_needed': len(career_requirements),
            'skills_covered': len(user_has),
            'total_required': total_required,
            'total_optional': total_optional,
            'required_covered': required_covered,
            'optional_covered': optional_covered,
            'total_required_importance': total_required_importance,
            'user_required_importance': user_required_importance,
            'required_missing_count': required_missing_count,
            'optional_missing_count': optional_missing_count
        }
    
    def _get_soft_skills_for_career(self, career: str) -> pd.DataFrame:
        """Add soft skills to career requirements"""
        # Define soft skills for each career
        soft_skills_mapping = {
            'Data Scientist': [
                {'skill': 'Communication', 'difficulty': 'Intermediate', 'importance': 8, 'is_required': True, 'category': 'soft', 'weight': 0.8},
                {'skill': 'Problem Solving', 'difficulty': 'Intermediate', 'importance': 9, 'is_required': True, 'category': 'soft', 'weight': 0.9},
                {'skill': 'Critical Thinking', 'difficulty': 'Intermediate', 'importance': 8, 'is_required': True, 'category': 'soft', 'weight': 0.8},
                {'skill': 'Teamwork', 'difficulty': 'Intermediate', 'importance': 7, 'is_required': False, 'category': 'soft', 'weight': 0.7},
                {'skill': 'Leadership', 'difficulty': 'Intermediate', 'importance': 6, 'is_required': False, 'category': 'soft', 'weight': 0.6}
            ],
            'Data Engineer': [
                {'skill': 'Communication', 'difficulty': 'Intermediate', 'importance': 7, 'is_required': True, 'category': 'soft', 'weight': 0.7},
                {'skill': 'Problem Solving', 'difficulty': 'Advanced', 'importance': 8, 'is_required': True, 'category': 'soft', 'weight': 0.8},
                {'skill': 'Attention to Detail', 'difficulty': 'Advanced', 'importance': 9, 'is_required': True, 'category': 'soft', 'weight': 0.9},
                {'skill': 'Teamwork', 'difficulty': 'Intermediate', 'importance': 6, 'is_required': False, 'category': 'soft', 'weight': 0.6}
            ],
            'Machine Learning Engineer': [
                {'skill': 'Communication', 'difficulty': 'Intermediate', 'importance': 7, 'is_required': True, 'category': 'soft', 'weight': 0.7},
                {'skill': 'Problem Solving', 'difficulty': 'Advanced', 'importance': 9, 'is_required': True, 'category': 'soft', 'weight': 0.9},
                {'skill': 'Research Skills', 'difficulty': 'Advanced', 'importance': 8, 'is_required': True, 'category': 'soft', 'weight': 0.8},
                {'skill': 'Creativity', 'difficulty': 'Intermediate', 'importance': 6, 'is_required': False, 'category': 'soft', 'weight': 0.6}
            ],
            'Software Engineer': [
                {'skill': 'Communication', 'difficulty': 'Intermediate', 'importance': 8, 'is_required': True, 'category': 'soft', 'weight': 0.8},
                {'skill': 'Problem Solving', 'difficulty': 'Advanced', 'importance': 9, 'is_required': True, 'category': 'soft', 'weight': 0.9},
                {'skill': 'Teamwork', 'difficulty': 'Intermediate', 'importance': 7, 'is_required': True, 'category': 'soft', 'weight': 0.7},
                {'skill': 'Time Management', 'difficulty': 'Intermediate', 'importance': 6, 'is_required': False, 'category': 'soft', 'weight': 0.6}
            ],
            'Frontend Developer': [
                {'skill': 'Communication', 'difficulty': 'Intermediate', 'importance': 8, 'is_required': True, 'category': 'soft', 'weight': 0.8},
                {'skill': 'Problem Solving', 'difficulty': 'Intermediate', 'importance': 7, 'is_required': True, 'category': 'soft', 'weight': 0.7},
                {'skill': 'Creativity', 'difficulty': 'Intermediate', 'importance': 7, 'is_required': False, 'category': 'soft', 'weight': 0.7},
                {'skill': 'User Empathy', 'difficulty': 'Intermediate', 'importance': 6, 'is_required': False, 'category': 'soft', 'weight': 0.6}
            ],
            'Backend Developer': [
                {'skill': 'Communication', 'difficulty': 'Intermediate', 'importance': 7, 'is_required': True, 'category': 'soft', 'weight': 0.7},
                {'skill': 'Problem Solving', 'difficulty': 'Advanced', 'importance': 8, 'is_required': True, 'category': 'soft', 'weight': 0.8},
                {'skill': 'System Thinking', 'difficulty': 'Advanced', 'importance': 7, 'is_required': False, 'category': 'soft', 'weight': 0.7}
            ],
            'DevOps Engineer': [
                {'skill': 'Communication', 'difficulty': 'Intermediate', 'importance': 7, 'is_required': True, 'category': 'soft', 'weight': 0.7},
                {'skill': 'Problem Solving', 'difficulty': 'Advanced', 'importance': 8, 'is_required': True, 'category': 'soft', 'weight': 0.8},
                {'skill': 'Incident Response', 'difficulty': 'Advanced', 'importance': 7, 'is_required': False, 'category': 'soft', 'weight': 0.7}
            ],
            'Product Manager': [
                {'skill': 'Communication', 'difficulty': 'Advanced', 'importance': 10, 'is_required': True, 'category': 'soft', 'weight': 1.0},
                {'skill': 'Leadership', 'difficulty': 'Advanced', 'importance': 9, 'is_required': True, 'category': 'soft', 'weight': 0.9},
                {'skill': 'Problem Solving', 'difficulty': 'Advanced', 'importance': 9, 'is_required': True, 'category': 'soft', 'weight': 0.9},
                {'skill': 'Strategic Thinking', 'difficulty': 'Advanced', 'importance': 8, 'is_required': True, 'category': 'soft', 'weight': 0.8}
            ]
        }
        
        # Get soft skills for this career, or use default if not found
        default_soft_skills = [
            {'skill': 'Communication', 'difficulty': 'Intermediate', 'importance': 8, 'is_required': True, 'category': 'soft', 'weight': 0.8},
            {'skill': 'Problem Solving', 'difficulty': 'Intermediate', 'importance': 9, 'is_required': True, 'category': 'soft', 'weight': 0.9},
            {'skill': 'Teamwork', 'difficulty': 'Intermediate', 'importance': 7, 'is_required': False, 'category': 'soft', 'weight': 0.7},
            {'skill': 'Leadership', 'difficulty': 'Intermediate', 'importance': 6, 'is_required': False, 'category': 'soft', 'weight': 0.6},
            {'skill': 'Critical Thinking', 'difficulty': 'Intermediate', 'importance': 8, 'is_required': True, 'category': 'soft', 'weight': 0.8}
        ]
        
        soft_skills = soft_skills_mapping.get(career, default_soft_skills)
        return pd.DataFrame(soft_skills)
    
    def _determine_skill_level(self, skill: str, default_level: str) -> str:
        """
        Determine skill level based on skill name and default level
        If no explicit level is provided, use intelligent defaults
        """
        # If default level is provided and not empty, use it
        if default_level and default_level.strip():
            return default_level
        
        # Intelligent default level assignment based on skill characteristics
        skill_lower = skill.lower()
        
        # Core programming languages - typically require intermediate+ level
        core_languages = ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin', 'sql', 'r']
        if skill_lower in core_languages:
            return 'Intermediate'
        
        # Core data science libraries - typically require intermediate level
        core_libraries = ['numpy', 'pandas', 'seaborn', 'matplotlib', 'scikit-learn', 'sklearn']
        if skill_lower in core_libraries:
            return 'Intermediate'
        
        # Advanced frameworks and tools - typically require advanced level
        advanced_tools = ['tensorflow', 'pytorch', 'kubernetes', 'docker', 'spark', 'hadoop', 'kafka', 'elasticsearch', 'deep learning', 'neural networks']
        if skill_lower in advanced_tools:
            return 'Advanced'
        
        # Basic tools and utilities - typically beginner level
        basic_tools = ['git', 'jupyter', 'excel', 'powerpoint', 'word', 'data visualization', 'data cleaning']
        if skill_lower in basic_tools:
            return 'Beginner'
        
        # Data science and ML concepts - vary by complexity
        ml_concepts = {
            'machine learning': 'Intermediate',
            'statistics': 'Intermediate',
            'feature engineering': 'Intermediate',
            'model evaluation': 'Intermediate',
            'a/b testing': 'Intermediate',
            'business intelligence': 'Beginner'
        }
        if skill_lower in ml_concepts:
            return ml_concepts[skill_lower]
        
        # Web development frameworks
        web_frameworks = {
            'react': 'Intermediate',
            'angular': 'Advanced',
            'vue.js': 'Intermediate',
            'node.js': 'Intermediate',
            'django': 'Intermediate',
            'flask': 'Beginner',
            'spring boot': 'Advanced',
            'express.js': 'Beginner'
        }
        if skill_lower in web_frameworks:
            return web_frameworks[skill_lower]
        
        # Cloud platforms
        cloud_platforms = ['aws', 'azure', 'gcp', 'heroku', 'digitalocean']
        if skill_lower in cloud_platforms:
            return 'Intermediate'
        
        # Soft skills - typically intermediate level
        soft_skills = ['communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking', 'creativity']
        if skill_lower in soft_skills:
            return 'Intermediate'
        
        # Default to Beginner for all other skills
        return 'Beginner'
    
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
            
            # Extract missing skills from dictionary format
            missing_skills_list = []
            if isinstance(match['missing_skills'], dict):
                for category, skills in match['missing_skills'].items():
                    if isinstance(skills, list):
                        missing_skills_list.extend([skill['skill'] if isinstance(skill, dict) else skill for skill in skills])
            elif isinstance(match['missing_skills'], list):
                missing_skills_list = [skill['skill'] if isinstance(skill, dict) else skill for skill in match['missing_skills']]
            
            final_analysis.append({
                'career': career,
                'overall_fit': round(combined_fit, 1),
                'skill_match': skill_match,
                'keyword_fit': keyword_fit,
                'matched_skills': match['matched_skills'],
                'missing_skills': missing_skills_list[:5],  # Top 5 missing
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
        """Extract skills from text using pattern matching"""
        # Get all available skills
        all_skills = set(self.career_skills_df['skill'].str.lower().tolist())
        
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
        Generate learning path for target career with improved prioritization and quality
        
        Args:
            target_career: Target career
            user_skills: Current user skills
            
        Returns:
            Learning path with courses, timeline, and progress metrics
        """
        gap_analysis = self.gap_analysis(user_skills, target_career)
        
        if "error" in gap_analysis:
            return gap_analysis
        
        # Get missing skills with prioritization
        required_missing = gap_analysis['required_missing']
        optional_missing = gap_analysis['optional_missing'][:3]  # Limit optional skills
        
        # Prioritize core skills for Data Scientist
        if target_career == 'Data Scientist':
            core_skills = ['Python', 'SQL', 'Statistics', 'Machine Learning', 'Data Cleaning', 
                          'Scikit-learn', 'Model Evaluation', 'Feature Engineering']
            
            # Reorder required missing skills to prioritize core skills
            prioritized_required = []
            other_required = []
            
            for skill_info in required_missing:
                if skill_info['skill'] in core_skills:
                    prioritized_required.append(skill_info)
                else:
                    other_required.append(skill_info)
            
            # Combine prioritized + other required + optional
            missing_skills = prioritized_required + other_required + optional_missing
        else:
            missing_skills = required_missing + optional_missing
        
        # Find relevant courses with quality filtering
        learning_path = {
            'target_career': target_career,
            'current_completion': gap_analysis['completion_percentage'],
            'technical_completion': gap_analysis['required_completion'],
            'soft_skills_completion': 0,  # Will calculate separately
            'phases': [],
            'timeline': {}
        }
        
        # Create learning phases with improved structure
        phases = [
            {'name': 'Foundation', 'level': 'Beginner', 'skills': [], 'courses': [], 'hours': 0},
            {'name': 'Intermediate', 'level': 'Intermediate', 'skills': [], 'courses': [], 'hours': 0},
            {'name': 'Advanced', 'level': 'Advanced', 'skills': [], 'courses': [], 'hours': 0}
        ]
        
        # Categorize missing skills by difficulty with soft skills distribution
        for skill_info in missing_skills:
            skill = skill_info['skill']
            difficulty = skill_info['difficulty']
            category = skill_info.get('category', 'technical')
            
            # Handle soft skills distribution
            if category == 'soft':
                if skill in ['Communication', 'Teamwork']:
                    # Start from Beginner
                    phases[0]['skills'].append(skill_info)
                elif skill in ['Problem Solving', 'Critical Thinking']:
                    # Span all levels - place in Intermediate for balanced learning
                    phases[1]['skills'].append(skill_info)
                elif skill == 'Leadership':
                    # Only in Advanced
                    phases[2]['skills'].append(skill_info)
                else:
                    # Default soft skills to Intermediate
                    phases[1]['skills'].append(skill_info)
            else:
                # Technical skills - use original difficulty
                if difficulty == 'Beginner':
                    phases[0]['skills'].append(skill_info)
                elif difficulty == 'Intermediate':
                    phases[1]['skills'].append(skill_info)
                else:
                    phases[2]['skills'].append(skill_info)
        
        # Find high-quality courses for each phase
        for phase in phases:
            if phase['skills']:
                phase_skills = [s['skill'] for s in phase['skills']]
                
                # Filter courses by skill and level, prioritize high ratings
                available_courses = self.courses_df[
                    (self.courses_df['skill'].isin(phase_skills)) & 
                    (self.courses_df['level'] == phase['level'])
                ].copy()
                
                if not available_courses.empty:
                    # Sort by rating (descending) and prioritize courses ≥ 4.3⭐
                    available_courses = available_courses.sort_values('rating', ascending=False)
                    
                    # Get high-quality courses first (≥ 4.3⭐)
                    high_quality = available_courses[available_courses['rating'] >= 4.3]
                    other_courses = available_courses[available_courses['rating'] < 4.3]
                    
                    # Select courses: high-quality first, then others if needed
                    selected_courses = []
                    if not high_quality.empty:
                        selected_courses.extend(high_quality.head(2).to_dict('records'))
                    
                    # If we need more courses or no high-quality ones, add others
                    if len(selected_courses) < 2 and not other_courses.empty:
                        remaining = 2 - len(selected_courses)
                        selected_courses.extend(other_courses.head(remaining).to_dict('records'))
                    
                    phase['courses'] = selected_courses
                    
                    # Calculate total hours for this phase
                    phase['hours'] = sum(course.get('duration_hours', 0) for course in selected_courses)
                    
                    # Flag courses with low ratings
                    for course in phase['courses']:
                        if course.get('rating', 0) < 4.3:
                            course['low_rating_warning'] = True
                
                learning_path['phases'].append(phase)
        
        # Calculate timeline with 20% buffer
        total_course_hours = sum(phase['hours'] for phase in learning_path['phases'])
        total_study_hours = int(total_course_hours * 1.2)  # 20% buffer for practice
        
        learning_path['timeline'] = {
            'total_course_hours': total_course_hours,
            'total_study_hours': total_study_hours,
            'weeks_10h': max(1, total_study_hours // 10),
            'weeks_15h': max(1, total_study_hours // 15),
            'weeks_20h': max(1, total_study_hours // 20)
        }
        
        # Calculate soft skills completion separately
        soft_skills = [skill for skill in missing_skills if skill.get('category') == 'soft']
        if soft_skills:
            soft_skills_importance = sum(skill.get('importance', 0) for skill in soft_skills)
            soft_skills_matched = sum(skill.get('importance', 0) for skill in soft_skills 
                                    if skill['skill'].lower() in [s.lower() for s in user_skills])
            learning_path['soft_skills_completion'] = min(100, int((soft_skills_matched / soft_skills_importance) * 100)) if soft_skills_importance > 0 else 0
        
        return learning_path
    
    def get_job_market_insights(self, career: str, user_skills: List[str] = None) -> Dict[str, Any]:
        """
        Get comprehensive job market insights for a career with skills matching
        
        Args:
            career: Target career
            user_skills: User's current skills for job matching
            
        Returns:
            Structured job market insights with skills analysis
        """
        if career not in self.salary_demand_df['career'].values:
            return {"error": "Career not found"}
        
        career_data = self.salary_demand_df[
            self.salary_demand_df['career'] == career
        ].iloc[0]
        
        # Get recent job posts with enhanced filtering
        recent_jobs = self.job_posts_df[
            self.job_posts_df['title'].str.contains(career, case=False, na=False)
        ].head(8)  # Get more jobs for better variety
        
        # Process job listings with skills matching
        enhanced_jobs = []
        for _, job in recent_jobs.iterrows():
            job_dict = job.to_dict()
            
            # Clean and format job data
            job_dict['formatted_salary'] = f"${job['min_salary']:,} – ${job['max_salary']:,}"
            job_dict['avg_salary'] = (job['min_salary'] + job['max_salary']) // 2
            
            # Parse required skills
            required_skills = [skill.strip() for skill in job['required_skills'].split(',')]
            job_dict['required_skills'] = required_skills
            
            # Skills matching analysis
            if user_skills:
                user_skill_set = set([skill.lower() for skill in user_skills])
                job_skill_set = set([skill.lower() for skill in required_skills])
                
                # Calculate match score
                matched_skills = user_skill_set.intersection(job_skill_set)
                match_score = len(matched_skills) / len(job_skill_set) * 100 if job_skill_set else 0
                
                job_dict['skills_analysis'] = {
                    'matched_skills': list(matched_skills),
                    'missing_skills': list(job_skill_set - user_skill_set),
                    'match_score': round(match_score, 1),
                    'total_skills': len(job_skill_set),
                    'matched_count': len(matched_skills)
                }
            else:
                job_dict['skills_analysis'] = {
                    'matched_skills': [],
                    'missing_skills': required_skills,
                    'match_score': 0.0,
                    'total_skills': len(required_skills),
                    'matched_count': 0
                }
            
            # Format experience level
            experience_mapping = {
                'Entry': 'Junior',
                'Mid': 'Mid-level',
                'Senior': 'Senior',
                'Lead': 'Lead',
                'Principal': 'Principal'
            }
            job_dict['experience_display'] = experience_mapping.get(job['experience_level'], job['experience_level'])
            
            # Format job type
            job_type_mapping = {
                'Full-time': 'Full-time',
                'Part-time': 'Part-time',
                'Contract': 'Contract',
                'Remote': 'Remote'
            }
            job_dict['job_type_display'] = job_type_mapping.get(job['job_type'], job['job_type'])
            
            enhanced_jobs.append(job_dict)
        
        # Sort jobs by match score if user skills provided
        if user_skills:
            enhanced_jobs.sort(key=lambda x: x['skills_analysis']['match_score'], reverse=True)
        
        # Calculate market insights
        demand_status = self._get_demand_status(career_data['demand_index'])
        growth_trend = self._get_growth_trend(career_data['growth_rate'])
        
        # Format salary data
        salary_data = {
                'min': career_data['min_salary'],
                'max': career_data['max_salary'],
            'avg': career_data['avg_salary'],
            'formatted_range': f"${career_data['min_salary']:,} – ${career_data['max_salary']:,}",
            'formatted_avg': f"${career_data['avg_salary']:,}"
        }
        
        # Market overview
        market_overview = {
            'demand_level': demand_status['level'],
            'demand_description': demand_status['description'],
            'growth_trend': growth_trend['trend'],
            'growth_description': growth_trend['description'],
            'remote_opportunities': "High" if career_data['remote_friendly'] else "Limited"
        }
        
        # Top countries with flags
        country_flags = {
            'United States': '🇺🇸', 'United Kingdom': '🇬🇧', 'Canada': '🇨🇦',
            'Germany': '🇩🇪', 'France': '🇫🇷', 'Australia': '🇦🇺',
            'Japan': '🇯🇵', 'Singapore': '🇸🇬', 'Switzerland': '🇨🇭',
            'Spain': '🇪🇸', 'Brazil': '🇧🇷', 'India': '🇮🇳',
            'Netherlands': '🇳🇱', 'Sweden': '🇸🇪'
        }
        
        top_countries = []
        for country in career_data['top_countries'].split(', '):
            flag = country_flags.get(country, '🌍')
            top_countries.append({
                'name': country,
                'flag': flag
            })
        
        return {
            'career': career,
            'salary_data': salary_data,
            'market_overview': market_overview,
            'demand_metrics': {
            'demand_index': career_data['demand_index'],
            'growth_rate': career_data['growth_rate'],
                'remote_friendly': career_data['remote_friendly']
            },
            'top_countries': top_countries,
            'job_listings': enhanced_jobs[:6],  # Show top 6 jobs
            'total_jobs_found': len(enhanced_jobs),
            'skills_analysis_enabled': user_skills is not None
        }
    
    def _get_demand_status(self, demand_index: int) -> Dict[str, str]:
        """Get demand status description based on demand index"""
        if demand_index >= 85:
            return {
                'level': 'Very High',
                'description': 'Excellent job prospects with high demand'
            }
        elif demand_index >= 70:
            return {
                'level': 'High',
                'description': 'Strong job market with good opportunities'
            }
        elif demand_index >= 50:
            return {
                'level': 'Moderate',
                'description': 'Stable job market with steady demand'
            }
        else:
            return {
                'level': 'Lower',
                'description': 'Competitive market, focus on differentiation'
            }
    
    def _get_growth_trend(self, growth_rate: int) -> Dict[str, str]:
        """Get growth trend description based on growth rate"""
        if growth_rate >= 20:
            return {
                'trend': '📈 Rapid Growth',
                'description': f'Fast-growing field with {growth_rate}% annual growth'
            }
        elif growth_rate >= 10:
            return {
                'trend': '📈 Steady Growth',
                'description': f'Growing field with {growth_rate}% annual growth'
            }
        elif growth_rate >= 5:
            return {
                'trend': '➡️ Stable',
                'description': f'Stable field with {growth_rate}% annual growth'
            }
        else:
            return {
                'trend': '📉 Slow Growth',
                'description': f'Slow growth field with {growth_rate}% annual growth'
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

    def _get_skill_synonyms(self, skill_name: str) -> List[str]:
        """
        Get synonyms for a given skill name
        
        Args:
            skill_name: The skill name to find synonyms for
            
        Returns:
            List of synonyms including the original skill name
        """
        skill_lower = skill_name.lower()
        synonyms = [skill_name]  # Always include the original skill name
        
        # Check if this skill has synonyms in our mapping
        for canonical_skill, skill_synonyms in self._get_skill_synonym_mapping().items():
            if skill_lower == canonical_skill.lower():
                synonyms.extend(skill_synonyms)
                break
            # Also check if the skill is in the synonyms list
            elif skill_lower in [s.lower() for s in skill_synonyms]:
                synonyms.extend(skill_synonyms)
                break
        
        return list(set(synonyms))  # Remove duplicates
    
    def _get_skill_synonym_mapping(self) -> Dict[str, List[str]]:
        """Get the skill synonym mapping dictionary"""
        return {
            # Programming Languages
            "python": ["python", "py", "python3", "python3.8", "python3.9", "python3.10"],
            "sql": ["sql", "mysql", "postgresql", "sqlite", "tsql", "plsql", "database", "db", "rdbms"],
            "java": ["java", "jdk", "jvm", "spring", "maven", "gradle"],
            "javascript": ["javascript", "js", "ecmascript", "es6", "es2015", "es2017", "es2020"],
            "c++": ["c++", "cpp", "c plus plus", "stl", "boost"],
            "c#": ["c#", "csharp", "dotnet", ".net", "asp.net", "entity framework"],
            
            # Data Science & ML
            "machine learning": ["machine learning", "ml", "ai", "artificial intelligence", "deep learning", "neural networks", "predictive modeling"],
            "deep learning": ["deep learning", "neural networks", "cnn", "rnn", "lstm", "transformer", "bert", "gpt"],
            "data science": ["data science", "data scientist", "analytics", "predictive analytics"],
            "statistics": ["statistics", "stats", "statistical analysis", "hypothesis testing", "regression", "correlation", "anova"],
            
            # Data Visualization & Tools
            "data visualization": ["data visualization", "visualization", "viz", "matplotlib", "seaborn", "plotly", "tableau", "powerbi", "d3.js", "ggplot"],
            "visualization": ["visualization", "data visualization", "viz", "charts", "graphs", "dashboards", "data viz"],
            "pandas": ["pandas", "pd", "dataframe", "data manipulation", "data analysis"],
            "numpy": ["numpy", "np", "numerical computing", "arrays", "matrices"],
            "scikit-learn": ["scikit-learn", "sklearn", "machine learning library", "ml library", "scikit"],
            
            # ML/AI Frameworks
            "tensorflow": ["tensorflow", "tf", "deep learning framework", "neural networks", "keras"],
            "pytorch": ["pytorch", "torch", "deep learning", "ml framework", "neural networks"],
            "keras": ["keras", "deep learning", "neural networks", "tensorflow"],
            
            # Web Development
            "react": ["react", "reactjs", "react.js", "jsx", "hooks", "redux", "context"],
            "angular": ["angular", "angularjs", "ng", "angular 2+", "angular material"],
            "vue.js": ["vue", "vue.js", "vuejs", "vue 3", "composition api"],
            "node.js": ["node.js", "nodejs", "node", "express", "npm", "yarn"],
            "html": ["html", "html5", "markup", "semantic html", "accessibility"],
            "css": ["css", "css3", "styling", "responsive design", "flexbox", "grid", "sass", "less"],
            "typescript": ["typescript", "ts", "typed javascript", "type safety"],
            
            # Python Web Frameworks
            "flask": ["flask", "python web framework", "microframework", "wsgi"],
            "django": ["django", "python web framework", "mvt", "admin panel", "orm"],
            "fastapi": ["fastapi", "python web framework", "async", "api", "pydantic"],
            
            # Java Frameworks
            "spring boot": ["spring boot", "spring", "java framework", "dependency injection", "aop"],
            "spring": ["spring", "spring framework", "spring boot", "java framework"],
            
            # DevOps & Cloud
            "docker": ["docker", "containerization", "containers", "dockerfile", "docker compose"],
            "kubernetes": ["kubernetes", "k8s", "container orchestration", "microservices", "deployment"],
            "aws": ["aws", "amazon web services", "ec2", "s3", "lambda", "rds", "cloudfront", "route53"],
            "azure": ["azure", "microsoft azure", "cloud computing", "vm", "blob storage", "functions"],
            "gcp": ["gcp", "google cloud platform", "google cloud", "compute engine", "cloud storage"],
            
            # Big Data
            "hadoop": ["hadoop", "apache hadoop", "big data", "mapreduce", "hdfs", "yarn"],
            "spark": ["spark", "apache spark", "big data", "distributed computing", "dataframes", "streaming"],
            "kafka": ["kafka", "apache kafka", "streaming", "message queue", "event streaming"],
            
            # Databases
            "mongodb": ["mongodb", "nosql", "document database", "mongo", "aggregation"],
            "postgresql": ["postgresql", "postgres", "relational database", "rdbms", "acid"],
            "mysql": ["mysql", "relational database", "rdbms", "maria db", "innodb"],
            "redis": ["redis", "in-memory database", "cache", "key-value store", "data structures"],
            
            # Infrastructure & Tools
            "terraform": ["terraform", "infrastructure as code", "iac", "hashicorp", "provisioning"],
            "jenkins": ["jenkins", "ci/cd", "continuous integration", "automation", "pipeline"],
            "git": ["git", "github", "gitlab", "version control", "vcs", "source control"],
            "linux": ["linux", "unix", "ubuntu", "centos", "debian", "red hat", "shell"],
            
            # Testing
            "selenium": ["selenium", "web testing", "automated testing", "browser automation", "webdriver"],
            "junit": ["junit", "java testing", "unit testing", "test framework", "tdd"],
            "pytest": ["pytest", "python testing", "unit testing", "test framework", "fixtures"],
            
            # Design & UX
            "figma": ["figma", "ui design", "ux design", "prototyping", "design tools", "collaboration"],
            "adobe xd": ["adobe xd", "ux design", "prototyping", "design tools", "wireframing"],
            "sketch": ["sketch", "ui design", "mac design tool", "prototyping", "design systems"],
            
            # Project Management
            "agile": ["agile", "scrum", "kanban", "project management", "iterative", "adaptive"],
            "scrum": ["scrum", "agile methodology", "sprint planning", "standup", "retrospective"],
            "jira": ["jira", "project management", "issue tracking", "agile tools", "atlassian"],
            
            # Specialized Skills
            "etl": ["etl", "extract transform load", "data pipeline", "data integration", "data processing"],
            "data modeling": ["data modeling", "database design", "schema design", "normalization", "erd"],
            "api": ["api", "rest api", "graphql", "web services", "endpoints", "microservices"],
            "microservices": ["microservices", "microservice architecture", "distributed systems", "service mesh"],
            "ci/cd": ["ci/cd", "continuous integration", "continuous deployment", "devops", "automation"],
            "mlops": ["mlops", "machine learning operations", "model deployment", "model monitoring", "ml infrastructure"]
            }

# Example usage and testing
if __name__ == "__main__":
    from ai_pipeline_simple import CareerRecommendationPipeline
    from file_parser import parse_uploaded_file, validate_resume_content, get_file_info
    from enhanced_resume_analyzer import EnhancedResumeAnalyzer

    # Initialize pipeline
    pipeline = CareerRecommendationPipeline()
    
    # Test skill matching
    test_skills = ["Python", "SQL", "Machine Learning", "Statistics"]
    matches = pipeline.skill_matching(test_skills)
    print("Skill Matches:", matches[:3])
    
    # Test gap analysis
    gap = pipeline.gap_analysis(test_skills, "Data Scientist")
    print("Gap Analysis:", gap)
