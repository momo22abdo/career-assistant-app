#!/usr/bin/env python3
"""Simple test for gap analysis fixes"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_pipeline_simple import CareerRecommendationPipeline

def main():
    print("Testing Gap Analysis Fixes...")
    
    pipeline = CareerRecommendationPipeline()
    
    # Test 1: Skill level parsing
    print("\n1. Testing skill level parsing...")
    parsed = pipeline._parse_user_skills("Python (Advanced)\nSQL - Intermediate\nML : Beginner")
    for skill in parsed:
        print(f"   {skill['skill']} -> {skill['level']}")
    
    # Test 2: Synonym handling
    print("\n2. Testing synonym handling...")
    synonyms = pipeline._get_skill_synonyms("Visualization")
    print(f"   Visualization -> {synonyms}")
    
    # Test 3: Debug skill matching
    print("\n3. Debugging skill matching...")
    # Check what skills are in the Data Scientist dataset
    career_skills = pipeline.career_skills_df[pipeline.career_skills_df['career'] == 'Data Scientist']
    print(f"   Data Scientist skills: {career_skills['skill'].tolist()[:5]}...")
    
    # Check what our expanded skill set contains
    parsed_skills = [{'skill': skill, 'level': pipeline._determine_skill_level(skill, "")} for skill in ["Python", "SQL"]]
    skill_mapping = {}
    for skill_info in parsed_skills:
        skill_name = skill_info['skill']
        synonyms = pipeline._get_skill_synonyms(skill_name)
        for synonym in synonyms:
            skill_mapping[synonym.lower()] = skill_info
    
    print(f"   Our skill mapping keys: {list(skill_mapping.keys())[:10]}...")
    
    # Test 4: Gap analysis with levels
    print("\n4. Testing gap analysis with levels...")
    result = pipeline.gap_analysis(["Python (Advanced)", "SQL - Intermediate"], "Data Scientist")
    if "error" not in result:
        print(f"   Skills covered: {result['skills_covered']}")
        print(f"   Completion: {result['completion_percentage']}%")
        print("   Skills you have:")
        for skill in result['user_has']:
            print(f"   {skill['skill']} -> {skill['difficulty']}")
    
    print("\nTests completed!")

if __name__ == "__main__":
    main()
