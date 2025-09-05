"""
AI Career Benchmarking Assistant
Structured analysis workflow for comparing user skills against realistic peer data
"""

import pandas as pd
import numpy as np
from collections import Counter
from typing import List, Dict, Any, Tuple
import random


class AICareerBenchmarkingAssistant:
    def __init__(self):
        # Career-specific skill mappings with realistic market data
        self.career_profiles = {
            'Data Scientist': {
                'core_skills': ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Pandas', 'NumPy', 'Data Analysis'],
                'emerging_skills': ['MLOps', 'Deep Learning', 'TensorFlow', 'PyTorch', 'AWS', 'Docker', 'Kubernetes'],
                'soft_skills': ['Communication', 'Problem Solving', 'Critical Thinking', 'Business Acumen'],
                'base_salary': 95000,
                'experience_range': (2, 12),
                'education_dist': {'Bachelor\'s': 0.35, 'Master\'s': 0.45, 'PhD': 0.15, 'Bootcamp': 0.05}
            },
            'ML Engineer': {
                'core_skills': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'Docker', 'Git', 'Linux', 'APIs'],
                'emerging_skills': ['MLOps', 'Kubernetes', 'Apache Spark', 'Model Deployment', 'CI/CD', 'Cloud Computing'],
                'soft_skills': ['Problem Solving', 'Collaboration', 'System Design', 'Attention to Detail'],
                'base_salary': 110000,
                'experience_range': (3, 15),
                'education_dist': {'Bachelor\'s': 0.50, 'Master\'s': 0.35, 'PhD': 0.10, 'Bootcamp': 0.05}
            },
            'Data Analyst': {
                'core_skills': ['SQL', 'Excel', 'Python', 'Tableau', 'Power BI', 'Statistics', 'Data Visualization'],
                'emerging_skills': ['R', 'Machine Learning', 'Advanced Analytics', 'Cloud Analytics', 'Automation'],
                'soft_skills': ['Communication', 'Business Acumen', 'Critical Thinking', 'Presentation Skills'],
                'base_salary': 70000,
                'experience_range': (1, 10),
                'education_dist': {'Bachelor\'s': 0.60, 'Master\'s': 0.25, 'PhD': 0.05, 'Bootcamp': 0.10}
            },
            'Software Engineer': {
                'core_skills': ['Python', 'JavaScript', 'Java', 'Git', 'SQL', 'Data Structures', 'Algorithms', 'APIs'],
                'emerging_skills': ['React', 'Node.js', 'Docker', 'Kubernetes', 'Cloud Computing', 'Microservices'],
                'soft_skills': ['Problem Solving', 'Teamwork', 'Communication', 'Adaptability'],
                'base_salary': 85000,
                'experience_range': (1, 12),
                'education_dist': {'Bachelor\'s': 0.55, 'Master\'s': 0.25, 'PhD': 0.05, 'Bootcamp': 0.15}
            }
        }
    
    def analyze_career_benchmarking(self, user_skills: List[str], target_career: str, 
                                  user_experience: int = None) -> Dict[str, Any]:
        """
        Complete AI career benchmarking analysis following structured workflow
        """
        
        # Step 1: Input Parsing
        if target_career not in self.career_profiles:
            return {"error": f"Career '{target_career}' not supported. Available: {list(self.career_profiles.keys())}"}
        
        user_skills_normalized = [skill.strip().lower() for skill in user_skills if skill.strip()]
        if not user_skills_normalized:
            return {"error": "Please provide at least one skill"}
        
        # Step 2: Peer Data Generation
        peer_profiles = self._generate_realistic_peer_group(target_career, sample_size=8)
        
        # Step 3: Peer Statistics & Rankings
        peer_stats = self._calculate_peer_statistics(peer_profiles)
        user_rankings = self._calculate_user_rankings(user_skills_normalized, user_experience, 
                                                    peer_profiles, target_career)
        
        # Step 4: Skills Gap Analysis
        skills_analysis = self._analyze_skills_gap(user_skills_normalized, target_career, peer_profiles)
        
        # Step 5: Generate Final Output
        return self._format_analysis_output(
            target_career, user_skills, peer_stats, user_rankings, 
            skills_analysis, peer_profiles[:5]  # Top 5 peers for display
        )
    
    def _generate_realistic_peer_group(self, career: str, sample_size: int = 8) -> List[Dict]:
        """Generate realistic peer profiles with no duplicates or invalid data"""
        career_profile = self.career_profiles[career]
        peers = []
        used_combinations = set()
        
        for i in range(sample_size):
            # Generate unique peer profile
            attempts = 0
            while attempts < 50:  # Prevent infinite loop
                # Experience (weighted toward mid-range)
                min_exp, max_exp = career_profile['experience_range']
                experience = max(min_exp, int(np.random.normal((min_exp + max_exp) / 2, 2)))
                experience = min(experience, max_exp)
                
                # Education (based on career distribution)
                education = np.random.choice(
                    list(career_profile['education_dist'].keys()),
                    p=list(career_profile['education_dist'].values())
                )
                
                # Salary (experience-based with realistic variance)
                base_salary = career_profile['base_salary']
                salary = base_salary + (experience * 7000) + random.randint(-12000, 20000)
                salary = max(salary, 40000)  # Minimum salary floor
                
                # Create unique identifier
                peer_id = (experience, education, salary // 5000)  # Group salary by 5k ranges
                
                if peer_id not in used_combinations:
                    used_combinations.add(peer_id)
                    break
                attempts += 1
            
            # Generate skills based on experience and career
            peer_skills = self._generate_peer_skills(career, experience)
            
            peers.append({
                'experience_years': experience,
                'education': education,
                'salary': salary,
                'skills': peer_skills,
                'skill_count': len(peer_skills)
            })
        
        return peers
    
    def _generate_peer_skills(self, career: str, experience: int) -> List[str]:
        """Generate realistic skill set for a peer based on experience"""
        career_profile = self.career_profiles[career]
        peer_skills = []
        
        # Core skills (high probability, increases with experience)
        for skill in career_profile['core_skills']:
            prob = 0.7 + min(experience * 0.05, 0.25)  # 70-95% chance
            if random.random() < prob:
                peer_skills.append(skill)
        
        # Emerging skills (lower probability, strongly tied to experience)
        for skill in career_profile['emerging_skills']:
            prob = max(0.1, min(experience * 0.08, 0.75))  # 10-75% chance
            if random.random() < prob:
                peer_skills.append(skill)
        
        # Soft skills (medium probability)
        for skill in career_profile['soft_skills']:
            if random.random() < 0.6:  # 60% chance
                peer_skills.append(skill)
        
        # Ensure minimum skill count
        if len(peer_skills) < 4:
            missing_core = [s for s in career_profile['core_skills'] if s not in peer_skills]
            peer_skills.extend(missing_core[:2])
        
        return peer_skills
    
    def _calculate_peer_statistics(self, peers: List[Dict]) -> Dict[str, Any]:
        """Calculate comprehensive peer market statistics"""
        experiences = [p['experience_years'] for p in peers]
        salaries = [p['salary'] for p in peers]
        skill_counts = [p['skill_count'] for p in peers]
        
        return {
            'total_peers': len(peers),
            'avg_experience': round(np.mean(experiences), 1),
            'median_experience': round(np.median(experiences), 1),
            'avg_salary': int(np.mean(salaries)),
            'median_salary': int(np.median(salaries)),
            'salary_range': {'min': min(salaries), 'max': max(salaries)},
            'avg_skill_count': round(np.mean(skill_counts), 1),
            'median_skill_count': round(np.median(skill_counts), 1)
        }
    
    def _calculate_user_rankings(self, user_skills: List[str], user_experience: int,
                               peers: List[Dict], career: str) -> Dict[str, Any]:
        """Calculate user's percentile rankings against peers"""
        
        # Estimate user experience if not provided
        if user_experience is None:
            user_experience = self._estimate_experience_from_skills(user_skills, career)
        
        # Calculate percentiles
        peer_experiences = [p['experience_years'] for p in peers]
        peer_skill_counts = [p['skill_count'] for p in peers]
        peer_salaries = [p['salary'] for p in peers]
        
        exp_percentile = self._calculate_percentile(user_experience, peer_experiences)
        skill_count_percentile = self._calculate_percentile(len(user_skills), peer_skill_counts)
        
        # Calculate skill coverage
        all_peer_skills = set()
        for peer in peers:
            all_peer_skills.update([s.lower() for s in peer['skills']])
        
        user_skill_set = set(user_skills)
        skill_coverage = len(user_skill_set.intersection(all_peer_skills)) / len(all_peer_skills) * 100
        
        # Estimate salary percentile
        estimated_salary = self._estimate_salary(user_experience, career, len(user_skills))
        salary_percentile = self._calculate_percentile(estimated_salary, peer_salaries)
        
        return {
            'experience_years': user_experience,
            'experience_percentile': exp_percentile,
            'skill_count': len(user_skills),
            'skill_count_percentile': skill_count_percentile,
            'skill_coverage_percentage': round(skill_coverage, 1),
            'estimated_salary': estimated_salary,
            'salary_percentile': salary_percentile
        }
    
    def _analyze_skills_gap(self, user_skills: List[str], career: str, 
                          peers: List[Dict]) -> Dict[str, Any]:
        """Comprehensive skills gap analysis"""
        career_profile = self.career_profiles[career]
        user_skill_set = set(user_skills)
        
        # Analyze peer skills frequency
        all_peer_skills = []
        for peer in peers:
            all_peer_skills.extend([s.lower() for s in peer['skills']])
        
        skill_frequency = Counter(all_peer_skills)
        common_skills = skill_frequency.most_common(15)
        
        # Categorize missing skills
        missing_core = []
        missing_emerging = []
        
        for skill in career_profile['core_skills']:
            if skill.lower() not in user_skill_set:
                missing_core.append(skill)
        
        for skill in career_profile['emerging_skills']:
            if skill.lower() not in user_skill_set:
                missing_emerging.append(skill)
        
        # Calculate skill overlaps with peers
        peer_overlaps = []
        for peer in peers:
            peer_skill_set = set([s.lower() for s in peer['skills']])
            overlap_count = len(user_skill_set.intersection(peer_skill_set))
            overlap_percentage = (overlap_count / len(peer_skill_set)) * 100 if peer_skill_set else 0
            peer_overlaps.append({
                'peer_index': len(peer_overlaps),
                'overlap_count': overlap_count,
                'overlap_percentage': round(overlap_percentage, 1),
                'peer_skills': peer['skills']
            })
        
        return {
            'most_common_skills': common_skills,
            'missing_skills': {
                'core': missing_core[:5],  # Top 5 missing core skills
                'emerging': missing_emerging[:5]  # Top 5 missing emerging skills
            },
            'skill_overlaps': sorted(peer_overlaps, key=lambda x: x['overlap_percentage'], reverse=True),
            'skills_in_common': len([s for s, _ in common_skills if s in user_skill_set]),
            'total_market_skills': len(set(all_peer_skills))
        }
    
    def _format_analysis_output(self, career: str, user_skills: List[str], peer_stats: Dict,
                              user_rankings: Dict, skills_analysis: Dict, 
                              sample_peers: List[Dict]) -> Dict[str, Any]:
        """Format analysis into UI-friendly structure with icons and clear sections"""
        
        return {
            'target_career': career,
            'analysis_sections': {
                'user_position': {
                    'title': '🎯 Your Position Among Peers',
                    'metrics': {
                        'skill_coverage': {
                            'value': user_rankings['skill_coverage_percentage'],
                            'label': 'Skill Coverage',
                            'format': 'percentage',
                            'benchmark': 70.0
                        },
                        'experience_rank': {
                            'value': user_rankings['experience_percentile'],
                            'label': 'Experience Rank',
                            'format': 'percentile',
                            'benchmark': 50.0
                        },
                        'skill_count_rank': {
                            'value': user_rankings['skill_count_percentile'],
                            'label': 'Skill Count Rank',
                            'format': 'percentile',
                            'benchmark': 50.0
                        },
                        'salary_estimate': {
                            'value': user_rankings['estimated_salary'],
                            'label': 'Estimated Salary',
                            'format': 'currency',
                            'benchmark': peer_stats['median_salary']
                        }
                    }
                },
                'market_statistics': {
                    'title': '📊 Peer Market Statistics',
                    'peer_averages': peer_stats,
                    'your_stats': {
                        'experience': user_rankings['experience_years'],
                        'skill_count': user_rankings['skill_count'],
                        'estimated_salary': user_rankings['estimated_salary']
                    }
                },
                'skills_analysis': {
                    'title': '🎯 Skills Analysis',
                    'missing_core_skills': skills_analysis['missing_skills']['core'],
                    'missing_emerging_skills': skills_analysis['missing_skills']['emerging'],
                    'common_skills_you_have': [
                        skill for skill, _ in skills_analysis['most_common_skills'][:10]
                        if skill in [s.lower() for s in user_skills]
                    ],
                    'skill_coverage_details': {
                        'skills_in_common': skills_analysis['skills_in_common'],
                        'total_market_skills': skills_analysis['total_market_skills'],
                        'coverage_percentage': user_rankings['skill_coverage_percentage']
                    }
                },
                'peer_profiles': {
                    'title': '👥 Sample Peer Profiles',
                    'profiles': [
                        {
                            'experience_years': peer['experience_years'],
                            'education': peer['education'],
                            'salary': peer['salary'],
                            'skill_count': peer['skill_count'],
                            'top_skills': peer['skills'][:6],
                            'skill_overlap_percentage': skills_analysis['skill_overlaps'][i]['overlap_percentage']
                        }
                        for i, peer in enumerate(sample_peers)
                    ]
                },
                'recommendations': {
                    'title': '💡 Personalized Recommendations',
                    'priority_actions': self._generate_recommendations(
                        user_rankings, skills_analysis, career
                    )
                }
            }
        }
    
    def _generate_recommendations(self, user_rankings: Dict, skills_analysis: Dict, 
                                career: str) -> List[Dict[str, str]]:
        """Generate personalized recommendations based on analysis"""
        recommendations = []
        
        # Skill coverage recommendations
        coverage = user_rankings['skill_coverage_percentage']
        if coverage < 50:
            recommendations.append({
                'priority': 'critical',
                'icon': '🚨',
                'title': 'Critical Skill Gap',
                'action': f"Your skill coverage is {coverage:.1f}%. Focus on core skills immediately.",
                'next_steps': 'Learn 3-4 core missing skills within the next 3 months.'
            })
        elif coverage < 70:
            recommendations.append({
                'priority': 'high',
                'icon': '📈',
                'title': 'Skill Development Needed',
                'action': f"Your skill coverage is {coverage:.1f}%. You're on track but need more skills.",
                'next_steps': 'Focus on 2-3 missing core skills and 1-2 emerging skills.'
            })
        else:
            recommendations.append({
                'priority': 'medium',
                'icon': '🎯',
                'title': 'Strong Foundation',
                'action': f"Excellent! {coverage:.1f}% skill coverage puts you ahead of most peers.",
                'next_steps': 'Focus on emerging skills and specialization areas.'
            })
        
        # Experience-based recommendations
        exp_percentile = user_rankings['experience_percentile']
        if exp_percentile > 75:
            recommendations.append({
                'priority': 'medium',
                'icon': '🏆',
                'title': 'Senior Level Position',
                'action': 'Your experience level is in the top 25%. Consider leadership roles.',
                'next_steps': 'Develop management skills and mentor junior professionals.'
            })
        elif exp_percentile < 25:
            recommendations.append({
                'priority': 'high',
                'icon': '🌱',
                'title': 'Build Experience',
                'action': 'Focus on gaining practical experience through projects.',
                'next_steps': 'Complete 2-3 portfolio projects and seek internships or entry-level roles.'
            })
        
        # Missing skills recommendations
        if skills_analysis['missing_skills']['core']:
            core_skills = ', '.join(skills_analysis['missing_skills']['core'][:3])
            recommendations.append({
                'priority': 'high',
                'icon': '🔴',
                'title': 'Core Skills Missing',
                'action': f"Most {career}s know: {core_skills}",
                'next_steps': 'Prioritize learning these skills to be competitive.'
            })
        
        return recommendations
    
    def _estimate_experience_from_skills(self, user_skills: List[str], career: str) -> int:
        """Estimate user experience based on skill complexity"""
        career_profile = self.career_profiles[career]
        user_skill_set = set([s.lower() for s in user_skills])
        
        # Base experience
        base_exp = 1
        
        # Add experience for core skills
        core_skills_count = len([s for s in career_profile['core_skills'] 
                               if s.lower() in user_skill_set])
        base_exp += core_skills_count * 0.5
        
        # Add experience for emerging skills (indicates seniority)
        emerging_skills_count = len([s for s in career_profile['emerging_skills'] 
                                   if s.lower() in user_skill_set])
        base_exp += emerging_skills_count * 1.0
        
        return min(int(base_exp), 12)  # Cap at 12 years
    
    def _estimate_salary(self, experience: int, career: str, skill_count: int) -> int:
        """Estimate salary based on experience, career, and skills"""
        base_salary = self.career_profiles[career]['base_salary']
        
        # Experience multiplier
        salary = base_salary + (experience * 6000)
        
        # Skill count bonus
        if skill_count > 8:
            salary += 10000
        elif skill_count > 12:
            salary += 20000
        
        return max(salary, 45000)  # Minimum salary floor
    
    def _calculate_percentile(self, value: float, data_list: List[float]) -> int:
        """Calculate percentile rank of value in data list"""
        if not data_list:
            return 50
        
        sorted_data = sorted(data_list)
        position = sum(1 for x in sorted_data if x <= value)
        percentile = (position / len(sorted_data)) * 100
        return int(percentile)
