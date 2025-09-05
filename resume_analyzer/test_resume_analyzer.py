#!/usr/bin/env python3
"""
Test script for Resume Analyzer
Tests all major components and provides example usage
"""

import sys
import os
import json
from pathlib import Path

# Add the backend to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend import ResumeAnalyzer
from backend.utils import create_sample_resume

def test_backend_components():
    """Test individual backend components"""
    print("🔧 Testing Backend Components...")
    
    try:
        # Initialize analyzer
        analyzer = ResumeAnalyzer()
        print("✅ ResumeAnalyzer initialized successfully")
        
        # Test sample resume creation
        sample_text = create_sample_resume()
        print(f"✅ Sample resume created ({len(sample_text)} characters)")
        
        # Test text analysis
        print("\n📝 Testing Text Analysis...")
        results = analyzer.analyze_resume_text(sample_text)
        
        if results.get('success'):
            print("✅ Text analysis completed successfully")
            
            # Display summary
            summary = analyzer.get_analysis_summary(results)
            print(f"📊 Analysis Summary:")
            print(f"   - Total Skills: {summary.get('total_skills', 0)}")
            print(f"   - Technical Skills: {summary.get('technical_skills', 0)}")
            print(f"   - Soft Skills: {summary.get('soft_skills', 0)}")
            print(f"   - Top Career: {summary.get('top_career', 'N/A')}")
            print(f"   - Career Score: {summary.get('top_career_score', 0):.1f}%")
            print(f"   - Resume Score: {summary.get('resume_score', 0):.1f}/100")
            
        else:
            print(f"❌ Text analysis failed: {results.get('error', 'Unknown error')}")
            return False
        
        # Test sample analysis
        print("\n🧪 Testing Sample Analysis...")
        sample_results = analyzer.run_sample_analysis()
        
        if sample_results.get('success'):
            print("✅ Sample analysis completed successfully")
        else:
            print(f"❌ Sample analysis failed: {sample_results.get('error', 'Unknown error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Backend test failed: {str(e)}")
        return False

def test_skills_extraction():
    """Test skills extraction specifically"""
    print("\n🔍 Testing Skills Extraction...")
    
    try:
        from backend.skills_extractor import SkillsExtractor
        
        # Initialize skills extractor
        extractor = SkillsExtractor()
        print("✅ SkillsExtractor initialized successfully")
        
        # Test text
        test_text = """
        I am a software engineer with experience in Python, JavaScript, React, and Node.js.
        I have strong communication skills and problem-solving abilities.
        I work well in teams and have leadership experience.
        """
        
        # Extract skills
        skills = extractor.extract_skills(test_text)
        
        print(f"✅ Skills extracted successfully:")
        print(f"   - Technical Skills: {skills.get('technical_skills', [])}")
        print(f"   - Soft Skills: {skills.get('soft_skills', [])}")
        print(f"   - Total Skills: {len(skills.get('all_skills', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Skills extraction test failed: {str(e)}")
        return False

def test_career_analysis():
    """Test career analysis specifically"""
    print("\n🎯 Testing Career Analysis...")
    
    try:
        from backend.career_analyzer import CareerAnalyzer
        
        # Initialize career analyzer
        analyzer = CareerAnalyzer()
        print("✅ CareerAnalyzer initialized successfully")
        
        # Test skills
        test_skills = {
            'technical_skills': ['Python', 'JavaScript', 'React', 'SQL'],
            'soft_skills': ['Communication', 'Problem Solving', 'Teamwork'],
            'all_skills': ['Python', 'JavaScript', 'React', 'SQL', 'Communication', 'Problem Solving', 'Teamwork']
        }
        
        # Analyze career fit
        career_analysis = analyzer.analyze_career_fit(test_skills, top_n=3)
        
        print(f"✅ Career analysis completed successfully:")
        for i, career in enumerate(career_analysis[:3], 1):
            print(f"   {i}. {career['career']}: {career['overall_score']:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Career analysis test failed: {str(e)}")
        return False

def test_resume_scoring():
    """Test resume scoring specifically"""
    print("\n📊 Testing Resume Scoring...")
    
    try:
        from backend.resume_scorer import ResumeScorer
        
        # Initialize resume scorer
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
        print(f"   - Overall Score: {score.get('overall_score', 0):.1f}/100")
        print(f"   - Formatting: {score.get('breakdown', {}).get('formatting_score', 0):.1f}/100")
        print(f"   - Content: {score.get('breakdown', {}).get('content_score', 0):.1f}/100")
        print(f"   - Keywords: {score.get('breakdown', {}).get('keyword_score', 0):.1f}/100")
        print(f"   - Action Verbs: {score.get('breakdown', {}).get('action_verb_score', 0):.1f}/100")
        
        return True
        
    except Exception as e:
        print(f"❌ Resume scoring test failed: {str(e)}")
        return False

def test_file_parsing():
    """Test file parsing specifically"""
    print("\n📄 Testing File Parsing...")
    
    try:
        from backend.parser import ResumeParser
        
        # Initialize parser
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
        
        return True
        
    except Exception as e:
        print(f"❌ File parsing test failed: {str(e)}")
        return False

def test_export_functionality():
    """Test export functionality"""
    print("\n💾 Testing Export Functionality...")
    
    try:
        analyzer = ResumeAnalyzer()
        
        # Run sample analysis
        results = analyzer.run_sample_analysis()
        
        if results.get('success'):
            # Test JSON export
            export_success = analyzer.save_analysis_results(results, "test_export.json")
            
            if export_success:
                print("✅ JSON export completed successfully")
                
                # Test loading results
                loaded_results = analyzer.load_results("test_export.json")
                if loaded_results:
                    print("✅ Results loading completed successfully")
                    
                    # Clean up test file
                    try:
                        os.remove("test_export.json")
                        print("✅ Test file cleaned up")
                    except:
                        pass
                    
                    return True
                else:
                    print("❌ Results loading failed")
                    return False
            else:
                print("❌ JSON export failed")
                return False
        else:
            print("❌ Sample analysis failed for export test")
            return False
            
    except Exception as e:
        print(f"❌ Export functionality test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Resume Analyzer Tests")
    print("=" * 50)
    
    # Test individual components
    tests = [
        ("Backend Components", test_backend_components),
        ("Skills Extraction", test_skills_extraction),
        ("Career Analysis", test_career_analysis),
        ("Resume Scoring", test_resume_scoring),
        ("File Parsing", test_file_parsing),
        ("Export Functionality", test_export_functionality)
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
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Resume Analyzer is ready to use.")
        print("\n📝 To run the Streamlit app:")
        print("   streamlit run app.py")
        print("\n📝 To use the API:")
        print("   from backend import ResumeAnalyzer")
        print("   analyzer = ResumeAnalyzer()")
        print("   results = analyzer.analyze_resume_text('your resume text')")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

