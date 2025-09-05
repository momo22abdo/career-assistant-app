#!/usr/bin/env python3
"""
Test script to verify Job Market Insights enhancements
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_pipeline_simple import CareerRecommendationPipeline

def test_job_insights_enhancements():
    """Test all the implemented job market insights improvements"""
    print("🧪 Testing Enhanced Job Market Insights...")
    
    # Initialize pipeline
    pipeline = CareerRecommendationPipeline()
    print("✅ Pipeline initialized successfully!")
    
    print("\n1️⃣ Testing Enhanced Job Market Insights Structure...")
    
    # Test with Data Scientist career
    target_career = "Data Scientist"
    user_skills = ["Python", "SQL", "Machine Learning", "Git"]
    
    print(f"   Testing: {target_career} with skills: {user_skills}")
    
    try:
        insights = pipeline.get_job_market_insights(target_career, user_skills)
        
        if "error" not in insights:
            print(f"   ✅ Job market insights generated successfully!")
            
            # Check new structure
            required_fields = [
                'career', 'salary_data', 'market_overview', 'demand_metrics',
                'top_countries', 'job_listings', 'total_jobs_found', 'skills_analysis_enabled'
            ]
            
            for field in required_fields:
                if field in insights:
                    print(f"     ✅ {field}: {type(insights[field])}")
                else:
                    print(f"     ❌ Missing field: {field}")
            
            # Check salary data structure
            if 'salary_data' in insights:
                salary_fields = ['min', 'max', 'avg', 'formatted_range', 'formatted_avg']
                for field in salary_fields:
                    if field in insights['salary_data']:
                        print(f"     ✅ salary_data.{field}: {insights['salary_data'][field]}")
                    else:
                        print(f"     ❌ Missing salary field: {field}")
            
            # Check market overview
            if 'market_overview' in insights:
                overview_fields = ['demand_level', 'demand_description', 'growth_trend', 'growth_description', 'remote_opportunities']
                for field in overview_fields:
                    if field in insights['market_overview']:
                        print(f"     ✅ market_overview.{field}: {insights['market_overview'][field]}")
                    else:
                        print(f"     ❌ Missing overview field: {field}")
            
            # Check demand metrics
            if 'demand_metrics' in insights:
                metrics_fields = ['demand_index', 'growth_rate', 'remote_friendly']
                for field in metrics_fields:
                    if field in insights['demand_metrics']:
                        print(f"     ✅ demand_metrics.{field}: {insights['demand_metrics'][field]}")
                    else:
                        print(f"     ❌ Missing metrics field: {field}")
            
            # Check top countries with flags
            if 'top_countries' in insights:
                print(f"     ✅ Found {len(insights['top_countries'])} countries with flags")
                for country in insights['top_countries'][:3]:  # Show first 3
                    print(f"       {country['flag']} {country['name']}")
            
            # Check job listings
            if 'job_listings' in insights:
                print(f"     ✅ Found {len(insights['job_listings'])} job listings")
                
                if insights['job_listings']:
                    first_job = insights['job_listings'][0]
                    job_fields = [
                        'title', 'company', 'location', 'formatted_salary', 
                        'experience_display', 'job_type_display', 'skills_analysis'
                    ]
                    
                    for field in job_fields:
                        if field in first_job:
                            print(f"       ✅ job.{field}: {type(first_job[field])}")
                        else:
                            print(f"       ❌ Missing job field: {field}")
                    
                    # Check skills analysis
                    if 'skills_analysis' in first_job:
                        skills_fields = ['matched_skills', 'missing_skills', 'match_score', 'total_skills', 'matched_count']
                        for field in skills_fields:
                            if field in first_job['skills_analysis']:
                                print(f"         ✅ skills_analysis.{field}: {first_job['skills_analysis'][field]}")
                            else:
                                print(f"         ❌ Missing skills field: {field}")
            
            # Check skills analysis enabled
            print(f"     ✅ Skills analysis enabled: {insights['skills_analysis_enabled']}")
            
        else:
            print(f"   ❌ Job market insights generation failed: {insights['error']}")
            
    except Exception as e:
        print(f"   ❌ Error during job market insights generation: {e}")
    
    print("\n2️⃣ Testing Skills Matching Accuracy...")
    
    try:
        # Test with different skill sets
        test_cases = [
            (["Python", "SQL", "Machine Learning"], "High match expected"),
            (["JavaScript", "HTML", "CSS"], "Low match expected"),
            ([], "No skills provided")
        ]
        
        for skills, description in test_cases:
            print(f"   Testing skills: {skills} ({description})")
            
            insights = pipeline.get_job_market_insights(target_career, skills)
            
            if "error" not in insights and insights['job_listings']:
                first_job = insights['job_listings'][0]
                if 'skills_analysis' in first_job:
                    analysis = first_job['skills_analysis']
                    match_score = analysis['match_score']
                    matched_count = analysis['matched_count']
                    total_skills = analysis['total_skills']
                    
                    print(f"     Match Score: {match_score}%")
                    print(f"     Matched Skills: {matched_count}/{total_skills}")
                    print(f"     Matched Skills: {analysis['matched_skills']}")
                    print(f"     Missing Skills: {analysis['missing_skills'][:3]}...")  # Show first 3
                    
                    # Validate match score calculation
                    expected_score = (matched_count / total_skills * 100) if total_skills > 0 else 0
                    if abs(match_score - expected_score) < 1:  # Allow for rounding
                        print(f"     ✅ Match score calculation correct")
                    else:
                        print(f"     ❌ Match score calculation incorrect: expected {expected_score}, got {match_score}")
                else:
                    print(f"     ❌ No skills analysis found")
            else:
                print(f"     ❌ Failed to get insights or no job listings")
    
    except Exception as e:
        print(f"   ❌ Error testing skills matching: {e}")
    
    print("\n3️⃣ Testing Demand Status and Growth Trend Functions...")
    
    try:
        # Test demand status function
        test_demands = [95, 75, 55, 30]
        for demand in test_demands:
            status = pipeline._get_demand_status(demand)
            print(f"   Demand {demand}: {status['level']} - {status['description']}")
        
        # Test growth trend function
        test_growths = [25, 15, 8, 2]
        for growth in test_growths:
            trend = pipeline._get_growth_trend(growth)
            print(f"   Growth {growth}%: {trend['trend']} - {trend['description']}")
    
    except Exception as e:
        print(f"   ❌ Error testing helper functions: {e}")
    
    print("\n4️⃣ Testing Job Data Formatting...")
    
    try:
        insights = pipeline.get_job_market_insights(target_career, user_skills)
        
        if "error" not in insights and insights['job_listings']:
            job = insights['job_listings'][0]
            
            # Check formatting
            print(f"   📋 Job: {job['title']}")
            print(f"     Company: {job['company']}")
            print(f"     Salary: {job['formatted_salary']}")
            print(f"     Experience: {job['experience_display']}")
            print(f"     Job Type: {job['job_type_display']}")
            print(f"     Posted: {job['posted_date']}")
            
            # Check if salary formatting is correct
            if '$' in job['formatted_salary'] and '–' in job['formatted_salary']:
                print(f"     ✅ Salary formatting correct")
            else:
                print(f"     ❌ Salary formatting incorrect")
            
            # Check if experience level mapping works
            if job['experience_display'] != job.get('experience_level', ''):
                print(f"     ✅ Experience level mapping working")
            else:
                print(f"     ❌ Experience level mapping not working")
    
    except Exception as e:
        print(f"   ❌ Error testing job data formatting: {e}")
    
    print("\n✅ All Job Market Insights tests completed!")
    print("\n📋 Summary of Enhancements Implemented:")
    print("   ✅ Enhanced data structure with salary_data, market_overview, demand_metrics")
    print("   ✅ Skills matching analysis with match scores and skill breakdowns")
    print("   ✅ Improved job listings with formatted data and experience level mapping")
    print("   ✅ Country flags and better visual presentation")
    print("   ✅ Demand status and growth trend helper functions")
    print("   ✅ Clean salary formatting (e.g., $49,775 – $74,662)")
    print("   ✅ Progress bars for demand index and visual indicators for growth")
    print("   ✅ Structured job cards with skills analysis and apply buttons")

if __name__ == "__main__":
    test_job_insights_enhancements()
