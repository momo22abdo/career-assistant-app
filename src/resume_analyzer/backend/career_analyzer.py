import json
from typing import Dict, List, Tuple
import logging

class CareerAnalyzer:
    """Analyze career fit based on extracted skills"""
    
    def __init__(self, careers_path: str = "data/careers.json"):
        """
        Initialize career analyzer with career definitions
        
        Args:
            careers_path: Path to careers JSON file
        """
        self.logger = logging.getLogger(__name__)
        self.careers = self._load_careers(careers_path)
    
    def _load_careers(self, careers_path: str) -> Dict:
        """Load career definitions from JSON file"""
        try:
            with open(careers_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('careers', {})
        except Exception as e:
            self.logger.error(f"Error loading careers: {str(e)}")
            return {}
    
    def analyze_career_fit(self, extracted_skills: Dict[str, List[str]], top_n: int = 5) -> List[Dict]:
        """
        Analyze career fit for extracted skills
        
        Args:
            extracted_skills: Dictionary with technical and soft skills
            top_n: Number of top career matches to return
            
        Returns:
            List of career matches with scores and analysis
        """
        all_skills = extracted_skills.get('all_skills', [])
        technical_skills = extracted_skills.get('technical_skills', [])
        soft_skills = extracted_skills.get('soft_skills', [])
        
        career_matches = []
        
        for career_name, career_data in self.careers.items():
            analysis = self._analyze_single_career(
                career_name, 
                career_data, 
                all_skills, 
                technical_skills, 
                soft_skills
            )
            career_matches.append(analysis)
        
        # Sort by overall score (descending)
        career_matches.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return career_matches[:top_n]
    
    def _analyze_single_career(self, career_name: str, career_data: Dict, 
                             all_skills: List[str], technical_skills: List[str], 
                             soft_skills: List[str]) -> Dict:
        """Analyze fit for a single career"""
        
        required_skills = career_data.get('required_skills', {})
        optional_skills = career_data.get('optional_skills', {})
        
        # Calculate required skills coverage
        required_matches = []
        required_missing = []
        required_importance_sum = 0
        matched_required_importance = 0
        
        for skill, importance in required_skills.items():
            required_importance_sum += importance
            if skill in all_skills:
                required_matches.append({
                    'skill': skill,
                    'importance': importance,
                    'type': 'required'
                })
                matched_required_importance += importance
            else:
                required_missing.append({
                    'skill': skill,
                    'importance': importance,
                    'type': 'required'
                })
        
        # Calculate optional skills coverage
        optional_matches = []
        optional_missing = []
        optional_importance_sum = sum(optional_skills.values())
        matched_optional_importance = 0
        
        for skill, importance in optional_skills.items():
            if skill in all_skills:
                optional_matches.append({
                    'skill': skill,
                    'importance': importance,
                    'type': 'optional'
                })
                matched_optional_importance += importance
            else:
                optional_missing.append({
                    'skill': skill,
                    'importance': importance,
                    'type': 'optional'
                })
        
        # Calculate scores
        required_coverage = (matched_required_importance / required_importance_sum * 100) if required_importance_sum > 0 else 0
        optional_coverage = (matched_optional_importance / optional_importance_sum * 100) if optional_importance_sum > 0 else 0
        
        # Overall score (weighted: 70% required, 30% optional)
        overall_score = (required_coverage * 0.7) + (optional_coverage * 0.3)
        
        # Calculate skill gaps
        skill_gaps = self._calculate_skill_gaps(required_missing, optional_missing)
        
        return {
            'career': career_name,
            'description': career_data.get('description', ''),
            'overall_score': round(overall_score, 1),
            'required_coverage': round(required_coverage, 1),
            'optional_coverage': round(optional_coverage, 1),
            'required_matches': required_matches,
            'required_missing': required_missing,
            'optional_matches': optional_matches,
            'optional_missing': optional_missing,
            'skill_gaps': skill_gaps,
            'total_required': len(required_skills),
            'total_optional': len(optional_skills),
            'matched_required': len(required_matches),
            'matched_optional': len(optional_matches),
            'missing_required': len(required_missing),
            'missing_optional': len(optional_missing)
        }
    
    def _calculate_skill_gaps(self, required_missing: List[Dict], optional_missing: List[Dict]) -> Dict:
        """Calculate skill gaps and recommendations"""
        
        # Sort missing skills by importance
        all_missing = required_missing + optional_missing
        all_missing.sort(key=lambda x: x['importance'], reverse=True)
        
        # Group by type
        critical_gaps = [skill for skill in required_missing if skill['importance'] >= 8]
        important_gaps = [skill for skill in required_missing if 6 <= skill['importance'] < 8]
        nice_to_have = [skill for skill in optional_missing if skill['importance'] >= 6]
        
        return {
            'critical_gaps': critical_gaps,
            'important_gaps': important_gaps,
            'nice_to_have': nice_to_have,
            'total_gaps': len(all_missing),
            'critical_count': len(critical_gaps),
            'important_count': len(important_gaps),
            'nice_to_have_count': len(nice_to_have)
        }
    
    def get_career_recommendations(self, career_analysis: List[Dict]) -> Dict:
        """Generate career recommendations based on analysis"""
        
        if not career_analysis:
            return {}
        
        top_career = career_analysis[0]
        
        recommendations = {
            'best_fit': top_career['career'],
            'best_score': top_career['overall_score'],
            'recommendations': []
        }
        
        # Generate specific recommendations
        if top_career['overall_score'] >= 80:
            recommendations['recommendations'].append({
                'type': 'excellent_fit',
                'message': f"Excellent fit for {top_career['career']}! Your skills align very well with this role.",
                'priority': 'high'
            })
        elif top_career['overall_score'] >= 60:
            recommendations['recommendations'].append({
                'type': 'good_fit',
                'message': f"Good fit for {top_career['career']}. Focus on filling critical skill gaps.",
                'priority': 'medium'
            })
        else:
            recommendations['recommendations'].append({
                'type': 'needs_improvement',
                'message': f"Consider developing more skills for {top_career['career']} or explore related careers.",
                'priority': 'low'
            })
        
        # Add specific skill recommendations
        if top_career['skill_gaps']['critical_gaps']:
            critical_skills = [skill['skill'] for skill in top_career['skill_gaps']['critical_gaps'][:3]]
            recommendations['recommendations'].append({
                'type': 'critical_skills',
                'message': f"Critical skills to develop: {', '.join(critical_skills)}",
                'priority': 'high'
            })
        
        if top_career['skill_gaps']['important_gaps']:
            important_skills = [skill['skill'] for skill in top_career['skill_gaps']['important_gaps'][:3]]
            recommendations['recommendations'].append({
                'type': 'important_skills',
                'message': f"Important skills to consider: {', '.join(important_skills)}",
                'priority': 'medium'
            })
        
        return recommendations
    
    def get_career_comparison(self, career_analysis: List[Dict]) -> Dict:
        """Generate comparison between top career matches"""
        
        if len(career_analysis) < 2:
            return {}
        
        comparison = {
            'top_careers': [],
            'skill_overlap': {},
            'unique_skills': {}
        }
        
        for i, career in enumerate(career_analysis[:3]):
            comparison['top_careers'].append({
                'rank': i + 1,
                'career': career['career'],
                'score': career['overall_score'],
                'required_coverage': career['required_coverage'],
                'optional_coverage': career['optional_coverage']
            })
        
        # Compare skills between top careers
        if len(career_analysis) >= 2:
            career1_skills = set([skill['skill'] for skill in career_analysis[0]['required_matches']])
            career2_skills = set([skill['skill'] for skill in career_analysis[1]['required_matches']])
            
            comparison['skill_overlap'] = {
                'overlap_skills': list(career1_skills.intersection(career2_skills)),
                'career1_unique': list(career1_skills - career2_skills),
                'career2_unique': list(career2_skills - career1_skills)
            }
        
        return comparison

