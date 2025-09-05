"""
Enhanced Peer Benchmarking with accurate statistics and career-specific filtering
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from typing import List, Dict, Any
import random


class EnhancedPeerBenchmarking:
    def __init__(self, career_skills_df, peer_profiles_df=None):
        self.career_skills_df = career_skills_df
        self.peer_profiles_df = peer_profiles_df
        
        # Career-specific skill mappings
        self.career_skill_mappings = {
            'Data Scientist': {
                'core': ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Pandas', 'NumPy', 'Scikit-learn'],
                'intermediate': ['R', 'TensorFlow', 'PyTorch', 'Tableau', 'Power BI', 'Jupyter', 'Git'],
                'emerging': ['MLOps', 'Docker', 'AWS', 'Azure', 'Kubernetes', 'Apache Spark', 'Deep Learning'],
                'soft': ['Communication', 'Problem Solving', 'Critical Thinking', 'Teamwork']
            },
            'Machine Learning Engineer': {
                'core': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'Docker', 'Git', 'Linux'],
                'intermediate': ['Kubernetes', 'AWS', 'MLOps', 'Apache Spark', 'SQL', 'Statistics'],
                'emerging': ['Kubeflow', 'MLflow', 'Apache Airflow', 'Terraform', 'CI/CD', 'Model Monitoring'],
                'soft': ['Problem Solving', 'Communication', 'Collaboration', 'Attention to Detail']
            },
            'Data Analyst': {
                'core': ['SQL', 'Excel', 'Python', 'Statistics', 'Data Visualization', 'Tableau', 'Power BI'],
                'intermediate': ['R', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'Business Intelligence'],
                'emerging': ['Machine Learning', 'Cloud Analytics', 'Advanced Analytics', 'Automation'],
                'soft': ['Communication', 'Business Acumen', 'Critical Thinking', 'Attention to Detail']
            },
            'Software Engineer': {
                'core': ['Python', 'Java', 'JavaScript', 'Git', 'SQL', 'Data Structures', 'Algorithms'],
                'intermediate': ['React', 'Node.js', 'Docker', 'REST APIs', 'Testing', 'Agile'],
                'emerging': ['Kubernetes', 'Microservices', 'Cloud Computing', 'DevOps', 'GraphQL'],
                'soft': ['Problem Solving', 'Teamwork', 'Communication', 'Adaptability']
            }
        }
        
        # Generate realistic peer data if not provided
        if self.peer_profiles_df is None or self.peer_profiles_df.empty:
            self.peer_profiles_df = self._generate_realistic_peer_data()
    
    def _generate_realistic_peer_data(self):
        """Generate realistic peer profiles for different careers"""
        careers = list(self.career_skill_mappings.keys())
        peer_data = []
        
        # Generate 50-100 peers per career
        for career in careers:
            skills_mapping = self.career_skill_mappings[career]
            all_career_skills = (skills_mapping['core'] + 
                               skills_mapping['intermediate'] + 
                               skills_mapping['emerging'] + 
                               skills_mapping['soft'])
            
            num_peers = random.randint(50, 100)
            
            for i in range(num_peers):
                # Generate realistic experience (0-15 years, weighted toward 3-8 years)
                experience = max(0, int(np.random.normal(5.5, 2.5)))
                experience = min(experience, 15)
                
                # Generate salary based on experience and career
                base_salary = {
                    'Data Scientist': 95000,
                    'Machine Learning Engineer': 110000,
                    'Data Analyst': 70000,
                    'Software Engineer': 85000
                }.get(career, 80000)
                
                # Salary increases with experience
                salary = base_salary + (experience * 8000) + random.randint(-15000, 25000)
                salary = max(salary, 45000)  # Minimum salary
                
                # Generate skills based on experience level
                peer_skills = []
                
                # Core skills (high probability)
                for skill in skills_mapping['core']:
                    if random.random() < 0.85:  # 85% chance
                        peer_skills.append(skill)
                
                # Intermediate skills (medium probability, higher with experience)
                for skill in skills_mapping['intermediate']:
                    prob = 0.4 + (experience * 0.05)  # Increases with experience
                    if random.random() < min(prob, 0.9):
                        peer_skills.append(skill)
                
                # Emerging skills (lower probability, much higher with experience)
                for skill in skills_mapping['emerging']:
                    prob = 0.1 + (experience * 0.08)  # Strongly increases with experience
                    if random.random() < min(prob, 0.8):
                        peer_skills.append(skill)
                
                # Soft skills (medium probability)
                for skill in skills_mapping['soft']:
                    if random.random() < 0.6:
                        peer_skills.append(skill)
                
                # Ensure minimum skills
                if len(peer_skills) < 5:
                    missing_core = [s for s in skills_mapping['core'] if s not in peer_skills]
                    peer_skills.extend(missing_core[:3])
                
                education_options = ['Bachelor\'s', 'Master\'s', 'PhD', 'Bootcamp', 'Self-taught']
                education_weights = [0.4, 0.35, 0.15, 0.08, 0.02]
                education = np.random.choice(education_options, p=education_weights)
                
                peer_data.append({
                    'career': career,
                    'experience_years': experience,
                    'salary': salary,
                    'education': education,
                    'skills': ', '.join(peer_skills),
                    'skill_count': len(peer_skills)
                })
        
        return pd.DataFrame(peer_data)
    
    def analyze_peer_benchmarking(self, user_skills: List[str], target_career: str) -> Dict[str, Any]:
        """Enhanced peer benchmarking with accurate statistics and insights"""
        
        # Normalize user skills
        user_skills_normalized = [skill.strip().lower() for skill in user_skills]
        user_skill_set = set(user_skills_normalized)
        
        # Filter peers by target career
        career_peers = self.peer_profiles_df[
            self.peer_profiles_df['career'] == target_career
        ].copy()
        
        if career_peers.empty:
            return {"error": f"No peer data available for {target_career}"}
        
        # Remove duplicates and clean data
        career_peers = career_peers.drop_duplicates()
        career_peers = career_peers[career_peers['salary'] > 0]  # Remove invalid salaries
        
        # Always calculate skill counts to ensure consistency
        career_peers = career_peers.copy()
        career_peers['skill_count'] = career_peers['skills'].apply(
            lambda x: len([s.strip() for s in str(x).split(',') if s.strip()]) if pd.notna(x) else 0
        )
        
        # Calculate accurate statistics
        peer_stats = {
            'avg_experience_years': round(career_peers['experience_years'].mean(), 1),
            'avg_salary': int(career_peers['salary'].mean()),
            'avg_skill_count': round(career_peers['skill_count'].mean(), 1),
            'total_peers': len(career_peers),
            'salary_range': {
                'min': int(career_peers['salary'].min()),
                'max': int(career_peers['salary'].max()),
                'median': int(career_peers['salary'].median())
            }
        }
        
        # Analyze skills across all peers
        all_peer_skills = []
        peer_skill_analysis = []
        
        for _, peer in career_peers.iterrows():
            peer_skills_raw = [s.strip() for s in peer['skills'].split(',')]
            peer_skills_normalized = [s.lower() for s in peer_skills_raw]
            peer_skill_set = set(peer_skills_normalized)
            
            # Calculate skill overlap
            skill_overlap_count = len(user_skill_set.intersection(peer_skill_set))
            skill_overlap_percentage = (skill_overlap_count / max(len(peer_skill_set), 1)) * 100
            
            peer_skill_analysis.append({
                'experience_years': peer['experience_years'],
                'salary': peer['salary'],
                'education': peer['education'],
                'skill_count': len(peer_skills_raw),
                'skill_overlap_count': skill_overlap_count,
                'skill_overlap_percentage': round(skill_overlap_percentage, 1),
                'skills': peer_skills_raw,
                'matched_skills': [s for s in peer_skills_raw if s.lower() in user_skill_set]
            })
            
            all_peer_skills.extend(peer_skills_normalized)
        
        # Find most common skills
        skill_frequency = Counter(all_peer_skills)
        most_common_skills = skill_frequency.most_common(15)
        
        # Calculate user's skill coverage
        peer_skill_set = set(all_peer_skills)
        user_coverage = len(user_skill_set.intersection(peer_skill_set))
        total_peer_skills = len(peer_skill_set)
        coverage_percentage = (user_coverage / max(total_peer_skills, 1)) * 100
        
        # Categorize missing skills
        missing_skills = self._categorize_missing_skills(
            user_skills_normalized, target_career, most_common_skills
        )
        
        # Get top peer profiles (sorted by skill overlap)
        top_peer_profiles = sorted(
            peer_skill_analysis, 
            key=lambda x: x['skill_overlap_percentage'], 
            reverse=True
        )[:5]
        
        # Calculate peer comparison metrics
        user_experience = self._estimate_user_experience(user_skills, target_career)
        experience_percentile = self._calculate_percentile(
            user_experience, career_peers['experience_years'].tolist()
        )
        
        skill_count_percentile = self._calculate_percentile(
            len(user_skills), career_peers['skill_count'].tolist()
        )
        
        return {
            'target_career': target_career,
            'statistics': peer_stats,
            'user_metrics': {
                'skill_coverage_percentage': round(coverage_percentage, 1),
                'skills_in_common': user_coverage,
                'total_peer_skills': total_peer_skills,
                'estimated_experience': user_experience,
                'experience_percentile': experience_percentile,
                'skill_count_percentile': skill_count_percentile
            },
            'most_common_skills': most_common_skills,
            'missing_skills': missing_skills,
            'peer_profiles': top_peer_profiles,
            'skill_distribution': self._analyze_skill_distribution(most_common_skills, user_skill_set)
        }
    
    def _categorize_missing_skills(self, user_skills: List[str], career: str, common_skills: List[tuple]) -> Dict[str, List[str]]:
        """Categorize missing skills into core, intermediate, and emerging"""
        if career not in self.career_skill_mappings:
            return {'core': [], 'intermediate': [], 'emerging': []}
        
        skill_mapping = self.career_skill_mappings[career]
        user_skill_set = set(user_skills)
        
        # Get top 10 most common skills from peers
        top_peer_skills = [skill for skill, _ in common_skills[:10]]
        
        missing_skills = {
            'core': [],
            'intermediate': [],
            'emerging': []
        }
        
        # Check core skills
        for skill in skill_mapping['core']:
            if skill.lower() not in user_skill_set:
                missing_skills['core'].append(skill)
        
        # Check intermediate skills that are also common among peers
        for skill in skill_mapping['intermediate']:
            if skill.lower() not in user_skill_set and skill.lower() in top_peer_skills:
                missing_skills['intermediate'].append(skill)
        
        # Check emerging skills that are common among experienced peers
        for skill in skill_mapping['emerging']:
            if skill.lower() not in user_skill_set and skill.lower() in top_peer_skills:
                missing_skills['emerging'].append(skill)
        
        return missing_skills
    
    def _estimate_user_experience(self, user_skills: List[str], career: str) -> int:
        """Estimate user experience based on skills"""
        if career not in self.career_skill_mappings:
            return 2
        
        skill_mapping = self.career_skill_mappings[career]
        user_skill_set = set([s.lower() for s in user_skills])
        
        # Count skills in each category
        core_count = sum(1 for s in skill_mapping['core'] if s.lower() in user_skill_set)
        intermediate_count = sum(1 for s in skill_mapping['intermediate'] if s.lower() in user_skill_set)
        emerging_count = sum(1 for s in skill_mapping['emerging'] if s.lower() in user_skill_set)
        
        # Estimate experience based on skill distribution
        base_experience = 1
        base_experience += core_count * 0.5
        base_experience += intermediate_count * 0.8
        base_experience += emerging_count * 1.2
        
        return min(int(base_experience), 12)  # Cap at 12 years
    
    def _calculate_percentile(self, value: float, data_list: List[float]) -> int:
        """Calculate percentile of value in data list"""
        if not data_list:
            return 50
        
        sorted_data = sorted(data_list)
        position = sum(1 for x in sorted_data if x <= value)
        percentile = (position / len(sorted_data)) * 100
        return int(percentile)
    
    def _analyze_skill_distribution(self, common_skills: List[tuple], user_skills: set) -> Dict[str, Any]:
        """Analyze skill distribution for visualization"""
        top_10_skills = common_skills[:10]
        
        skill_analysis = []
        for skill, frequency in top_10_skills:
            has_skill = skill in user_skills
            skill_analysis.append({
                'skill': skill.title(),
                'frequency': frequency,
                'percentage': round((frequency / sum(freq for _, freq in common_skills)) * 100, 1),
                'user_has': has_skill
            })
        
        return {
            'top_skills': skill_analysis,
            'user_coverage': sum(1 for item in skill_analysis if item['user_has']),
            'total_top_skills': len(skill_analysis)
        }
