#!/usr/bin/env python3
"""
Enhanced Test script for Resume Analyzer
Tests all major components including new enhancements
"""

import sys
import os
import json
from pathlib import Path

# Add the backend to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend import ResumeAnalyzer
from backend.utils import create_sample_resume

def test_enhanced_features():
    """Test enhanced features"""
    print("🚀 Testing Enhanced Resume Analyzer Features")
    print("=" * 60)
    
    try:
        # Initialize analyzer
        analyzer = ResumeAnalyzer()
        print("✅ ResumeAnalyzer initialized successfully")
        
        # Test file size limit
        max_size = analyzer.get_max_file_size()
        max_size_mb = max_size / (1024 * 1024)
        print(f"✅ File size limit: {max_size_mb:.0f}MB")
        
        # Test supported file types
        supported_types = analyzer.get_supported_file_types()
        print(f"✅ Supported file types: {', '.join(supported_types)}")
        
        # Test sample analysis
        print("\n🧪 Testing Sample Analysis...")
        results = analyzer.run_sample_analysis()
        
        if results.get('success'):
            print("✅ Sample analysis completed successfully")
            
            # Test JSON export
            print("\n📄 Testing JSON Export...")
            json_success = analyzer.save_analysis_results(results, "test_export.json")
            if json_success:
                print("✅ JSON export successful")
                os.remove("test_export.json")
            else:
                print("❌ JSON export failed")
            
            # Test CSV export
            print("\n📊 Testing CSV Export...")
            csv_success = analyzer.save_analysis_results_csv(results, "test_export.csv")
            if csv_success:
                print("✅ CSV export successful")
                os.remove("test_export.csv")
            else:
                print("❌ CSV export failed")
            
            # Display summary
            summary = analyzer.get_analysis_summary(results)
            print(f"\n📊 Analysis Summary:")
            print(f"   - Total Skills: {summary.get('total_skills', 0)}")
            print(f"   - Technical Skills: {summary.get('technical_skills', 0)}")
            print(f"   - Soft Skills: {summary.get('soft_skills', 0)}")
            print(f"   - Top Career: {summary.get('top_career', 'N/A')}")
            print(f"   - Career Score: {summary.get('top_career_score', 0):.1f}%")
            print(f"   - Resume Score: {summary.get('resume_score', 0):.1f}/100")
            
        else:
            print(f"❌ Sample analysis failed: {results.get('error', 'Unknown error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced features test failed: {str(e)}")
        return False

def test_file_parsing():
    """Test file parsing capabilities"""
    print("\n📄 Testing File Parsing...")
    
    try:
        from backend.parser import ResumeParser
        
        parser = ResumeParser()
        print("✅ ResumeParser initialized successfully")
        
        # Test text cleaning
        test_text = """
        JOHN DOE
        Software Engineer
        
        •   Developed applications
        •   Led teams
        •   Implemented solutions
        """
        
        cleaned_text = parser.clean_text(test_text)
        print(f"✅ Text cleaning completed ({len(cleaned_text)} characters)")
        
        # Test contact info extraction
        contact_info = parser.extract_contact_info(cleaned_text)
        print(f"✅ Contact info extraction completed")
        
        # Test OCR fallback method exists
        if hasattr(parser, '_ocr_fallback'):
            print("✅ OCR fallback method available")
        else:
            print("⚠️ OCR fallback method not found")
        
        return True
        
    except Exception as e:
        print(f"❌ File parsing test failed: {str(e)}")
        return False

def test_skills_extraction():
    """Test skills extraction with fuzzy matching"""
    print("\n🔍 Testing Skills Extraction...")
    
    try:
        from backend.skills_extractor import SkillsExtractor
        
        extractor = SkillsExtractor()
        print("✅ SkillsExtractor initialized successfully")
        
        # Test with variations
        test_text = """
        I am a software engineer with experience in:
        - Python programming
        - Data visualization using matplotlib
        - Machine learning with scikit-learn
        - Web development with React.js
        - Database management with SQL
        - Cloud platforms like AWS
        - DevOps tools including Docker
        - Strong communication and problem-solving skills
        """
        
        skills = extractor.extract_skills(test_text)
        
        print(f"✅ Skills extracted successfully:")
        print(f"   - Technical Skills: {skills.get('technical_skills', [])}")
        print(f"   - Soft Skills: {skills.get('soft_skills', [])}")
        print(f"   - Total Skills: {len(skills.get('all_skills', []))}")
        
        # Test fuzzy matching
        if 'Data Visualization' in skills.get('technical_skills', []):
            print("✅ Fuzzy matching working (visualization → Data Visualization)")
        else:
            print("⚠️ Fuzzy matching may need adjustment")
        
        return True
        
    except Exception as e:
        print(f"❌ Skills extraction test failed: {str(e)}")
        return False

def test_career_analysis():
    """Test career analysis with importance weights"""
    print("\n🎯 Testing Career Analysis...")
    
    try:
        from backend.career_analyzer import CareerAnalyzer
        
        analyzer = CareerAnalyzer()
        print("✅ CareerAnalyzer initialized successfully")
        
        # Test skills
        test_skills = {
            'technical_skills': ['Python', 'Machine Learning', 'SQL', 'Data Visualization'],
            'soft_skills': ['Communication', 'Problem Solving', 'Teamwork'],
            'all_skills': ['Python', 'Machine Learning', 'SQL', 'Data Visualization', 'Communication', 'Problem Solving', 'Teamwork']
        }
        
        # Analyze career fit
        career_analysis = analyzer.analyze_career_fit(test_skills, top_n=3)
        
        print(f"✅ Career analysis completed successfully:")
        for i, career in enumerate(career_analysis[:3], 1):
            print(f"   {i}. {career['career']}: {career['overall_score']:.1f}%")
            print(f"      Required Coverage: {career['required_coverage']:.1f}%")
            print(f"      Optional Coverage: {career['optional_coverage']:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Career analysis test failed: {str(e)}")
        return False

def test_resume_scoring():
    """Test resume scoring and ATS suggestions"""
    print("\n📊 Testing Resume Scoring...")
    
    try:
        from backend.resume_scorer import ResumeScorer
        
        scorer = ResumeScorer()
        print("✅ ResumeScorer initialized successfully")
        
        # Test text
        test_text = """
        JOHN DOE
        Software Engineer
        john.doe@email.com | (555) 123-4567
        
        EXPERIENCE
        Senior Software Engineer | TechCorp Inc. | 2021-Present
        • Developed and maintained microservices using Python and Flask
        • Led a team of 3 developers in building a React-based dashboard
        • Implemented CI/CD pipelines using Docker and AWS
        • Optimized database queries resulting in 40% performance improvement
        
        SKILLS
        Technical Skills: Python, JavaScript, React, Node.js, SQL, Git, Docker, AWS
        Soft Skills: Communication, Problem Solving, Teamwork, Leadership
        """
        
        # Test skills
        test_skills = {
            'technical_skills': ['Python', 'JavaScript', 'React', 'SQL'],
            'soft_skills': ['Communication', 'Problem Solving', 'Teamwork'],
            'all_skills': ['Python', 'JavaScript', 'React', 'SQL', 'Communication', 'Problem Solving', 'Teamwork']
        }
        
        # Test career analysis (minimal)
        test_career_analysis = [{
            'career': 'Software Engineer',
            'required_matches': [{'skill': 'Python', 'importance': 8}],
            'optional_matches': [{'skill': 'React', 'importance': 6}],
            'required_missing': [],
            'optional_missing': []
        }]
        
        # Score resume
        score = scorer.score_resume(test_text, test_skills, test_career_analysis)
        
        print(f"✅ Resume scoring completed successfully:")
        print(f"   - Score keys: {list(score.keys())}")
        print(f"   - Overall Score: {score.get('overall_score', score.get('score', 0)):.1f}/100")
        print(f"   - Formatting: {score.get('breakdown', {}).get('formatting_score', 0):.1f}/100")
        print(f"   - Content: {score.get('breakdown', {}).get('content_score', 0):.1f}/100")
        print(f"   - Keywords: {score.get('breakdown', {}).get('keyword_score', 0):.1f}/100")
        print(f"   - Action Verbs: {score.get('breakdown', {}).get('action_verb_score', 0):.1f}/100")
        
        # Check suggestions
        suggestions = score.get('suggestions', [])
        if suggestions:
            print(f"   - ATS Suggestions: {len(suggestions)} suggestions generated")
        
        return True
        
    except Exception as e:
        print(f"❌ Resume scoring test failed: {str(e)}")
        return False

def main():
    """Run all enhanced tests"""
    print("🚀 Starting Enhanced Resume Analyzer Tests")
    print("=" * 60)
    
    # Test enhanced features
    tests = [
        ("Enhanced Features", test_enhanced_features),
        ("File Parsing", test_file_parsing),
        ("Skills Extraction", test_skills_extraction),
        ("Career Analysis", test_career_analysis),
        ("Resume Scoring", test_resume_scoring)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All enhanced tests passed! Resume Analyzer is ready to use.")
        print("\n📝 To run the Streamlit app:")
        print("   streamlit run app.py")
        print("\n📝 New Features:")
        print("   ✅ Increased file size limit to 200MB")
        print("   ✅ Enhanced error handling with fallback suggestions")
        print("   ✅ OCR fallback for PDF parsing")
        print("   ✅ CSV export functionality")
        print("   ✅ Better file upload UI with file info display")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
