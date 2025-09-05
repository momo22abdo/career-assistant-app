import re
from typing import Dict, List, Tuple
import logging

class ResumeScorer:
    """Score resume and provide ATS optimization suggestions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Action verbs for resume optimization
        self.action_verbs = [
            'developed', 'implemented', 'designed', 'created', 'built', 'managed', 'led', 'coordinated',
            'analyzed', 'optimized', 'improved', 'increased', 'decreased', 'reduced', 'enhanced',
            'delivered', 'completed', 'achieved', 'accomplished', 'executed', 'launched', 'deployed',
            'maintained', 'supported', 'troubleshot', 'debugged', 'tested', 'validated', 'verified',
            'collaborated', 'communicated', 'presented', 'trained', 'mentored', 'coached', 'guided',
            'researched', 'investigated', 'evaluated', 'assessed', 'reviewed', 'monitored', 'tracked'
        ]
        
        # Common resume sections
        self.resume_sections = [
            'summary', 'objective', 'experience', 'work history', 'employment',
            'education', 'academic', 'skills', 'technical skills', 'competencies',
            'projects', 'achievements', 'certifications', 'awards', 'publications',
            'volunteer', 'activities', 'interests', 'languages'
        ]
    
    def score_resume(self, text: str, extracted_skills: Dict[str, List[str]], 
                    career_analysis: List[Dict]) -> Dict:
        """
        Score resume and provide ATS optimization suggestions
        
        Args:
            text: Resume text
            extracted_skills: Extracted skills
            career_analysis: Career fit analysis
            
        Returns:
            Dictionary with score and suggestions
        """
        if not text:
            return {'score': 0, 'suggestions': [], 'error': 'Empty resume text'}
        
        # Calculate individual scores
        formatting_score = self._calculate_formatting_score(text)
        content_score = self._calculate_content_score(text, extracted_skills)
        keyword_score = self._calculate_keyword_score(text, career_analysis)
        action_verb_score = self._calculate_action_verb_score(text)
        
        # Weighted overall score
        overall_score = (
            formatting_score * 0.25 +
            content_score * 0.35 +
            keyword_score * 0.25 +
            action_verb_score * 0.15
        )
        
        # Generate suggestions
        suggestions = self._generate_suggestions(
            text, extracted_skills, career_analysis, 
            formatting_score, content_score, keyword_score, action_verb_score
        )
        
        return {
            'overall_score': round(overall_score, 1),
            'breakdown': {
                'formatting_score': round(formatting_score, 1),
                'content_score': round(content_score, 1),
                'keyword_score': round(keyword_score, 1),
                'action_verb_score': round(action_verb_score, 1)
            },
            'suggestions': suggestions,
            'strengths': self._identify_strengths(text, extracted_skills, career_analysis),
            'areas_for_improvement': self._identify_improvement_areas(
                text, extracted_skills, career_analysis
            )
        }
    
    def _calculate_formatting_score(self, text: str) -> float:
        """Calculate formatting score based on resume structure"""
        score = 0
        max_score = 100
        
        # Check for proper sections
        section_count = 0
        for section in self.resume_sections:
            if re.search(rf'\b{section}\b', text, re.IGNORECASE):
                section_count += 1
        
        # Section score (max 40 points)
        section_score = min(40, (section_count / 5) * 40)
        score += section_score
        
        # Check for bullet points
        bullet_points = len(re.findall(r'[•·▪▫‣⁃\-*]\s', text))
        bullet_score = min(20, (bullet_points / 10) * 20)
        score += bullet_score
        
        # Check for proper spacing and structure
        lines = text.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        if len(non_empty_lines) >= 20:  # Minimum content length
            score += 20
        elif len(non_empty_lines) >= 10:
            score += 10
        
        # Check for consistent formatting
        if len(set(len(line) for line in non_empty_lines)) > 1:  # Varied line lengths
            score += 20
        
        return min(score, max_score)
    
    def _calculate_content_score(self, text: str, extracted_skills: Dict[str, List[str]]) -> float:
        """Calculate content score based on skills and content quality"""
        score = 0
        max_score = 100
        
        # Skills diversity score
        total_skills = len(extracted_skills.get('all_skills', []))
        technical_skills = len(extracted_skills.get('technical_skills', []))
        soft_skills = len(extracted_skills.get('soft_skills', []))
        
        if total_skills >= 10:
            score += 30
        elif total_skills >= 5:
            score += 20
        elif total_skills >= 3:
            score += 10
        
        # Balance between technical and soft skills
        if technical_skills > 0 and soft_skills > 0:
            score += 20
        elif technical_skills > 0 or soft_skills > 0:
            score += 10
        
        # Content length and quality
        word_count = len(text.split())
        if word_count >= 300:
            score += 25
        elif word_count >= 200:
            score += 15
        elif word_count >= 100:
            score += 10
        
        # Check for specific content indicators
        content_indicators = [
            'experience', 'project', 'achievement', 'result', 'impact',
            'responsibility', 'duty', 'task', 'goal', 'objective'
        ]
        
        indicator_count = sum(1 for indicator in content_indicators 
                            if re.search(rf'\b{indicator}\b', text, re.IGNORECASE))
        score += min(25, indicator_count * 5)
        
        return min(score, max_score)
    
    def _calculate_keyword_score(self, text: str, career_analysis: List[Dict]) -> float:
        """Calculate keyword optimization score"""
        if not career_analysis:
            return 0
        
        score = 0
        max_score = 100
        
        # Get keywords from top career match
        top_career = career_analysis[0]
        required_skills = [skill['skill'] for skill in top_career.get('required_matches', [])]
        optional_skills = [skill['skill'] for skill in top_career.get('optional_matches', [])]
        
        all_keywords = required_skills + optional_skills
        text_lower = text.lower()
        
        # Calculate keyword density
        keyword_matches = 0
        for keyword in all_keywords:
            if keyword.lower() in text_lower:
                keyword_matches += 1
        
        if all_keywords:
            keyword_density = keyword_matches / len(all_keywords)
            score = keyword_density * 100
        
        return min(score, max_score)
    
    def _calculate_action_verb_score(self, text: str) -> float:
        """Calculate action verb usage score"""
        score = 0
        max_score = 100
        
        text_lower = text.lower()
        action_verb_count = 0
        
        for verb in self.action_verbs:
            if re.search(rf'\b{verb}\b', text_lower):
                action_verb_count += 1
        
        # Score based on action verb count
        if action_verb_count >= 8:
            score = 100
        elif action_verb_count >= 6:
            score = 80
        elif action_verb_count >= 4:
            score = 60
        elif action_verb_count >= 2:
            score = 40
        elif action_verb_count >= 1:
            score = 20
        
        return score
    
    def _generate_suggestions(self, text: str, extracted_skills: Dict[str, List[str]], 
                             career_analysis: List[Dict], formatting_score: float, 
                             content_score: float, keyword_score: float, 
                             action_verb_score: float) -> List[Dict]:
        """Generate specific suggestions for improvement"""
        suggestions = []
        
        # Formatting suggestions
        if formatting_score < 70:
            suggestions.append({
                'category': 'formatting',
                'priority': 'high',
                'suggestion': 'Improve resume structure with clear sections and bullet points',
                'details': 'Add sections like Summary, Experience, Skills, Education, and Projects'
            })
        
        # Content suggestions
        if content_score < 70:
            suggestions.append({
                'category': 'content',
                'priority': 'high',
                'suggestion': 'Add more specific achievements and quantifiable results',
                'details': 'Include metrics, percentages, and specific outcomes from your work'
            })
        
        # Keyword suggestions
        if keyword_score < 60 and career_analysis:
            top_career = career_analysis[0]
            missing_keywords = [skill['skill'] for skill in top_career.get('required_missing', [])[:5]]
            if missing_keywords:
                suggestions.append({
                    'category': 'keywords',
                    'priority': 'medium',
                    'suggestion': f"Incorporate missing keywords: {', '.join(missing_keywords)}",
                    'details': 'Add these skills naturally throughout your resume'
                })
        
        # Action verb suggestions
        if action_verb_score < 60:
            suggestions.append({
                'category': 'action_verbs',
                'priority': 'medium',
                'suggestion': 'Use more action verbs to start bullet points',
                'details': 'Examples: Developed, Implemented, Designed, Managed, Led, Analyzed'
            })
        
        # Skills balance suggestions
        technical_skills = len(extracted_skills.get('technical_skills', []))
        soft_skills = len(extracted_skills.get('soft_skills', []))
        
        if technical_skills == 0:
            suggestions.append({
                'category': 'skills',
                'priority': 'high',
                'suggestion': 'Add technical skills relevant to your target role',
                'details': 'Include programming languages, tools, and technologies'
            })
        
        if soft_skills == 0:
            suggestions.append({
                'category': 'skills',
                'priority': 'medium',
                'suggestion': 'Include soft skills like communication and teamwork',
                'details': 'Add skills like Leadership, Problem Solving, Communication'
            })
        
        return suggestions
    
    def _identify_strengths(self, text: str, extracted_skills: Dict[str, List[str]], 
                          career_analysis: List[Dict]) -> List[str]:
        """Identify resume strengths"""
        strengths = []
        
        # Skills strengths
        total_skills = len(extracted_skills.get('all_skills', []))
        if total_skills >= 8:
            strengths.append(f"Strong skill diversity ({total_skills} skills identified)")
        
        technical_skills = len(extracted_skills.get('technical_skills', []))
        soft_skills = len(extracted_skills.get('soft_skills', []))
        
        if technical_skills >= 5:
            strengths.append(f"Strong technical background ({technical_skills} technical skills)")
        
        if soft_skills >= 3:
            strengths.append(f"Good soft skills coverage ({soft_skills} soft skills)")
        
        # Career fit strengths
        if career_analysis and career_analysis[0].get('overall_score', 0) >= 80:
            strengths.append(f"Excellent fit for {career_analysis[0]['career']}")
        elif career_analysis and career_analysis[0].get('overall_score', 0) >= 60:
            strengths.append(f"Good potential for {career_analysis[0]['career']}")
        
        # Content strengths
        word_count = len(text.split())
        if word_count >= 300:
            strengths.append("Comprehensive content coverage")
        
        return strengths
    
    def _identify_improvement_areas(self, text: str, extracted_skills: Dict[str, List[str]], 
                                  career_analysis: List[Dict]) -> List[str]:
        """Identify areas for improvement"""
        areas = []
        
        # Skills gaps
        if career_analysis:
            top_career = career_analysis[0]
            critical_gaps = top_career.get('skill_gaps', {}).get('critical_gaps', [])
            if critical_gaps:
                areas.append(f"Critical skill gaps for {top_career['career']}")
        
        # Content areas
        word_count = len(text.split())
        if word_count < 200:
            areas.append("Resume content could be more detailed")
        
        # Formatting areas
        bullet_points = len(re.findall(r'[•·▪▫‣⁃\-*]\s', text))
        if bullet_points < 5:
            areas.append("Add more bullet points for better readability")
        
        return areas
