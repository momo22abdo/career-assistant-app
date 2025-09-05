#!/usr/bin/env python3
"""
Simple test script to verify the AI Career Assistant works correctly
"""

import streamlit as st
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_pipeline_simple import CareerRecommendationPipeline

def test_gap_analysis():
    """Test the improved gap analysis functionality"""
    print("🧪 Testing Improved Gap Analysis...")
    
    # Initialize pipeline
    pipeline = CareerRecommendationPipeline()
    
    # Test case 1: Basic skills without levels
    print("\n📋 Test 1: Basic skills without levels")
    user_skills = ["Python", "SQL", "Machine Learning"]
    result = pipeline.gap_analysis(user_skills, "Data Scientist")
    
    if "error" not in result:
        print(f"✅ Completion: {result['completion_percentage']}%")
        print(f"✅ Skills covered: {result['skills_covered']}")
        print(f"✅ Required missing: {len(result['required_missing'])}")
        print(f"✅ Optional missing: {len(result['optional_missing'])}")
        print(f"✅ Total required importance: {result['total_required_importance']}")
        print(f"✅ User required importance: {result['user_required_importance']}")
        
        # Check if soft skills are included
        soft_skills_in_required = [s for s in result['required_missing'] if s.get('category') == 'soft']
        print(f"✅ Soft skills in required: {len(soft_skills_in_required)}")
        
        # Check skill levels
        user_skills_with_levels = [s for s in result['user_has']]
        print(f"✅ User skills with levels: {[(s['skill'], s['difficulty']) for s in user_skills_with_levels]}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Test case 2: Skills with explicit levels
    print("\n📋 Test 2: Skills with explicit levels")
    user_skills_with_levels = ["Python (Advanced)", "SQL - Intermediate", "Communication"]
    result2 = pipeline.gap_analysis(user_skills_with_levels, "Data Scientist")
    
    if "error" not in result2:
        print(f"✅ Completion: {result2['completion_percentage']}%")
        print(f"✅ Skills covered: {result2['skills_covered']}")
        
        # Check if user levels are respected
        for skill in result2['user_has']:
            print(f"✅ Skill: {skill['skill']} → Level: {skill['difficulty']}")
    else:
        print(f"❌ Error: {result2['error']}")
    
    # Test case 3: Skills with synonyms
    print("\n📋 Test 3: Skills with synonyms")
    user_skills_synonyms = ["Visualization", "Numpy", "ML"]
    result3 = pipeline.gap_analysis(user_skills_synonyms, "Data Scientist")
    
    if "error" not in result3:
        print(f"✅ Completion: {result3['completion_percentage']}%")
        print(f"✅ Skills covered: {result3['skills_covered']}")
        print(f"✅ Skills found: {[s['skill'] for s in result3['user_has']]}")
    else:
        print(f"❌ Error: {result3['error']}")
    
    # Test case 4: Check counters are not negative
    print("\n📋 Test 4: Check counters are not negative")
    if "error" not in result:
        required_missing_count = result.get('required_missing_count', len(result['required_missing']))
        optional_missing_count = result.get('optional_missing_count', len(result['optional_missing']))
        
        print(f"✅ Required missing count: {required_missing_count} (should be >= 0)")
        print(f"✅ Optional missing count: {optional_missing_count} (should be >= 0)")
        
        if required_missing_count >= 0 and optional_missing_count >= 0:
            print("✅ Counters are not negative!")
        else:
            print("❌ Counters are negative!")
    
    print("\n🎉 Gap Analysis Testing Complete!")

if __name__ == "__main__":
    test_gap_analysis()
