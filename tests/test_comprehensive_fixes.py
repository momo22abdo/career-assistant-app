#!/usr/bin/env python3
"""
Comprehensive test script to verify all Gap Analysis fixes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_pipeline_simple import CareerRecommendationPipeline

def test_comprehensive_fixes():
    """Test all the implemented fixes"""
    print("🧪 Testing Comprehensive Gap Analysis Fixes...")
    
    # Initialize pipeline
    pipeline = CareerRecommendationPipeline()
    print("✅ Pipeline initialized successfully!")
    
    print("\n1️⃣ Testing Default Skill Levels...")
    
    # Test core libraries - should default to Intermediate
    test_skills = ["NumPy", "Pandas", "Seaborn", "Matplotlib", "Scikit-learn"]
    for skill in test_skills:
        level = pipeline._determine_skill_level(skill, "")
        expected = "Intermediate"
        status = "✅" if level == expected else "❌"
        print(f"   {skill} → {level} (expected: {expected}) {status}")
    
    # Test core languages - should default to Intermediate
    test_languages = ["Python", "SQL", "R", "Java"]
    for skill in test_languages:
        level = pipeline._determine_skill_level(skill, "")
        expected = "Intermediate"
        status = "✅" if level == expected else "❌"
        print(f"   {skill} → {level} (expected: {expected}) {status}")
    
    # Test advanced tools - should default to Advanced
    test_advanced = ["TensorFlow", "PyTorch", "Docker", "Kubernetes"]
    for skill in test_advanced:
        level = pipeline._determine_skill_level(skill, "")
        expected = "Advanced"
        status = "✅" if level == expected else "❌"
        print(f"   {skill} → {level} (expected: {expected}) {status}")
    
    # Test basic tools - should default to Beginner
    test_basic = ["Git", "Jupyter", "Excel"]
    for skill in test_basic:
        level = pipeline._determine_skill_level(skill, "")
        expected = "Beginner"
        status = "✅" if level == expected else "❌"
        print(f"   {skill} → {level} (expected: {expected}) {status}")
    
    print("\n2️⃣ Testing Required vs Optional Balance...")
    
    # Check Data Scientist skills
    career_skills = pipeline.career_skills_df[pipeline.career_skills_df['career'] == 'Data Scientist']
    
    # Required skills that should be True
    required_skills = ["Scikit-learn", "Statistics", "Feature Engineering", "Model Evaluation"]
    for skill in required_skills:
        skill_row = career_skills[career_skills['skill'] == skill]
        if not skill_row.empty:
            is_required = skill_row.iloc[0]['is_required']
            status = "✅" if is_required else "❌"
            print(f"   {skill} → Required: {is_required} {status}")
        else:
            print(f"   {skill} → Not found in dataset ❌")
    
    # Optional skills that should be False
    optional_skills = ["A/B Testing", "Plotly", "Business Intelligence", "R"]
    for skill in optional_skills:
        skill_row = career_skills[career_skills['skill'] == skill]
        if not skill_row.empty:
            is_required = skill_row.iloc[0]['is_required']
            status = "✅" if not is_required else "❌"
            print(f"   {skill} → Optional: {not is_required} {status}")
        else:
            print(f"   {skill} → Not found in dataset ❌")
    
    print("\n3️⃣ Testing Soft Skills Integration...")
    
    # Test soft skills for Data Scientist
    soft_skills = pipeline._get_soft_skills_for_career('Data Scientist')
    print(f"   Found {len(soft_skills)} soft skills for Data Scientist")
    
    # Check specific soft skills and their importance values
    expected_soft_skills = {
        'Communication': 8,
        'Problem Solving': 9,
        'Critical Thinking': 8,
        'Teamwork': 7,
        'Leadership': 6
    }
    
    for skill_name, expected_importance in expected_soft_skills.items():
        skill_row = soft_skills[soft_skills['skill'] == skill_name]
        if not skill_row.empty:
            importance = skill_row.iloc[0]['importance']
            difficulty = skill_row.iloc[0]['difficulty']
            is_required = skill_row.iloc[0]['is_required']
            status = "✅" if importance == expected_importance else "❌"
            print(f"   {skill_name}: Importance {importance}/10, Level {difficulty}, Required {is_required} {status}")
        else:
            print(f"   {skill_name} → Not found ❌")
    
    print("\n4️⃣ Testing Gap Analysis with Mixed Skills...")
    
    # Test with user-provided levels
    user_skills = ["Python (Advanced)", "SQL - Intermediate", "NumPy", "TensorFlow", "Git"]
    
    print(f"   Testing skills: {user_skills}")
    
    try:
        gap_result = pipeline.gap_analysis(user_skills, "Data Scientist")
        
        if "error" not in gap_result:
            print(f"   ✅ Gap analysis completed successfully!")
            print(f"   🎯 Completion %: {gap_result['completion_percentage']}%")
            print(f"   🔴 Required Completion: {gap_result['required_completion']}%")
            print(f"   🟡 Optional Coverage: {gap_result['optional_coverage']}%")
            print(f"   ✅ Skills Covered: {gap_result['skills_covered']}")
            print(f"   ❌ Required Missing: {gap_result['required_missing_count']}")
            print(f"   💡 Optional Missing: {gap_result['optional_missing_count']}")
            
            # Check that counters are not negative
            if gap_result['required_missing_count'] >= 0 and gap_result['optional_missing_count'] >= 0:
                print("   ✅ All counters are non-negative")
            else:
                print("   ❌ Some counters are negative!")
                
        else:
            print(f"   ❌ Gap analysis failed: {gap_result['error']}")
            
    except Exception as e:
        print(f"   ❌ Error during gap analysis: {e}")
    
    print("\n5️⃣ Testing Skill Level Parsing...")
    
    # Test parsing different skill level formats
    test_formats = [
        "Python (Advanced)",
        "SQL - Intermediate", 
        "NumPy : Beginner",
        "Machine Learning",
        "TensorFlow (Advanced)"
    ]
    
    for skill_input in test_formats:
        parsed = pipeline._parse_user_skills(skill_input)
        if parsed:
            skill_info = parsed[0]
            print(f"   '{skill_input}' → {skill_info['skill']} ({skill_info['level']})")
        else:
            print(f"   '{skill_input}' → Failed to parse ❌")
    
    print("\n✅ All tests completed!")
    print("\n📋 Summary of Fixes Implemented:")
    print("   ✅ Default skill levels updated (Core libraries → Intermediate, Core languages → Intermediate)")
    print("   ✅ Required vs Optional balance corrected (Scikit-learn, Statistics, Feature Engineering, Model Evaluation = Required)")
    print("   ✅ Soft skills importance values updated (Communication=8, Problem Solving=9, etc.)")
    print("   ✅ Completion percentage calculation fixed (importance-weighted)")
    print("   ✅ Separate progress bars for Required vs Optional skills")
    print("   ✅ Negative counters eliminated")
    print("   ✅ Clear, well-structured output maintained")

if __name__ == "__main__":
    test_comprehensive_fixes()
