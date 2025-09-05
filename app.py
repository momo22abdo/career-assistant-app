import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_pipeline_simple import CareerRecommendationPipeline
from file_parser import parse_uploaded_file, validate_resume_content, get_file_info
from enhanced_resume_analyzer import EnhancedResumeAnalyzer
from enhanced_peer_benchmarking import EnhancedPeerBenchmarking
from ai_career_benchmarking_assistant import AICareerBenchmarkingAssistant

# Page configuration
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .success-metric {
        border-left-color: #28a745;
    }
    .warning-metric {
        border-left-color: #ffc107;
    }
    .danger-metric {
        border-left-color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_pipeline():
    """Load the AI pipeline with caching"""
    return CareerRecommendationPipeline()

@st.cache_resource
def load_enhanced_analyzer():
    """Load the enhanced resume analyzer with caching"""
    pipeline = load_pipeline()
    return EnhancedResumeAnalyzer(pipeline.career_skills_df, pipeline.career_keywords_df)

@st.cache_resource
def load_enhanced_peer_benchmarking():
    """Load the enhanced peer benchmarking with caching"""
    pipeline = load_pipeline()
    return EnhancedPeerBenchmarking(pipeline.career_skills_df, pipeline.peer_profiles_df)

@st.cache_resource
def load_ai_benchmarking_assistant():
    """Load the AI career benchmarking assistant with caching"""
    return AICareerBenchmarkingAssistant()

def main():
    # Initialize pipeline
    pipeline = load_pipeline()
    
    # Header
    st.markdown('<h1 class="main-header">🚀 AI Career Assistant</h1>', unsafe_allow_html=True)
    st.markdown("### Your intelligent guide to career success and skill development")
    
    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        [
            "🏠 Home",
            "🎯 Skill Matching",
            "📊 Gap Analysis", 
            "📚 Learning Path",
            "💼 Job Market Insights",
            "📄 Resume Analyzer",
            "🤖 AI Chatbot",
            "🗺️ Career Roadmap",
            "👥 Peer Benchmarking",
            "🔮 Recommendations"
        ]
    )
    
    # Route to different pages
    if page == "🏠 Home":
        show_home_page(pipeline)
    elif page == "🎯 Skill Matching":
        show_skill_matching_page(pipeline)
    elif page == "📊 Gap Analysis":
        show_gap_analysis_page(pipeline)
    elif page == "📚 Learning Path":
        show_learning_path_page(pipeline)
    elif page == "💼 Job Market Insights":
        show_job_insights_page(pipeline)
    elif page == "📄 Resume Analyzer":
        show_resume_analyzer_page(pipeline)
    elif page == "🤖 AI Chatbot":
        show_chatbot_page(pipeline)
    elif page == "🗺️ Career Roadmap":
        show_roadmap_page(pipeline)
    elif page == "👥 Peer Benchmarking":
        show_peer_benchmarking_page(pipeline)
    elif page == "🔮 Recommendations":
        show_recommendations_page(pipeline)

def show_home_page(pipeline):
    """Display the home page with overview"""
    st.markdown("## Welcome to Your AI Career Assistant! 🎉")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Smart Skill Matching</h3>
            <p>Enter your skills and discover the best matching career paths with match percentages.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Gap Analysis</h3>
            <p>Identify missing skills needed for your target career and get personalized suggestions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Learning Path</h3>
            <p>Get structured learning recommendations from beginner to advanced levels.</p>
        </div>
        """, unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3>💼 Job Market Insights</h3>
            <p>Explore salary ranges, demand trends, and top hiring countries for any career.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Resume Analyzer</h3>
            <p>Upload your resume and get AI-powered career fit analysis and improvement suggestions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Chatbot</h3>
            <p>Ask career-related questions and get instant, intelligent responses.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start section
    st.markdown("## 🚀 Quick Start")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Get Started in 3 Steps:
        1. **Enter Your Skills**: Use the Skill Matching feature to see which careers match your current skills
        2. **Choose Your Target**: Pick a career that interests you and analyze the skill gaps
        3. **Start Learning**: Follow the personalized learning path to achieve your career goals
        """)
    
    with col2:
        # Quick skill input
        st.markdown("### Try It Now!")
        quick_skills = st.text_input(
            "Enter your skills (comma-separated):",
            placeholder="e.g., Python, SQL, Machine Learning"
        )
        
        if st.button("Quick Match", type="primary"):
            if quick_skills:
                skills_list = [skill.strip() for skill in quick_skills.split(",")]
                matches = pipeline.skill_matching(skills_list)
                
                if matches:
                    st.success(f"Top match: **{matches[0]['career']}** ({matches[0]['match_percentage']}%)")
                    st.info(f"Navigate to 'Skill Matching' for detailed analysis!")
                else:
                    st.warning("No matches found. Try different skills or check spelling.")
            else:
                st.error("Please enter some skills first!")

def show_skill_matching_page(pipeline):
    """Display the skill matching page"""
    st.markdown("## 🎯 Smart Skill Matching")
    st.markdown("Enter your skills to discover the best matching career paths!")
    
    # Skill input and configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_skills_input = st.text_area(
            "Enter your skills (one per line or comma-separated):",
            height=150,
            placeholder="Python\nSQL\nMachine Learning\nStatistics\nData Visualization\nCommunication\nProblem Solving"
        )
        
        # Top N results control
        col1a, col1b = st.columns(2)
        with col1a:
            top_n = st.selectbox(
                "Number of results to show:",
                [3, 5, 10, 15],
                index=1  # Default to 5
            )
    
    with col2:
        st.markdown("### 💡 Tips:")
        st.markdown("""
        - Be specific with your skills
        - Include both technical and soft skills
        - Don't worry about exact spelling
        - The AI will find the best matches
        - Core skills (Python, SQL, ML) carry more weight
        - Soft skills (Communication, Leadership) are valued
        """)
    
    if st.button("Find Career Matches", type="primary"):
        if user_skills_input:
            # Parse skills
            if "\n" in user_skills_input:
                skills_list = [skill.strip() for skill in user_skills_input.split("\n") if skill.strip()]
            else:
                skills_list = [skill.strip() for skill in user_skills_input.split(",") if skill.strip()]
            
            if skills_list:
                with st.spinner("Analyzing your skills..."):
                    matches = pipeline.skill_matching(skills_list, top_n=top_n)
                
                if matches:
                    st.success(f"Found {len(matches)} career matches!")
                    
                    # Display top matches
                    for i, match in enumerate(matches):
                        with st.expander(f"#{i+1} {match['career']} - {match['match_percentage']}% Match"):
                            # Score breakdown
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Base Score", f"{match['base_score']}%")
                            with col2:
                                st.metric("Bonus Score", f"+{match['bonus_score']}%")
                            with col3:
                                st.metric("Final Score", f"{match['match_percentage']}%")
                            
                            # Detailed breakdown
                            st.markdown("### 📊 Score Breakdown")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**⚖️ Weighted Analysis:**")
                                st.markdown(f"- **Weighted Match:** {match['weighted_match_percentage']}%")
                                st.markdown(f"- **Required Skills:** {match['required_match_percentage']}%")
                                st.markdown(f"- **Semantic Similarity:** {match['semantic_similarity']}")
                            
                            with col2:
                                st.markdown("**📈 Category Scores:**")
                                for category, score in match['category_scores'].items():
                                    if score > 0:
                                        st.markdown(f"- **{category.title()}:** {score}%")
                            
                            # Skills breakdown by category
                            st.markdown("### 🎯 Skills Analysis")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**✅ Matched Skills:**")
                                if match['matched_skills']:
                                    for category, skills in match['matched_skills'].items():
                                        if skills and isinstance(skills, list):
                                            st.markdown(f"**{category.title()}:**")
                                            for skill_info in skills[:3]:  # Show first 3 per category
                                                if isinstance(skill_info, dict) and 'skill' in skill_info:
                                                    st.markdown(f"  - {skill_info['skill']} (Weight: {skill_info.get('weight', 'N/A')})")
                                else:
                                    st.markdown("*No skills matched*")
                            
                            with col2:
                                st.markdown("**❌ Missing Skills:**")
                                if match['missing_skills']:
                                    # Show high-priority missing skills first
                                    for category in ['core', 'intermediate', 'supporting', 'soft']:
                                        if category in match['missing_skills'] and match['missing_skills'][category]:
                                            st.markdown(f"**{category.title()}:**")
                                            for skill_info in match['missing_skills'][category][:3]:  # Show first 3 per category
                                                if isinstance(skill_info, dict) and 'skill' in skill_info:
                                                    weight = skill_info.get('weight', 0)
                                                    if weight > 0.5:  # Show high-weight missing skills
                                                        st.markdown(f"  - {skill_info['skill']} (Weight: {weight})")
                                else:
                                    st.markdown("*No missing skills data*")
                            
                            # Required missing skills (critical)
                            if match['required_missing'] and any(match['required_missing'].values()):
                                st.markdown("### 🚨 Critical Missing Skills")
                                for category, skills in match['required_missing'].items():
                                    if skills and isinstance(skills, list):
                                        st.markdown(f"**{category.title()}:**")
                                        for skill_info in skills[:3]:
                                            if isinstance(skill_info, dict) and 'skill' in skill_info:
                                                st.markdown(f"  - {skill_info['skill']} (Required)")
                            
                            # Summary stats
                            st.markdown("### 📋 Summary")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                skills_covered = match.get('skills_covered', 0)
                                total_skills = match.get('total_career_skills', 0)
                                st.metric("Skills Covered", f"{skills_covered}/{total_skills}")
                            with col2:
                                required_pct = match.get('required_match_percentage', 0)
                                st.metric("Required Skills", f"{required_pct:.0f}%")
                            with col3:
                                total_required = match.get('total_required_skills', 0)
                                st.metric("Total Required", total_required)
                    
                    # Visualization
                    if len(matches) > 1:
                        st.markdown("### 📊 Match Overview")
                        
                        # Create bar chart
                        df_matches = pd.DataFrame(matches[:10])
                        fig = px.bar(
                            df_matches, 
                            x='match_percentage', 
                            y='career',
                            orientation='h',
                            title="Career Match Percentages",
                            color='match_percentage',
                            color_continuous_scale='viridis'
                        )
                        fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No career matches found. Try different skills or check your input.")
            else:
                st.error("Please enter at least one skill!")
        else:
            st.error("Please enter your skills first!")

def show_gap_analysis_page(pipeline):
    """Display the gap analysis page"""
    st.markdown("## 📊 Gap Analysis & Skill Suggestions")
    st.markdown("Analyze skill gaps for your target career and get personalized improvement suggestions!")
    
    # Get available careers
    careers = pipeline.career_skills_df['career'].unique().tolist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # User skills input
        user_skills_input = st.text_area(
            "Enter your current skills (one per line or comma-separated):",
            height=120,
            placeholder="Python\nSQL\nMachine Learning\nStatistics\nCommunication\nProblem Solving"
        )
        
        # Skill level input instructions
        with st.expander("💡 How to specify skill levels (optional)"):
            st.markdown("""
            You can specify skill levels to get more accurate analysis:
            
            **Format Examples:**
            - `Python (Advanced)` or `Python - Advanced`
            - `SQL (Intermediate)` or `SQL : Intermediate`
            - `Machine Learning` (will use intelligent default)
            
            **If no level specified:**
            - Core languages (Python, SQL, R, Java) → Intermediate
            - Core libraries (NumPy, Pandas, Seaborn, Matplotlib, Scikit-learn) → Intermediate
            - Advanced tools (TensorFlow, PyTorch, Docker, Kubernetes) → Advanced  
            - Basic tools (Git, Jupyter, Excel) → Beginner
            - Soft skills → Intermediate
            """)
        
        # Target career selection
        target_career = st.selectbox(
            "Select your target career:",
            ["Select a career..."] + careers
        )
    
    with col2:
        st.markdown("### 💡 How it works:")
        st.markdown("""
        1. **Enter your skills** - List all your current technical and soft skills
        2. **Choose target career** - Select the career you want to pursue
        3. **Get analysis** - See what skills you're missing and get suggestions
        4. **Plan learning** - Use the results to plan your skill development
        """)
    
    if st.button("Analyze Skill Gaps", type="primary"):
        if user_skills_input and target_career != "Select a career...":
            # Parse skills
            if "\n" in user_skills_input:
                skills_list = [skill.strip() for skill in user_skills_input.split("\n") if skill.strip()]
            else:
                skills_list = [skill.strip() for skill in user_skills_input.split(",") if skill.strip()]
            
            if skills_list:
                with st.spinner("Analyzing skill gaps..."):
                    gap_analysis = pipeline.gap_analysis(skills_list, target_career)
                
                if "error" not in gap_analysis:
                    # Display results
                    st.success(f"Analysis complete for {target_career}!")
                    
                    # Main completion percentage (importance-weighted)
                    st.markdown("### 🎯 Overall Career Readiness")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric(
                            "🎯 Completion %",
                            f"{gap_analysis['completion_percentage']}%",
                            delta=f"{gap_analysis['completion_percentage'] - 50:.1f}%"
                        )
                        st.markdown("*Importance-weighted required skills*")
                    
                    with col2:
                        st.metric(
                            "✅ Skills Covered",
                            gap_analysis['skills_covered'],
                            delta=f"+{gap_analysis['skills_covered']}"
                        )
                        st.markdown(f"*Total skills matched*")
                    
                    # Separate progress bars for required vs optional
                    st.markdown("### 📊 Skills Progress")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**🔴 Required Skills Completion**")
                        required_progress = gap_analysis.get('required_completion', 0) / 100
                        st.progress(required_progress)
                        st.markdown(f"{gap_analysis.get('required_completion', 0):.1f}% ({gap_analysis['required_covered']}/{gap_analysis['total_required']})")
                        
                        required_missing_count = gap_analysis.get('required_missing_count', len(gap_analysis['required_missing']))
                        st.metric(
                            "❌ Required Missing",
                            required_missing_count,
                            delta=f"-{required_missing_count}"
                        )
                    
                    with col2:
                        st.markdown("**🟡 Optional Skills Coverage**")
                        optional_progress = gap_analysis.get('optional_coverage', 0) / 100
                        st.progress(optional_progress)
                        st.markdown(f"{gap_analysis.get('optional_coverage', 0):.1f}% ({gap_analysis['optional_covered']}/{gap_analysis['total_optional']})")
                        
                        optional_missing_count = gap_analysis.get('optional_missing_count', len(gap_analysis['optional_missing']))
                        st.metric(
                            "💡 Optional Missing",
                            optional_missing_count,
                            delta=f"-{optional_missing_count}"
                        )
                    
                    # Skills breakdown with improved categorization
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### ✅ Skills You Have")
                        if gap_analysis['user_has']:
                            # Separate technical and soft skills
                            technical_skills = [s for s in gap_analysis['user_has'] if s.get('category', 'technical') != 'soft']
                            soft_skills = [s for s in gap_analysis['user_has'] if s.get('category') == 'soft']
                            
                            if technical_skills:
                                st.markdown("**🔧 Technical Skills:**")
                                for skill in technical_skills:
                                    difficulty_color = {
                                        'Beginner': '🟢',
                                        'Intermediate': '🟡', 
                                        'Advanced': '🔴'
                                    }
                                    st.markdown(f"{difficulty_color.get(skill['difficulty'], '⚪')} **{skill['skill']}** ({skill['difficulty']}) - Importance: {skill['importance']}/10")
                            
                            if soft_skills:
                                st.markdown("**🌟 Soft Skills:**")
                                for skill in soft_skills:
                                    difficulty_color = {
                                        'Beginner': '🟢',
                                        'Intermediate': '🟡', 
                                        'Advanced': '🔴'
                                    }
                                    st.markdown(f"{difficulty_color.get(skill['difficulty'], '⚪')} **{skill['skill']}** ({skill['difficulty']}) - Importance: {skill['importance']}/10")
                        else:
                            st.info("No matching skills found. Consider learning the basics first!")
                    
                    with col2:
                        st.markdown("### ❌ Required Skills Missing")
                        if gap_analysis['required_missing']:
                            # Separate technical and soft skills
                            technical_missing = [s for s in gap_analysis['required_missing'] if s.get('category', 'technical') != 'soft']
                            soft_missing = [s for s in gap_analysis['required_missing'] if s.get('category') == 'soft']
                            
                            if technical_missing:
                                st.markdown("**🔧 Technical Skills:**")
                                for skill in technical_missing[:3]:
                                    difficulty_color = {
                                        'Beginner': '🟢',
                                        'Intermediate': '🟡',
                                        'Advanced': '🔴'
                                    }
                                    st.markdown(f"{difficulty_color.get(skill['difficulty'], '⚪')} **{skill['skill']}** ({skill['difficulty']}) - Importance: {skill['importance']}/10")
                            
                            if soft_missing:
                                st.markdown("**🌟 Soft Skills:**")
                                for skill in soft_missing[:2]:
                                    difficulty_color = {
                                        'Beginner': '🟢',
                                        'Intermediate': '🟡',
                                        'Advanced': '🔴'
                                    }
                                    st.markdown(f"{difficulty_color.get(skill['difficulty'], '⚪')} **{skill['skill']}** ({skill['difficulty']}) - Importance: {skill['importance']}/10")
                        else:
                            st.success("Great! You have all required skills!")
                    
                    # Optional skills with improved display
                    if gap_analysis['optional_missing']:
                        st.markdown("### 💡 Optional Skills to Consider")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            technical_optional = [s for s in gap_analysis['optional_missing'] if s.get('category', 'technical') != 'soft']
                            if technical_optional:
                                st.markdown("**🔧 Technical Skills:**")
                                for skill in technical_optional[:3]:
                                    difficulty_color = {
                                        'Beginner': '🟢',
                                        'Intermediate': '🟡',
                                        'Advanced': '🔴'
                                    }
                                    st.markdown(f"{difficulty_color.get(skill['difficulty'], '⚪')} **{skill['skill']}** ({skill['difficulty']}) - Importance: {skill['importance']}/10")
                    
                        with col2:
                            soft_optional = [s for s in gap_analysis['optional_missing'] if s.get('category') == 'soft']
                            if soft_optional:
                                st.markdown("**🌟 Soft Skills:**")
                                for skill in soft_optional[:3]:
                                    difficulty_color = {
                                        'Beginner': '🟢',
                                        'Intermediate': '🟡',
                                        'Advanced': '🔴'
                                    }
                                    st.markdown(f"{difficulty_color.get(skill['difficulty'], '⚪')} **{skill['skill']}** ({skill['difficulty']}) - Importance: {skill['importance']}/10")
                    
                    # Recommended soft skills section (not marked as missing)
                    st.markdown("### 🌟 Recommended Soft Skills")
                    st.info("""
                    **💡 These soft skills are valuable for your target career but not required:**
                    
                    - **Communication** - Essential for collaboration and presenting findings
                    - **Problem Solving** - Critical for debugging and optimization
                    - **Teamwork** - Important for project collaboration
                    - **Leadership** - Valuable for career advancement
                    - **Critical Thinking** - Helps with system design and troubleshooting
                    
                    Consider developing these alongside your technical skills!
                    """)
                    
                    # Detailed analysis section
                    st.markdown("### 📊 Detailed Analysis")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Required Skills:** {gap_analysis['required_covered']}/{gap_analysis['total_required']}")
                        st.markdown(f"**Optional Skills:** {gap_analysis['optional_covered']}/{gap_analysis['total_optional']}")
                        st.markdown(f"**Total Skills:** {gap_analysis['skills_covered']}/{gap_analysis['total_skills_needed']}")
                    
                    with col2:
                        st.markdown(f"**Required Importance:** {gap_analysis['user_required_importance']}/{gap_analysis['total_required_importance']}")
                        st.markdown(f"**Completion Formula:** (User Required Importance / Total Required Importance) × 100")
                        st.markdown(f"**Result:** {gap_analysis['user_required_importance']} ÷ {gap_analysis['total_required_importance']} × 100 = {gap_analysis['completion_percentage']}%")
                    
                    # Importance-weighted explanation
                    st.info(f"""
                    **🎯 Importance-Weighted Completion Calculation:**
                    
                    Your completion percentage is calculated based on the **importance scores** of required skills you have, not just the count.
                    
                    - **You have:** {gap_analysis['user_required_importance']} importance points from required skills
                    - **Total needed:** {gap_analysis['total_required_importance']} importance points from all required skills
                    - **Formula:** ({gap_analysis['user_required_importance']} ÷ {gap_analysis['total_required_importance']}) × 100 = **{gap_analysis['completion_percentage']}%**
                    
                    This gives you a more accurate picture of your career readiness!
                    """)
                    
                    # Recommendations with improved logic
                    st.markdown("### 🎯 Recommendations")
                    completion = gap_analysis['completion_percentage']
                    
                    if completion < 30:
                        st.warning("**🚨 Critical Gap Detected!** Focus on fundamental required skills first. Start with beginner-level technical skills and basic soft skills like Communication.")
                    elif completion < 50:
                        st.warning("**⚠️ Significant Gap** Focus on remaining required skills, especially those with high importance scores. Build a solid foundation before moving to advanced topics.")
                    elif completion < 70:
                        st.info("**📈 Good Progress!** You're on the right track. Focus on remaining required skills, then consider high-value optional skills.")
                    elif completion < 90:
                        st.success("**🎉 Strong Foundation!** You're well-prepared. Focus on remaining gaps and consider advanced optional skills for specialization.")
                    else:
                        st.success("**🏆 Excellent!** You're highly qualified. Consider advanced optional skills, specializations, or mentoring others.")
                    
                    # Next steps with specific guidance
                    st.markdown("### 📚 Next Steps")
                    if completion < 50:
                        st.markdown("1. **🔧 Master Fundamentals** - Focus on missing required technical skills with high importance")
                        st.markdown("2. **🌟 Build Soft Skills** - Develop Communication and Problem Solving abilities")
                        st.markdown("3. **📖 Structured Learning** - Use the Learning Path feature for beginner courses")
                        st.markdown("4. **🎯 Practice Projects** - Apply skills in real projects to reinforce learning")
                    else:
                        st.markdown("1. **🎯 Fill Remaining Gaps** - Complete any missing required skills")
                        st.markdown("2. **💡 Explore Optional Skills** - Consider high-value optional skills for specialization")
                        st.markdown("3. **🚀 Advanced Projects** - Work on complex projects to demonstrate expertise")
                        st.markdown("4. **👥 Peer Benchmarking** - Compare your skills with others in your field")
                    
                else:
                    st.error(f"Error: {gap_analysis['error']}")
            else:
                st.error("Please enter at least one skill!")
        else:
            st.error("Please enter your skills and select a target career!")

def show_learning_path_page(pipeline):
    """Display the learning path page"""
    st.markdown("## 📚 Learning Path Generator")
    st.markdown("Get personalized learning recommendations from beginner to advanced levels!")
    
    # Get available careers
    careers = pipeline.career_skills_df['career'].unique().tolist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # User skills input
        user_skills_input = st.text_area(
            "Enter your current skills (one per line or comma-separated):",
            height=120,
            placeholder="Python\nSQL\nMachine Learning"
        )
        
        # Target career selection
        target_career = st.selectbox(
            "Select your target career:",
            ["Select a career..."] + careers
        )
    
    with col2:
        st.markdown("### 🎓 Learning Levels:")
        st.markdown("""
        - **🟢 Beginner**: Foundation concepts and basic skills
        - **🟡 Intermediate**: Practical applications and projects
        - **🔴 Advanced**: Specialized knowledge and expertise
        """)
        
        # Study pace selector
        st.markdown("### ⏱️ Study Pace:")
        study_pace = st.selectbox(
            "Choose your weekly study hours:",
            ["10 hours/week", "15 hours/week", "20 hours/week"],
            help="This will help calculate your estimated timeline"
        )
    
    if st.button("Generate Learning Path", type="primary"):
        if user_skills_input and target_career != "Select a career...":
            # Parse skills
            if "\n" in user_skills_input:
                skills_list = [skill.strip() for skill in user_skills_input.split("\n") if skill.strip()]
            else:
                skills_list = [skill.strip() for skill in user_skills_input.split(",") if skill.strip()]
            
            if skills_list:
                with st.spinner("Generating personalized learning path..."):
                    learning_path = pipeline.get_learning_path(target_career, skills_list)
                
                if "error" not in learning_path:
                    st.success(f"Learning path generated for {target_career}!")
                    
                    # Current progress with separate technical vs soft skills
                    st.markdown("### 📊 Current Progress")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("🎯 Overall Completion", f"{learning_path['current_completion']}%")
                    
                    with col2:
                        st.metric("🔴 Technical Skills", f"{learning_path['technical_completion']}%")
                    
                    with col3:
                        st.metric("💬 Soft Skills", f"{learning_path['soft_skills_completion']}%")
                    
                    # Progress bars
                    st.markdown("**Overall Progress:**")
                    overall_progress = learning_path['current_completion'] / 100
                    st.progress(overall_progress)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Technical Skills Progress:**")
                        tech_progress = learning_path['technical_completion'] / 100
                        st.progress(tech_progress)
                    
                    with col2:
                        st.markdown("**Soft Skills Progress:**")
                        soft_progress = learning_path['soft_skills_completion'] / 100
                        st.progress(soft_progress)
                    
                    # Learning phases
                    st.markdown("### 🗺️ Learning Roadmap")
                    
                    for i, phase in enumerate(learning_path['phases']):
                        if phase['skills']:
                            with st.expander(f"Phase {i+1}: {phase['name']} ({phase['level']}) - {phase['hours']}h", expanded=i==0):
                                st.markdown(f"**Focus**: {phase['level']} level skills")
                                
                                # Skills to learn
                                st.markdown("**Skills to Learn:**")
                                for skill in phase['skills']:
                                    difficulty_color = {
                                        'Beginner': '🟢',
                                        'Intermediate': '🟡',
                                        'Advanced': '🔴'
                                    }
                                    category_icon = '💬' if skill.get('category') == 'soft' else '⚙️'
                                    st.markdown(f"{difficulty_color.get(skill['difficulty'], '⚪')} {category_icon} **{skill['skill']}** (Importance: {skill['importance']}/10)")
                                
                                # Recommended courses
                                if 'courses' in phase and phase['courses']:
                                    st.markdown("**Recommended Courses:**")
                                    for course in phase['courses']:
                                        with st.container():
                                            # Course quality indicator
                                            rating_emoji = "⭐" * int(course['rating'])
                                            quality_badge = "🟢 High Quality" if course.get('rating', 0) >= 4.3 else "🟡 Good Quality"
                                            if course.get('low_rating_warning'):
                                                quality_badge = "⚠️ Lower Rating"
                                            
                                            st.markdown(f"**📖 {course['title']}** {quality_badge}")
                                            col1, col2, col3 = st.columns(3)
                                            with col1:
                                                st.markdown(f"Platform: {course['platform']}")
                                            with col2:
                                                st.markdown(f"Duration: {course['duration_hours']}h")
                                            with col3:
                                                st.markdown(f"Rating: {course['rating']} {rating_emoji}")
                                            
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                st.markdown(f"Price: ${course['price']}")
                                            with col2:
                                                if course['certificate']:
                                                    st.markdown("🏆 Certificate Available")
                                            
                                            if st.button(f"View Course", key=f"course_{course['title']}"):
                                                st.markdown(f"🔗 [Course Link]({course['url']})")
                                
                                # Phase completion tips
                                st.markdown("**💡 Tips for this phase:**")
                                if phase['level'] == 'Beginner':
                                    st.markdown("- Focus on understanding fundamentals")
                                    st.markdown("- Practice with simple projects")
                                    st.markdown("- Don't rush, build solid foundation")
                                elif phase['level'] == 'Intermediate':
                                    st.markdown("- Apply skills in real projects")
                                    st.markdown("- Join communities and forums")
                                    st.markdown("- Build a portfolio")
                                else:
                                    st.markdown("- Work on complex projects")
                                    st.markdown("- Contribute to open source")
                                    st.markdown("- Consider specialization")
                    
                    # Improved timeline with multiple pace options
                    st.markdown("### ⏱️ Estimated Timeline")
                    timeline = learning_path['timeline']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Course Hours", f"{timeline['total_course_hours']}h")
                    with col2:
                        st.metric("Total Study Hours", f"{timeline['total_study_hours']}h")
                    with col3:
                        st.metric("Buffer (20%)", f"{timeline['total_study_hours'] - timeline['total_course_hours']}h")
                    
                    st.markdown("**📅 Timeline by Study Pace:**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("10h/week", f"{timeline['weeks_10h']} weeks")
                    with col2:
                        st.metric("15h/week", f"{timeline['weeks_15h']} weeks")
                    with col3:
                        st.metric("20h/week", f"{timeline['weeks_20h']} weeks")
                    
                    st.info("💡 **Note**: Timeline includes 20% buffer for practice, projects, and review. Choose a pace that fits your schedule!")
                    
                    # Success tips
                    st.markdown("### 🎯 Success Tips")
                    st.markdown("1. **Consistent Practice**: Study regularly, even if just 1-2 hours daily")
                    st.markdown("2. **Hands-on Projects**: Apply what you learn in real projects")
                    st.markdown("3. **Community Engagement**: Join online communities and forums")
                    st.markdown("4. **Portfolio Building**: Document your learning journey")
                    st.markdown("5. **Networking**: Connect with professionals in your target field")
                    
                else:
                    st.error(f"Error: {learning_path['error']}")
            else:
                st.error("Please enter at least one skill!")
        else:
            st.error("Please enter your skills and select a target career!")

def show_job_insights_page(pipeline):
    """Display the enhanced job market insights page"""
    st.markdown("## 💼 Job Market Insights")
    st.markdown("Explore salary ranges, demand trends, and market opportunities for any career!")
    
    # Get available careers
    careers = pipeline.salary_demand_df['career'].unique().tolist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Career selection
        selected_career = st.selectbox(
            "Select a career to analyze:",
            ["Select a career..."] + careers
        )
        
        # Optional: Add user skills for job matching
        add_skills = st.checkbox("Add my skills for job matching", help="Compare your skills with job requirements")
        
        user_skills = []
        if add_skills:
            skills_input = st.text_area(
                "Enter your skills (comma-separated):",
                placeholder="Python, SQL, Machine Learning, Git",
                height=80
            )
            if skills_input:
                user_skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
    
    with col2:
        st.markdown("### 📈 What you'll see:")
        st.markdown("""
        - 💰 **Salary ranges** with clean formatting
        - 📊 **Demand indicators** with progress bars
        - 📈 **Growth trends** with visual indicators
        - 🌍 **Top countries** with flag emojis
        - 💼 **Job listings** with skills matching
        - 🎯 **Match scores** for each position
        """)
    
    if st.button("Get Market Insights", type="primary"):
        if selected_career != "Select a career...":
            with st.spinner("Analyzing job market data..."):
                insights = pipeline.get_job_market_insights(selected_career, user_skills)
            
            if "error" not in insights:
                st.success(f"🎉 Market insights for {selected_career}!")
                
                # 1. Salary Range & Charts
                st.markdown("### 💰 Salary Overview")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "💰 Salary Range",
                        insights['salary_data']['formatted_range'],
                        help="Annual salary range for this career"
                    )
                
                with col2:
                    st.metric(
                        "📊 Average Salary",
                        insights['salary_data']['formatted_avg'],
                        help="Median annual salary"
                    )
                
                with col3:
                    if "demand_metrics" in insights and "remote_friendly" in insights["demand_metrics"]:
                        remote_icon = "🌐" if insights['demand_metrics']['remote_friendly'] else "🏢"
                        remote_text = "High Remote" if insights['demand_metrics']['remote_friendly'] else "Limited Remote"
                    else:
                        remote_icon = "❓"
                        remote_text = "Not available"
                    st.metric(
                        f"{remote_icon} Remote Work",
                        remote_text,
                        help="Remote work opportunities"
                    )
                
                # Salary visualization
                salary_data = {
                    'Min': insights['salary_data']['min'],
                    'Average': insights['salary_data']['avg'],
                    'Max': insights['salary_data']['max']
                }
                
                # Create a simple bar chart
                import plotly.express as px
                fig = px.bar(
                    x=list(salary_data.keys()),
                    y=list(salary_data.values()),
                    title=f"Salary Range for {selected_career}",
                    color=list(salary_data.values()),
                    color_continuous_scale='viridis'
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # 2. Demand & Growth
                st.markdown("### 📊 Market Demand & Growth")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📈 Demand Index**")
                    if "demand_metrics" in insights and "demand_index" in insights["demand_metrics"]:
                        demand_value = insights['demand_metrics']['demand_index']
                        demand_progress = demand_value / 100
                    else:
                        demand_value = 0
                        demand_progress = 0
                    
                    # Color-coded progress bar
                    if demand_value >= 80:
                        color = "success"
                    elif demand_value >= 60:
                        color = "info"
                    else:
                        color = "warning"
                    
                    st.progress(demand_progress, text=f"{demand_value}/100")
                    if "market_overview" in insights and "demand_level" in insights["market_overview"] and "demand_description" in insights["market_overview"]:
                        st.markdown(f"**{insights['market_overview']['demand_level']}** - {insights['market_overview']['demand_description']}")
                    else:
                        st.markdown("**Market overview not available**")
                
                with col2:
                    st.markdown("**📈 Growth Trend**")
                    if "demand_metrics" in insights and "growth_rate" in insights["demand_metrics"]:
                        growth_rate = insights['demand_metrics']['growth_rate']
                    else:
                        growth_rate = 0
                    if "market_overview" in insights and "growth_trend" in insights["market_overview"]:
                        st.markdown(f"### {insights['market_overview']['growth_trend']}")
                        if "growth_description" in insights["market_overview"]:
                            st.markdown(insights['market_overview']['growth_description'])
                    else:
                        st.markdown("### Growth data not available")
                    
                    # Growth indicator
                    if growth_rate >= 20:
                        st.success("🚀 **Rapidly Growing Field**")
                    elif growth_rate >= 10:
                        st.info("📈 **Growing Field**")
                    elif growth_rate >= 5:
                        st.warning("➡️ **Stable Field**")
                    else:
                        st.error("📉 **Slow Growth**")
                
                # 3. Top Countries
                    st.markdown("### 🌍 Top Hiring Countries")
                    countries = insights['top_countries']
                    
                # Display countries in a grid
                cols = st.columns(3)
                for i, country in enumerate(countries):
                    col_idx = i % 3
                    with cols[col_idx]:
                        st.markdown(f"{country['flag']} **{country['name']}**")
                
                # 4. Job Listings with Skills Matching
                st.markdown("### 💼 Recent Job Openings")
                
                if insights['skills_analysis_enabled']:
                    st.info(f"🔍 Showing {len(insights['job_listings'])} jobs, sorted by skills match")
                else:
                    st.info(f"💼 Showing {len(insights['job_listings'])} recent job openings")
                
                # Display jobs in cards
                for i, job in enumerate(insights['job_listings']):
                    with st.expander(f"📋 {job['title']} at {job['company']}", expanded=i < 2):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**🏢 Company:** {job['company']}")
                            st.markdown(f"**📍 Location:** {job['location']}")
                            st.markdown(f"**💼 Type:** {job['job_type_display']}")
                            st.markdown(f"**👨‍💼 Level:** {job['experience_display']}")
                            st.markdown(f"**💰 Salary:** {job['formatted_salary']}")
                            st.markdown(f"**📅 Posted:** {job['posted_date']}")
                        
                        with col2:
                            if insights['skills_analysis_enabled']:
                                # Skills matching analysis
                                skills_analysis = job['skills_analysis']
                                st.markdown("**🎯 Skills Match**")
                                
                                # Match score with color
                                match_score = skills_analysis['match_score']
                                if match_score >= 80:
                                    score_color = "success"
                                elif match_score >= 60:
                                    score_color = "warning"
                                else:
                                    score_color = "error"
                                
                                st.metric("Match Score", f"{match_score}%", delta=f"{skills_analysis['matched_count']}/{skills_analysis['total_skills']} skills")
                                
                                # Skills breakdown
                                if skills_analysis['matched_skills']:
                                    st.markdown("**✅ Your Skills:**")
                                    for skill in skills_analysis['matched_skills'][:3]:  # Show first 3
                                        st.markdown(f"  • {skill}")
                                
                                if skills_analysis['missing_skills']:
                                    st.markdown("**❌ Missing Skills:**")
                                    for skill in skills_analysis['missing_skills'][:3]:  # Show first 3
                                        st.markdown(f"  • {skill}")
                            else:
                                st.markdown("**💡 Enable skills matching** to see how well you fit each job!")
                        
                        # Apply button
                        if st.button(f"Apply to {job['company']}", key=f"apply_{i}"):
                            st.markdown(f"🔗 [Application Link]({job['url']})")
                
                # Summary
                st.markdown("### 📋 Market Summary")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Jobs Found", insights['total_jobs_found'])
                
                with col2:
                    st.metric("Remote Opportunities", insights['market_overview']['remote_opportunities'])
                
                with col3:
                    st.metric("Top Countries", len(insights['top_countries']))
                
                # Tips based on market data
                st.markdown("### 💡 Career Tips")
                if "demand_metrics" in insights and "demand_index" in insights["demand_metrics"]:
                    demand_index = insights['demand_metrics']['demand_index']
                    if demand_index >= 80:
                        st.success("🎯 **High Demand Field**: Excellent time to enter this career!")
                    elif demand_index >= 60:
                        st.info("📈 **Growing Field**: Good opportunities available with the right skills.")
                    else:
                        st.warning("⚠️ **Competitive Market**: Focus on building unique skills and experience.")
                else:
                    st.info("📊 **Market Data**: Demand information not available for this career.")
                
                if "demand_metrics" in insights and "growth_rate" in insights["demand_metrics"] and insights['demand_metrics']['growth_rate'] >= 15:
                    st.success("🚀 **Fast Growth**: This field is expanding rapidly - great for career advancement!")
                
                if "demand_metrics" in insights and "remote_friendly" in insights["demand_metrics"] and insights['demand_metrics']['remote_friendly']:
                    st.info("🌐 **Remote-Friendly**: Many opportunities for remote work available.")
                
            else:
                st.error(f"Error: {insights['error']}")
        else:
            st.error("Please select a career to analyze!")

def show_resume_analyzer_page(pipeline):
    """Display the resume analyzer page"""
    st.markdown("## 📄 Resume Analyzer")
    st.markdown("Upload your resume and get AI-powered career fit analysis and improvement suggestions!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Resume input options
        input_method = st.radio(
            "Choose input method:",
            ["📝 Paste Resume Text", "📁 Upload Resume File"]
        )
        
        resume_text = ""
        
        if input_method == "📝 Paste Resume Text":
            resume_text = st.text_area(
                "Paste your resume content here:",
                height=300,
                placeholder="Paste your resume text here...\n\nExample:\nJohn Doe\nSoftware Engineer\n\nSkills: Python, SQL, Machine Learning\nExperience: 3 years in data analysis\nEducation: Computer Science Degree"
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload your resume (PDF, DOC, TXT):",
                type=['pdf', 'doc', 'docx', 'txt']
            )
            
            if uploaded_file:
                # Show file information
                file_info = get_file_info(uploaded_file)
                st.success(f"✅ **{file_info['name']}** ({file_info['size_mb']} MB)")
                
                # Parse the uploaded file
                with st.spinner("Extracting text from your resume..."):
                    resume_text = parse_uploaded_file(uploaded_file)
                
                if resume_text:
                    # Validate the content
                    validation = validate_resume_content(resume_text)
                    
                    if validation["warning"]:
                        st.warning(f"⚠️ {validation['warning']}")
                        if validation["suggestions"]:
                            with st.expander("💡 Suggestions"):
                                for suggestion in validation["suggestions"]:
                                    st.markdown(f"- {suggestion}")
                    
                    # Show preview of extracted text
                    with st.expander("📄 Preview extracted text"):
                        preview_text = resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
                        st.text_area("Extracted content:", preview_text, height=150, disabled=True)
                        st.info(f"Total characters extracted: {len(resume_text)}")
                else:
                    st.error("❌ Failed to extract text from the uploaded file. Please try a different format or use 'Paste Resume Text' option.")
    
    with col2:
        st.markdown("### 🔍 What we analyze:")
        st.markdown("""
        - **Skills Extraction**: Identify technical and soft skills
        - **Career Matching**: Find best-fit career paths
        - **Keyword Analysis**: Check for industry-relevant terms
        - **Improvement Suggestions**: Get specific recommendations
        - **Sentiment Analysis**: Assess resume tone and impact
        """)
        
        st.markdown("### 💡 Tips for better results:")
        st.markdown("""
        - Include all your technical skills
        - Mention specific tools and technologies
        - Add project descriptions
        - Include relevant keywords
        - Keep it comprehensive but concise
        """)
    
    if st.button("Analyze Resume", type="primary"):
        if resume_text.strip():
            with st.spinner("Analyzing your resume with enhanced ATS scoring..."):
                # Use enhanced analyzer
                enhanced_analyzer = load_enhanced_analyzer()
                analysis = enhanced_analyzer.analyze_resume(resume_text)
            
            st.success("Enhanced resume analysis complete!")
            
            # ATS Score Dashboard
            st.markdown("### 📊 ATS Resume Score")
            
            # Overall score with gauge
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                overall_score = analysis['ats_score']['overall_score']
                score_color = "🟢" if overall_score >= 80 else "🟡" if overall_score >= 60 else "🔴"
                st.metric("Overall Score", f"{score_color} {overall_score}/100")
            
            with col2:
                skills_score = analysis['ats_score']['skills_score']
                st.metric("Skills Score", f"{skills_score}/100")
            
            with col3:
                keywords_score = analysis['ats_score']['keywords_score']
                st.metric("Keywords Score", f"{keywords_score}/100")
            
            with col4:
                formatting_score = analysis['ats_score']['formatting_score']
                st.metric("Formatting Score", f"{formatting_score}/100")
            
            with col5:
                clarity_score = analysis['ats_score']['clarity_score']
                st.metric("Clarity Score", f"{clarity_score}/100")
            
            # Progress bars for each category
            st.markdown("**Score Breakdown:**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Skills & Keywords:**")
                st.progress(skills_score / 100, text=f"Skills: {skills_score}%")
                st.progress(keywords_score / 100, text=f"Keywords: {keywords_score}%")
            
            with col2:
                st.markdown("**Structure & Clarity:**")
                st.progress(formatting_score / 100, text=f"Formatting: {formatting_score}%")
                st.progress(clarity_score / 100, text=f"Clarity: {clarity_score}%")
            
            # Resume Summary
            st.markdown("### 📋 Resume Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Word Count", analysis['resume_summary']['word_count'])
            
            with col2:
                st.metric("Technical Skills", analysis['resume_summary']['technical_skills_count'])
            
            with col3:
                st.metric("Soft Skills", analysis['resume_summary']['soft_skills_count'])
            
            with col4:
                st.metric("Certifications", analysis['resume_summary']['certifications_count'])
            
            # Extracted Skills by Category
            st.markdown("### 🎯 Skills Analysis")
            
            # Technical Skills
            if analysis['extracted_skills']['technical']:
                st.markdown("**🔧 Technical Skills Found:**")
                for category, skills in analysis['extracted_skills']['technical'].items():
                    if skills:
                        st.markdown(f"**{category.replace('_', ' ').title()}:** {', '.join(skills[:5])}")
            
            # Soft Skills
            if analysis['extracted_skills']['soft']:
                st.markdown("**🌟 Soft Skills Found:**")
                soft_skills_text = ", ".join([skill['skill'] for skill in analysis['extracted_skills']['soft'][:5]])
                st.markdown(soft_skills_text)
            
            # Certifications
            if analysis['extracted_skills']['certifications']:
                st.markdown("**🏆 Certifications Found:**")
                cert_text = ", ".join([cert['certification'] for cert in analysis['extracted_skills']['certifications']])
                st.markdown(cert_text)
            
            # Top 3 Career Fits
            st.markdown("### 🎯 Top Career Matches")
            
            top_careers = analysis['career_fits'][:3]  # Top 3 only
            
            for i, career in enumerate(top_careers):
                with st.expander(f"#{i+1} {career['career']} - {career['fit_score']}% Match", expanded=i==0):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**📊 Fit Analysis:**")
                        st.metric("Overall Fit", f"{career['fit_score']}%")
                        st.metric("Required Skills Fit", f"{career['required_fit']}%")
                        st.metric("Optional Skills Fit", f"{career['optional_fit']}%")
                        
                        # Matched Skills
                        if career['matched_skills']['required']:
                            st.markdown("**✅ Required Skills Matched:**")
                            for skill in career['matched_skills']['required'][:3]:
                                st.markdown(f"- {skill}")
                        
                        if career['matched_skills']['optional']:
                            st.markdown("**✅ Optional Skills Matched:**")
                            for skill in career['matched_skills']['optional'][:3]:
                                st.markdown(f"- {skill}")
                    
                    with col2:
                        # Missing Required Skills (High Priority)
                        if career['missing_skills']['required']:
                            st.markdown("**🚨 Critical Missing Skills:**")
                            for skill in career['missing_skills']['required'][:3]:
                                importance = skill['importance']
                                priority = "🔴 High" if importance >= 8 else "🟡 Medium"
                                st.markdown(f"- {skill['skill']} ({priority} Priority)")
                        
                        # Missing Optional Skills
                        if career['missing_skills']['optional']:
                            st.markdown("**💡 Optional Skills to Consider:**")
                            for skill in career['missing_skills']['optional'][:3]:
                                st.markdown(f"- {skill['skill']} (Nice to have)")
                        
                        # Skill Progress
                        required_progress = career['skill_counts']['required_matched'] / max(career['skill_counts']['required_total'], 1)
                        optional_progress = career['skill_counts']['optional_matched'] / max(career['skill_counts']['optional_total'], 1)
                        
                        st.markdown("**📈 Skill Coverage:**")
                        st.progress(required_progress, text=f"Required: {career['skill_counts']['required_matched']}/{career['skill_counts']['required_total']}")
                        st.progress(optional_progress, text=f"Optional: {career['skill_counts']['optional_matched']}/{career['skill_counts']['optional_total']}")
            
            # Improvement Suggestions
            st.markdown("### 💡 Improvement Suggestions")
            
            suggestions = analysis['improvement_suggestions']
            
            if suggestions['critical']:
                st.markdown("**🚨 Critical Improvements:**")
                for suggestion in suggestions['critical']:
                    st.error(f"• {suggestion}")
            
            if suggestions['important']:
                st.markdown("**⚠️ Important Improvements:**")
                for suggestion in suggestions['important']:
                    st.warning(f"• {suggestion}")
            
            if suggestions['nice_to_have']:
                st.markdown("**💡 Nice to Have:**")
                for suggestion in suggestions['nice_to_have']:
                    st.info(f"• {suggestion}")
            
            # ATS Optimization Tips
            st.markdown("### 🎯 ATS Optimization Tips")
            
            breakdown = analysis['ats_score']['breakdown']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📈 Strengths:**")
                if breakdown['technical_skills_found'] >= 5:
                    st.success("✅ Good technical skills coverage")
                if breakdown['action_verbs_found'] >= 3:
                    st.success("✅ Uses action verbs effectively")
                if breakdown['quantification_instances'] >= 2:
                    st.success("✅ Includes quantifiable achievements")
            
            with col2:
                st.markdown("**🔧 Areas to Improve:**")
                if breakdown['technical_skills_found'] < 5:
                    st.warning("⚠️ Add more technical skills")
                if breakdown['action_verbs_found'] < 3:
                    st.warning("⚠️ Use more action verbs (achieved, implemented, optimized)")
                if breakdown['quantification_instances'] < 2:
                    st.warning("⚠️ Add numbers and percentages to show impact")
                if breakdown['avg_sentence_length'] > 25:
                    st.warning("⚠️ Shorten sentences for better readability")
            
        else:
            st.error("Please provide resume content to analyze!")

def show_chatbot_page(pipeline):
    """Display the AI chatbot page"""
    st.markdown("## 🤖 AI Career Chatbot")
    st.markdown("Ask me anything about careers, skills, learning paths, or job market insights!")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about careers, skills, or learning paths..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = pipeline.chatbot_response(prompt)
            
            # Display response
            st.markdown(response['answer'])
            
            # Show confidence if available
            if response['confidence'] > 0:
                st.caption(f"Confidence: {response['confidence']}% | Category: {response['category']}")
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response['answer']})
    
    # Sidebar with example questions
    with st.sidebar:
        st.markdown("### 💡 Example Questions:")
        
        example_questions = [
            "Which career suits me if I love AI?",
            "How do I start to become a Software Engineer?",
            "What skills do I need for Data Science?",
            "Is a degree necessary for tech careers?",
            "How much can I earn as a Data Engineer?",
            "What's the difference between Data Scientist and Data Analyst?",
            "How do I transition from non-tech to tech?",
            "What programming language should I learn first?"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{question}"):
                # Add example question to chat
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

def show_roadmap_page(pipeline):
    """Display the career roadmap visualization page"""
    st.markdown("## 🗺️ Career Roadmap Visualization")
    st.markdown("Visualize your journey from current skills to your target career!")
    
    # Get available careers
    careers = pipeline.career_skills_df['career'].unique().tolist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # User skills input
        user_skills_input = st.text_area(
            "Enter your current skills (one per line or comma-separated):",
            height=120,
            placeholder="Python\nSQL\nMachine Learning"
        )
        
        # Target career selection
        target_career = st.selectbox(
            "Select your target career:",
            ["Select a career..."] + careers
        )
    
    with col2:
        st.markdown("### 🗺️ Roadmap Features:")
        st.markdown("""
        - **Current Skills** → What you have now
        - **Missing Skills** → What you need to learn
        - **Learning Path** → How to get there
        - **Target Career** → Your end goal
        - **Timeline** → Estimated completion time
        """)
    
    if st.button("Generate Roadmap", type="primary"):
        if user_skills_input and target_career != "Select a career...":
            # Parse skills
            if "\n" in user_skills_input:
                skills_list = [skill.strip() for skill in user_skills_input.split("\n") if skill.strip()]
            else:
                skills_list = [skill.strip() for skill in user_skills_input.split(",") if skill.strip()]
            
            if skills_list:
                with st.spinner("Creating your career roadmap..."):
                    # Get gap analysis and learning path
                    gap_analysis = pipeline.gap_analysis(skills_list, target_career)
                    learning_path = pipeline.get_learning_path(target_career, skills_list)
                
                if "error" not in gap_analysis and "error" not in learning_path:
                    st.success(f"Roadmap generated for {target_career}!")
                    
                    # Roadmap visualization
                    st.markdown("### 🗺️ Your Career Roadmap")
                    
                    # Create a visual roadmap
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown("### 🎯 Current State")
                        st.markdown(f"**Skills:** {len(skills_list)}")
                        st.markdown(f"**Readiness:** {gap_analysis['completion_percentage']}%")
                        
                        # Current skills
                        for skill in skills_list[:5]:
                            st.markdown(f"✅ {skill}")
                        if len(skills_list) > 5:
                            st.markdown(f"... and {len(skills_list) - 5} more")
                    
                    with col2:
                        st.markdown("### ❌ Missing Skills")
                        missing_count = len(gap_analysis['required_missing'])
                        st.markdown(f"**Required:** {missing_count}")
                        
                        for skill in gap_analysis['required_missing'][:3]:
                            st.markdown(f"🔴 {skill['skill']}")
                        if missing_count > 3:
                            st.markdown(f"... and {missing_count - 3} more")
                    
                    with col3:
                        st.markdown("### 📚 Learning Path")
                        phases = len(learning_path['phases'])
                        st.markdown(f"**Phases:** {phases}")
                        
                        for i, phase in enumerate(learning_path['phases'][:2]):
                            st.markdown(f"🟡 Phase {i+1}: {phase['name']}")
                        if phases > 2:
                            st.markdown(f"... and {phases - 2} more phases")
                    
                    with col4:
                        st.markdown("### 🎯 Target Career")
                        st.markdown(f"**{target_career}**")
                        
                        # Get job insights
                        insights = pipeline.get_job_market_insights(target_career)
                        if "error" not in insights:
                            if "salary_range" in insights and "avg" in insights["salary_range"]:
                                st.markdown(f"💰 ${insights['salary_range']['avg']:,}")
                            else:
                                st.markdown("💰 Not available")
                            if "demand_index" in insights:
                                st.markdown(f"📈 {insights['demand_index']}/100 demand")
                            else:
                                st.markdown("📈 Demand data not available")
                    
                    # Progress timeline
                    st.markdown("### ⏱️ Progress Timeline")
                    
                    # Create a timeline visualization
                    timeline_data = []
                    current_phase = 0
                    
                    for i, phase in enumerate(learning_path['phases']):
                        if phase['skills']:
                            timeline_data.append({
                                'Phase': f"Phase {i+1}",
                                'Name': phase['name'],
                                'Level': phase['level'],
                                'Skills_Count': len(phase['skills']),
                                'Estimated_Hours': sum(course.get('duration_hours', 0) for course in phase.get('courses', []))
                            })
                    
                    if timeline_data:
                        df_timeline = pd.DataFrame(timeline_data)
                        
                        # Create timeline chart
                        fig = px.bar(
                            df_timeline,
                            x='Phase',
                            y='Estimated_Hours',
                            color='Level',
                            title="Learning Timeline by Phase",
                            color_discrete_map={
                                'Beginner': '#28a745',
                                'Intermediate': '#ffc107',
                                'Advanced': '#dc3545'
                            }
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Detailed roadmap steps
                    st.markdown("### 📋 Detailed Roadmap Steps")
                    
                    step_number = 1
                    for i, phase in enumerate(learning_path['phases']):
                        if phase['skills']:
                            with st.expander(f"Step {step_number}: {phase['name']} ({phase['level']})", expanded=i==0):
                                st.markdown(f"**Focus:** {phase['level']} level skills for {target_career}")
                                
                                # Skills to learn
                                st.markdown("**Skills to Learn:**")
                                for skill in phase['skills']:
                                    difficulty_color = {
                                        'Beginner': '🟢',
                                        'Intermediate': '🟡',
                                        'Advanced': '🔴'
                                    }
                                    st.markdown(f"{difficulty_color.get(skill['difficulty'], '⚪')} {skill['skill']}")
                                
                                # Courses
                                if 'courses' in phase and phase['courses']:
                                    st.markdown("**Recommended Courses:**")
                                    for course in phase['courses']:
                                        st.markdown(f"📖 {course['title']} ({course['platform']}) - {course['duration_hours']}h")
                                
                                # Estimated time
                                total_hours = sum(course.get('duration_hours', 0) for course in phase.get('courses', []))
                                if total_hours > 0:
                                    st.markdown(f"**Estimated Time:** {total_hours} hours ({total_hours // 10} weeks at 10h/week)")
                                
                                step_number += 1
                    
                    # Success metrics
                    st.markdown("### 🎯 Success Metrics")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Current Readiness",
                            f"{gap_analysis['completion_percentage']}%",
                            delta=f"{gap_analysis['completion_percentage'] - 50:.1f}%"
                        )
                    
                    with col2:
                        total_hours = sum(
                            sum(course.get('duration_hours', 0) for course in phase.get('courses', []))
                            for phase in learning_path['phases']
                        )
                        st.metric(
                            "Total Study Time",
                            f"{total_hours}h",
                            delta=f"{total_hours // 10} weeks"
                        )
                    
                    with col3:
                        st.metric(
                            "Skills to Learn",
                            len(gap_analysis['required_missing']),
                            delta=f"-{len(gap_analysis['required_missing'])}"
                        )
                    
                    # Action plan
                    st.markdown("### 🚀 Your Action Plan")
                    st.markdown("1. **Start with Phase 1** - Focus on foundation skills")
                    st.markdown("2. **Set weekly goals** - Aim for 10 hours of study per week")
                    st.markdown("3. **Practice regularly** - Apply skills in real projects")
                    st.markdown("4. **Track progress** - Monitor your skill development")
                    st.markdown("5. **Network** - Connect with professionals in your target field")
                    
                else:
                    st.error("Error generating roadmap. Please check your inputs.")
            else:
                st.error("Please enter at least one skill!")
        else:
            st.error("Please enter your skills and select a target career!")

def show_peer_benchmarking_page(pipeline):
    """Display the AI Career Benchmarking Assistant page"""
    st.markdown("## 🤖 AI Career Benchmarking Assistant")
    st.markdown("Get structured analysis comparing your skills against realistic peer data with personalized recommendations!")
    
    # Load AI benchmarking assistant
    ai_assistant = load_ai_benchmarking_assistant()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # User skills input
        user_skills_input = st.text_area(
            "Enter your current skills (one per line or comma-separated):",
            height=120,
            placeholder="Python\nSQL\nMachine Learning\nStatistics"
        )
        
        # Target career selection
        target_career = st.selectbox(
            "Select your target career:",
            ["Select a career..."] + ["Data Scientist", "ML Engineer", "Data Analyst", "Software Engineer"]
        )
        
        # Optional experience input
        user_experience = st.number_input(
            "Years of experience (optional - will be estimated if not provided):",
            min_value=0,
            max_value=20,
            value=0,
            help="Leave as 0 to auto-estimate based on your skills"
        )
    
    with col2:
        st.markdown("### 🎯 AI Analysis Features:")
        st.markdown("""
        - **Structured Workflow** - 6-step systematic analysis
        - **Realistic Peer Data** - 5-10 unique peer profiles
        - **Percentile Rankings** - Experience, skills, salary estimates
        - **Skills Gap Analysis** - Core vs emerging skills categorization
        - **Visual Analytics** - Progress bars, charts, metrics
        - **Personalized Recommendations** - Priority actions & next steps
        """)
    
    if st.button("🚀 Run AI Career Analysis", type="primary"):
        if user_skills_input and target_career != "Select a career...":
            # Parse skills
            if "\n" in user_skills_input:
                skills_list = [skill.strip() for skill in user_skills_input.split("\n") if skill.strip()]
            else:
                skills_list = [skill.strip() for skill in user_skills_input.split(",") if skill.strip()]
            
            if skills_list:
                with st.spinner("🤖 Running AI career benchmarking analysis..."):
                    # Use None for experience if 0 (auto-estimate)
                    exp_input = user_experience if user_experience > 0 else None
                    analysis = ai_assistant.analyze_career_benchmarking(skills_list, target_career, exp_input)
                
                if "error" not in analysis:
                    st.success(f"✅ AI analysis complete for {target_career}!")
                    
                    sections = analysis['analysis_sections']
                    
                    # 🎯 Your Position Among Peers
                    st.markdown(f"### {sections['user_position']['title']}")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    metrics = sections['user_position']['metrics']
                    
                    with col1:
                        coverage = metrics['skill_coverage']
                        st.metric(
                            coverage['label'],
                            f"{coverage['value']:.1f}%",
                            delta=f"{coverage['value'] - coverage['benchmark']:.1f}% vs target"
                        )
                        st.progress(coverage['value'] / 100)
                    
                    with col2:
                        exp_rank = metrics['experience_rank']
                        st.metric(
                            exp_rank['label'],
                            f"{exp_rank['value']:.0f}th percentile",
                            delta=f"{exp_rank['value'] - exp_rank['benchmark']:.0f} vs median"
                        )
                        st.progress(exp_rank['value'] / 100)
                    
                    with col3:
                        skill_rank = metrics['skill_count_rank']
                        st.metric(
                            skill_rank['label'],
                            f"{skill_rank['value']:.0f}th percentile",
                            delta=f"{skill_rank['value'] - skill_rank['benchmark']:.0f} vs median"
                        )
                        st.progress(skill_rank['value'] / 100)
                    
                    with col4:
                        salary = metrics['salary_estimate']
                        st.metric(
                            salary['label'],
                            f"${salary['value']:,}",
                            delta=f"${salary['value'] - salary['benchmark']:,} vs median"
                        )
                    
                    # 📊 Peer Market Statistics
                    st.markdown(f"### {sections['market_statistics']['title']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Market Averages")
                        peer_stats = sections['market_statistics']['peer_averages']
                        st.metric("Average Experience", f"{peer_stats['avg_experience']:.1f} years")
                        st.metric("Average Salary", f"${peer_stats['avg_salary']:,}")
                        st.metric("Average Skills", f"{peer_stats['avg_skill_count']:.1f}")
                        st.metric("Sample Size", f"{peer_stats['total_peers']} peers")
                    
                    with col2:
                        st.markdown("#### Your Profile")
                        your_stats = sections['market_statistics']['your_stats']
                        st.metric("Your Experience", f"{your_stats['experience']} years")
                        st.metric("Your Estimated Salary", f"${your_stats['estimated_salary']:,}")
                        st.metric("Your Skills", f"{your_stats['skill_count']}")
                        
                        # Market position indicator
                        coverage_pct = metrics['skill_coverage']['value']
                        if coverage_pct >= 80:
                            st.success("🎯 Strong market position")
                        elif coverage_pct >= 60:
                            st.warning("📈 Developing position")
                        else:
                            st.error("🚨 Needs improvement")
                    
                    # 🎯 Skills Analysis
                    st.markdown(f"### {sections['skills_analysis']['title']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Missing Skills by Priority")
                        
                        core_missing = sections['skills_analysis']['missing_core_skills']
                        if core_missing:
                            st.markdown("**🔴 Core Skills (Critical)**")
                            for skill in core_missing:
                                st.markdown(f"• {skill}")
                        
                        emerging_missing = sections['skills_analysis']['missing_emerging_skills']
                        if emerging_missing:
                            st.markdown("**🟡 Emerging Skills (Important)**")
                            for skill in emerging_missing:
                                st.markdown(f"• {skill}")
                        
                        if not core_missing and not emerging_missing:
                            st.success("🎉 You have all key skills!")
                    
                    with col2:
                        st.markdown("#### Skills You Have")
                        
                        common_skills = sections['skills_analysis']['common_skills_you_have']
                        if common_skills:
                            st.markdown("**✅ Market-Relevant Skills**")
                            for skill in common_skills[:8]:
                                st.markdown(f"• {skill.title()}")
                        
                        # Coverage details
                        coverage_details = sections['skills_analysis']['skill_coverage_details']
                        st.markdown("**📊 Coverage Summary**")
                        st.markdown(f"• Skills in common: {coverage_details['skills_in_common']}")
                        st.markdown(f"• Total market skills: {coverage_details['total_market_skills']}")
                        st.markdown(f"• Coverage: {coverage_details['coverage_percentage']:.1f}%")
                    
                    # 👥 Sample Peer Profiles
                    st.markdown(f"### {sections['peer_profiles']['title']}")
                    
                    for i, peer in enumerate(sections['peer_profiles']['profiles']):
                        with st.expander(f"Peer #{i+1} - {peer['experience_years']} years, {peer['education']}, ${peer['salary']:,}"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown(f"**Experience:** {peer['experience_years']} years")
                                st.markdown(f"**Education:** {peer['education']}")
                                st.markdown(f"**Salary:** ${peer['salary']:,}")
                            
                            with col2:
                                overlap_pct = peer['skill_overlap_percentage']
                                st.markdown(f"**Skill Overlap:** {overlap_pct:.1f}%")
                                st.progress(overlap_pct / 100)
                                st.markdown(f"**Total Skills:** {peer['skill_count']}")
                            
                            with col3:
                                st.markdown("**Key Skills:**")
                                user_skills_lower = [s.lower() for s in skills_list]
                                for skill in peer['top_skills']:
                                    if skill.lower() in user_skills_lower:
                                        st.markdown(f"✅ {skill}")
                                    else:
                                        st.markdown(f"❌ {skill}")
                    
                    # 💡 Personalized Recommendations
                    st.markdown(f"### {sections['recommendations']['title']}")
                    
                    recommendations = sections['recommendations']['priority_actions']
                    
                    for rec in recommendations:
                        if rec['priority'] == 'critical':
                            st.error(f"**{rec['icon']} {rec['title']}**")
                        elif rec['priority'] == 'high':
                            st.warning(f"**{rec['icon']} {rec['title']}**")
                        else:
                            st.info(f"**{rec['icon']} {rec['title']}**")
                        
                        st.markdown(f"**Analysis:** {rec['action']}")
                        st.markdown(f"**Next Steps:** {rec['next_steps']}")
                        st.markdown("---")
                    
                else:
                    st.error(f"❌ Analysis failed: {analysis.get('error', 'Unknown error')}")
            else:
                st.error("Please enter at least one skill!")
        else:
            st.error("Please enter your skills and select a target career!")

def show_recommendations_page(pipeline):
    """Display the personalized recommendations page"""
    st.markdown("## 🔮 Personalized Recommendation Engine")
    st.markdown("Get personalized career recommendations, job matches, and learning suggestions!")
    
    # Get available careers
    careers = pipeline.career_skills_df['career'].unique().tolist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # User skills input
        user_skills_input = st.text_area(
            "Enter your current skills (one per line or comma-separated):",
            height=120,
            placeholder="Python\nSQL\nMachine Learning\nStatistics"
        )
        
        # User preferences
        st.markdown("### 🎯 Your Preferences")
        
        col_pref1, col_pref2 = st.columns(2)
        
        with col_pref1:
            experience_level = st.selectbox(
                "Experience Level:",
                ["Entry Level", "Mid Level", "Senior Level", "Lead Level"]
            )
            
            work_type = st.selectbox(
                "Preferred Work Type:",
                ["Full-time", "Contract", "Part-time", "Remote", "Any"]
            )
        
        with col_pref2:
            salary_range = st.selectbox(
                "Salary Range:",
                ["$50K-75K", "$75K-100K", "$100K-125K", "$125K-150K", "$150K+", "Any"]
            )
            
            location = st.selectbox(
                "Preferred Location:",
                ["Any", "United States", "United Kingdom", "Germany", "Canada", "Remote"]
            )
    
    with col2:
        st.markdown("### 🎯 What you'll get:")
        st.markdown("""
        - **Career Matches** - Best-fit career paths
        - **Job Opportunities** - Matching job postings
        - **Learning Recommendations** - Personalized courses
        - **Skill Suggestions** - Skills to develop
        - **Portfolio Projects** - Project ideas
        - **Networking Tips** - How to connect
        """)
    
    if st.button("Get Personalized Recommendations", type="primary"):
        if user_skills_input:
            # Parse skills
            if "\n" in user_skills_input:
                skills_list = [skill.strip() for skill in user_skills_input.split("\n") if skill.strip()]
            else:
                skills_list = [skill.strip() for skill in user_skills_input.split(",") if skill.strip()]
            
            if skills_list:
                with st.spinner("Generating personalized recommendations..."):
                    # Get career matches
                    career_matches = pipeline.skill_matching(skills_list)
                    
                    # Get job matches
                    job_matches = []
                    for career in [match['career'] for match in career_matches[:3]]:
                        jobs = pipeline.job_posts_df[
                            pipeline.job_posts_df['title'].str.contains(career, case=False, na=False)
                        ].head(2)
                        job_matches.extend(jobs.to_dict('records'))
                
                st.success("Personalized recommendations generated!")
                
                # Career recommendations
                st.markdown("### 🎯 Top Career Recommendations")
                
                for i, match in enumerate(career_matches[:3]):
                    with st.expander(f"#{i+1} {match['career']} - {match['match_percentage']}% Match"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**✅ Your Strengths:**")
                            for skill in match['matched_skills']:
                                st.markdown(f"- {skill}")
                        
                        with col2:
                            st.markdown("**📚 Skills to Develop:**")
                            # Handle missing_skills as dictionary with categories
                            missing_skills_list = []
                            if isinstance(match['missing_skills'], dict):
                                for category, skills in match['missing_skills'].items():
                                    if isinstance(skills, list):
                                        missing_skills_list.extend([s['skill'] if isinstance(s, dict) else s for s in skills])
                                    else:
                                        missing_skills_list.extend(skills)
                            else:
                                missing_skills_list = match['missing_skills']
                            
                            for skill in missing_skills_list[:5]:
                                st.markdown(f"- {skill}")
                        
                        # Get job market insights
                        insights = pipeline.get_job_market_insights(match['career'])
                        if "error" not in insights:
                            if "salary_range" in insights and "avg" in insights["salary_range"]:
                                st.markdown(f"**💰 Average Salary:** ${insights['salary_range']['avg']:,}")
                            else:
                                st.markdown("**💰 Average Salary:** Not available")
                            if "demand_index" in insights:
                                st.markdown(f"**📈 Market Demand:** {insights['demand_index']}/100")
                            else:
                                st.markdown("**📈 Market Demand:** Not available")
                
                # Job opportunities
                if job_matches:
                    st.markdown("### 💼 Matching Job Opportunities")
                    
                    for job in job_matches[:5]:
                        with st.expander(f"📋 {job['title']} at {job['company']}"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown(f"**Location:** {job['location']}")
                                st.markdown(f"**Type:** {job['job_type']}")
                            
                            with col2:
                                st.markdown(f"**Experience:** {job['experience_level']}")
                                st.markdown(f"**Salary:** ${job['min_salary']:,} - ${job['max_salary']:,}")
                            
                            with col3:
                                st.markdown(f"**Posted:** {job['posted_date']}")
                                if st.button(f"Apply", key=f"apply_{job['job_id']}"):
                                    st.markdown(f"🔗 [Apply Here]({job['url']})")
                            
                            # Calculate job match
                            job_skills = [s.strip().lower() for s in job['required_skills'].split(',')]
                            user_skill_lower = [s.lower() for s in skills_list]
                            job_match = len(set(job_skills) & set(user_skill_lower)) / len(job_skills) * 100
                            
                            st.markdown(f"**🎯 Job Match:** {job_match:.1f}%")
                            st.markdown(f"**Required Skills:** {job['required_skills']}")
                
                # Learning recommendations
                st.markdown("### 📚 Learning Recommendations")
                
                # Get courses for top missing skills
                all_missing_skills = []
                for match in career_matches[:2]:
                    # Handle missing_skills as dictionary with categories
                    missing_skills_list = []
                    if isinstance(match['missing_skills'], dict):
                        for category, skills in match['missing_skills'].items():
                            if isinstance(skills, list):
                                missing_skills_list.extend([s['skill'] if isinstance(s, dict) else s for s in skills])
                            else:
                                missing_skills_list.extend(skills)
                    else:
                        missing_skills_list = match['missing_skills']
                    
                    all_missing_skills.extend(missing_skills_list[:3])
                
                if all_missing_skills:
                    # Get courses for these skills
                    recommended_courses = pipeline.courses_df[
                        pipeline.courses_df['skill'].isin(all_missing_skills)
                    ].head(6)
                    
                    if not recommended_courses.empty:
                        for idx, course in recommended_courses.iterrows():
                            with st.container():
                                st.markdown(f"**📖 {course['title']}**")
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.markdown(f"Platform: {course['platform']}")
                                    st.markdown(f"Skill: {course['skill']}")
                                
                                with col2:
                                    st.markdown(f"Level: {course['level']}")
                                    st.markdown(f"Duration: {course['duration_hours']}h")
                                
                                with col3:
                                    st.markdown(f"Rating: {course['rating']}⭐")
                                    st.markdown(f"Price: ${course['price']}")
                                
                                if st.button(f"View Course", key=f"rec_course_{idx}_{course['platform']}_{course['skill']}"):
                                    st.markdown(f"🔗 [Course Link]({course['url']})")
                
                # Portfolio project suggestions
                st.markdown("### 🛠️ Portfolio Project Suggestions")
                
                project_ideas = [
                    {
                        "title": "Data Analysis Dashboard",
                        "description": "Create an interactive dashboard using Python, SQL, and visualization tools",
                        "skills": ["Python", "SQL", "Data Visualization", "Dashboard"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "title": "Machine Learning Model",
                        "description": "Build and deploy a machine learning model with real-world data",
                        "skills": ["Python", "Machine Learning", "Data Science", "Deployment"],
                        "difficulty": "Advanced"
                    },
                    {
                        "title": "Web Application",
                        "description": "Develop a full-stack web application with modern technologies",
                        "skills": ["JavaScript", "React", "Node.js", "Database"],
                        "difficulty": "Intermediate"
                    },
                    {
                        "title": "API Development",
                        "description": "Create RESTful APIs with authentication and documentation",
                        "skills": ["Python", "API", "Authentication", "Documentation"],
                        "difficulty": "Intermediate"
                    }
                ]
                
                # Filter projects based on user skills
                relevant_projects = []
                for project in project_ideas:
                    project_skills = [s.lower() for s in project['skills']]
                    user_skills_lower = [s.lower() for s in skills_list]
                    overlap = len(set(project_skills) & set(user_skills_lower))
                    if overlap > 0:
                        relevant_projects.append((project, overlap))
                
                # Sort by relevance
                relevant_projects.sort(key=lambda x: x[1], reverse=True)
                
                for project, relevance in relevant_projects[:3]:
                    with st.expander(f"🛠️ {project['title']} (Relevance: {relevance} skills)"):
                        st.markdown(f"**Description:** {project['description']}")
                        st.markdown(f"**Difficulty:** {project['difficulty']}")
                        st.markdown(f"**Skills Used:** {', '.join(project['skills'])}")
                        
                        # Check which skills user has
                        user_has = [skill for skill in project['skills'] if skill.lower() in [s.lower() for s in skills_list]]
                        user_needs = [skill for skill in project['skills'] if skill.lower() not in [s.lower() for s in skills_list]]
                        
                        if user_has:
                            st.markdown(f"**✅ Skills you have:** {', '.join(user_has)}")
                        if user_needs:
                            st.markdown(f"**📚 Skills to learn:** {', '.join(user_needs)}")
                
                # Networking recommendations
                st.markdown("### 🤝 Networking Recommendations")
                
                networking_tips = [
                    f"Join {career_matches[0]['career']} communities on LinkedIn and Reddit",
                    "Attend local tech meetups and conferences",
                    "Connect with professionals in your target field",
                    "Participate in online forums and discussions",
                    "Contribute to open source projects",
                    "Share your learning journey on social media"
                ]
                
                for tip in networking_tips:
                    st.markdown(f"💡 {tip}")
                
                # Action plan
                st.markdown("### 🚀 Your Action Plan")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Immediate Actions (Next 30 days):**")
                    st.markdown("1. Start learning top missing skills")
                    st.markdown("2. Apply to 2-3 relevant job postings")
                    st.markdown("3. Begin a portfolio project")
                    st.markdown("4. Update your LinkedIn profile")
                
                with col2:
                    st.markdown("**Long-term Goals (Next 6 months):**")
                    st.markdown("1. Complete learning path for target career")
                    st.markdown("2. Build 2-3 portfolio projects")
                    st.markdown("3. Network with 50+ professionals")
                    st.markdown("4. Apply to 20+ job opportunities")
                
            else:
                st.error("Please enter at least one skill!")
        else:
            st.error("Please enter your skills first!")

if __name__ == "__main__":
    main()
