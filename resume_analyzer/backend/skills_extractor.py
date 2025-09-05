import json
import re
from typing import Dict, List, Tuple
from rapidfuzz import fuzz, process
import logging

class SkillsExtractor:
    """Extract and match skills from resume text"""
    
    def __init__(self, skills_vocab_path: str = "data/skills_vocab.json"):
        """
        Initialize skills extractor with vocabulary
        
        Args:
            skills_vocab_path: Path to skills vocabulary JSON file
        """
        self.logger = logging.getLogger(__name__)
        self.skills_vocab = self._load_skills_vocab(skills_vocab_path)
        self.skill_mapping = self._create_skill_mapping()
        
    def _load_skills_vocab(self, vocab_path: str) -> Dict:
        """Load skills vocabulary from JSON file"""
        try:
            with open(vocab_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading skills vocabulary: {str(e)}")
            return {}
    
    def _create_skill_mapping(self) -> Dict[str, str]:
        """
        Create a flat mapping of skill variations to canonical names
        
        Returns:
            Dictionary mapping skill variations to canonical names
        """
        skill_mapping = {}
        
        # Process technical skills
        for category, skills in self.skills_vocab.get('technical_skills', {}).items():
            for canonical_name, variations in skills.items():
                # Add canonical name
                skill_mapping[canonical_name.lower()] = canonical_name
                
                # Add variations
                for variation in variations:
                    skill_mapping[variation.lower()] = canonical_name
        
        # Process soft skills
        for category, variations in self.skills_vocab.get('soft_skills', {}).items():
            # Convert category name to canonical name
            canonical_name = category.replace('_', ' ').title()
            skill_mapping[canonical_name.lower()] = canonical_name
            
            # Add variations
            for variation in variations:
                skill_mapping[variation.lower()] = canonical_name
        
        return skill_mapping
    
    def extract_skills(self, text: str, confidence_threshold: float = 80.0) -> Dict[str, List[str]]:
        """
        Extract skills from resume text
        
        Args:
            text: Resume text
            confidence_threshold: Minimum confidence for fuzzy matching
            
        Returns:
            Dictionary with technical and soft skills
        """
        if not text:
            return {'technical_skills': [], 'soft_skills': []}
        
        # Normalize text
        text_lower = text.lower()
        
        # Extract skills using exact and fuzzy matching
        extracted_skills = self._extract_skills_exact(text_lower)
        fuzzy_skills = self._extract_skills_fuzzy(text_lower, confidence_threshold)
        
        # Combine and deduplicate
        all_skills = list(set(extracted_skills + fuzzy_skills))
        
        # Categorize skills
        technical_skills = []
        soft_skills = []
        
        for skill in all_skills:
            if self._is_technical_skill(skill):
                technical_skills.append(skill)
            else:
                soft_skills.append(skill)
        
        return {
            'technical_skills': sorted(technical_skills),
            'soft_skills': sorted(soft_skills),
            'all_skills': sorted(all_skills)
        }
    
    def _extract_skills_exact(self, text: str) -> List[str]:
        """Extract skills using exact matching"""
        found_skills = []
        
        for variation, canonical_name in self.skill_mapping.items():
            # Check for exact matches (word boundaries)
            pattern = r'\b' + re.escape(variation) + r'\b'
            if re.search(pattern, text):
                found_skills.append(canonical_name)
        
        return found_skills
    
    def _extract_skills_fuzzy(self, text: str, confidence_threshold: float) -> List[str]:
        """Extract skills using fuzzy matching"""
        found_skills = []
        
        # Split text into words and phrases
        words = re.findall(r'\b\w+(?:\s+\w+)*\b', text)
        
        for word in words:
            if len(word) < 3:  # Skip very short words
                continue
                
            # Find best match in skill mapping
            best_match = process.extractOne(
                word, 
                self.skill_mapping.keys(),
                scorer=fuzz.token_sort_ratio,
                score_cutoff=confidence_threshold
            )
            
            if best_match:
                canonical_name = self.skill_mapping[best_match[0]]
                if canonical_name not in found_skills:
                    found_skills.append(canonical_name)
        
        return found_skills
    
    def _is_technical_skill(self, skill: str) -> bool:
        """Check if a skill is technical or soft"""
        skill_lower = skill.lower()
        
        # Check if skill exists in technical skills
        for category, skills in self.skills_vocab.get('technical_skills', {}).items():
            if skill_lower in [s.lower() for s in skills.keys()]:
                return True
        
        return False
    
    def get_skill_category(self, skill: str) -> str:
        """Get the category of a skill"""
        skill_lower = skill.lower()
        
        # Check technical skills
        for category, skills in self.skills_vocab.get('technical_skills', {}).items():
            if skill_lower in [s.lower() for s in skills.keys()]:
                return category
        
        # Check soft skills
        for category in self.skills_vocab.get('soft_skills', {}).keys():
            if skill_lower == category.replace('_', ' ').lower():
                return 'soft_skills'
        
        return 'unknown'
    
    def get_skill_synonyms(self, skill: str) -> List[str]:
        """Get synonyms for a given skill"""
        skill_lower = skill.lower()
        
        # Check technical skills
        for category, skills in self.skills_vocab.get('technical_skills', {}).items():
            for canonical_name, variations in skills.items():
                if canonical_name.lower() == skill_lower:
                    return variations
        
        # Check soft skills
        for category, variations in self.skills_vocab.get('soft_skills', {}).items():
            canonical_name = category.replace('_', ' ').title()
            if canonical_name.lower() == skill_lower:
                return variations
        
        return []
    
    def normalize_skill_name(self, skill: str) -> str:
        """Normalize skill name to canonical form"""
        skill_lower = skill.lower()
        return self.skill_mapping.get(skill_lower, skill)
    
    def get_skills_summary(self, extracted_skills: Dict[str, List[str]]) -> Dict:
        """Generate summary statistics for extracted skills"""
        technical_count = len(extracted_skills.get('technical_skills', []))
        soft_count = len(extracted_skills.get('soft_skills', []))
        total_count = len(extracted_skills.get('all_skills', []))
        
        # Get skill categories
        technical_categories = {}
        for skill in extracted_skills.get('technical_skills', []):
            category = self.get_skill_category(skill)
            technical_categories[category] = technical_categories.get(category, 0) + 1
        
        return {
            'total_skills': total_count,
            'technical_skills_count': technical_count,
            'soft_skills_count': soft_count,
            'technical_categories': technical_categories,
            'skills_ratio': {
                'technical': technical_count / total_count if total_count > 0 else 0,
                'soft': soft_count / total_count if total_count > 0 else 0
            }
        }

