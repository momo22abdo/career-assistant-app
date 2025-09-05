#!/usr/bin/env python3
"""Debug script for gap analysis"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_pipeline_simple import CareerRecommendationPipeline

def main():
    print("🔍 Debugging Gap Analysis...")
    
    pipeline = CareerRecommendationPipeline()
    
    # Check Data Scientist skills
    career_skills = pipeline.career_skills_df[pipeline.career_skills_df['career'] == 'Data Scientist']
    print(f"Data Scientist skills: {career_skills['skill'].tolist()}")
    
    # Check our skill mapping
    user_skills = ["Python", "SQL"]
    skill_mapping = {}
    for skill_name in user_skills:
        synonyms = pipeline._get_skill_synonyms(skill_name)
        for synonym in synonyms:
            skill_mapping[synonym.lower()] = skill_name
    
    print(f"Skill mapping keys: {list(skill_mapping.keys())}")
    
    # Check exact matches
    for skill in career_skills['skill']:
        if skill.lower() in skill_mapping:
            print(f"MATCH: '{skill}' found in skill mapping")
        else:
            print(f"NO MATCH: '{skill}' not in skill mapping")

if __name__ == "__main__":
    main()
