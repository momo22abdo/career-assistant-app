#!/usr/bin/env python3
"""Final comprehensive test for gap analysis fixes"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_pipeline_simple import CareerRecommendationPipeline

def main():
    print("🧪 Final Comprehensive Test for Gap Analysis Fixes...")
    
    pipeline = CareerRecommendationPipeline()
    
    # Test 1: Skill level parsing and defaults
    print("\n1️⃣ Testing skill level parsing and defaults...")
    test_skills = ["Python (Advanced)", "SQL - Intermediate", "NumPy", "TensorFlow", "Git"]
    
    for skill in test_skills:
        if "(" in skill or "-" in skill or ":" in skill:
            parsed = pipeline._parse_user_skills(skill)
            print(f"   {skill} → {parsed[0]['skill']} ({parsed[0]['level']})")
        else:
            level = pipeline._determine_skill_level(skill, "")
            print(f"   {skill} → {level} (default)")
    
    # Test 2: Gap analysis with mixed skills
    print("\n2️⃣ Testing gap analysis with mixed skills...")
    user_skills = ["Python (Advanced)", "SQL - Intermediate", "Communication", "Problem Solving"]
    target_career = "Data Scientist"
    
    result = pipeline.gap_analysis(user_skills, target_career)
    
    if "error" not in result:
        print(f"   ✅ Success!")
        print(f"   Main Completion: {result['completion_percentage']}%")
        print(f"   Required Completion: {result.get('required_completion', 'N/A')}%")
        print(f"   Optional Coverage: {result.get('optional_coverage', 'N/A')}%")
        print(f"   Skills covered: {result['skills_covered']}")
        print(f"   Required missing: {result['required_missing_count']}")
        print(f"   Optional missing: {result['optional_missing_count']}")
        
        # Check skill categories
        technical_skills = [s for s in result['user_has'] if s.get('category', 'technical') != 'soft']
        soft_skills = [s for s in result['user_has'] if s.get('category') == 'soft']
        
        print(f"   Technical skills: {len(technical_skills)}")
        print(f"   Soft skills: {len(soft_skills)}")
        
        # Verify no negative counters
        if result['required_missing_count'] >= 0 and result['optional_missing_count'] >= 0:
            print("   ✅ No negative counters found")
        else:
            print("   ❌ Negative counters found!")
        
    else:
        print(f"   ❌ Error: {result['error']}")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()
