import streamlit as st
import json
import os
import tempfile
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Add the backend to the path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend import ResumeAnalyzer
from backend.utils import format_contact_info, get_skill_category_icon, get_priority_color, format_score, truncate_text, save_results_csv

# Page configuration
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .career-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .skill-tag {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        margin: 0.1rem;
        display: inline-block;
    }
    .suggestion-card {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
        margin-bottom: 1rem;
    }
    .strength-card {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📄 Resume Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### AI-Powered Resume Analysis & Career Fit Assessment")
    
    # Initialize analyzer
    @st.cache_resource
    def get_analyzer():
        return ResumeAnalyzer()
    
    analyzer = get_analyzer()
    
    # Sidebar
    st.sidebar.title("📋 Options")
    
    # Input method selection
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["📁 Upload File", "📝 Paste Text", "🧪 Sample Analysis"]
    )
    
    top_careers = st.sidebar.slider("Number of top career matches:", 3, 10, 5)
    
    # Main content area
    if input_method == "📁 Upload File":
        show_file_upload(analyzer, top_careers)
    elif input_method == "📝 Paste Text":
        show_text_input(analyzer, top_careers)
    else:
        show_sample_analysis(analyzer, top_careers)

def show_file_upload(analyzer, top_careers):
    """Show file upload interface"""
    st.header("📁 Upload Resume")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a resume file",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT (max 200MB)"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.info(f"📄 **File:** {uploaded_file.name} ({file_size_mb:.1f} MB)")
        
        # Add analyze button
        if st.button("🔍 Analyze Uploaded Resume", type="primary"):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # Analyze resume
                with st.spinner("🔍 Analyzing your resume..."):
                    results = analyzer.analyze_resume_file(tmp_file_path, top_careers)
                
                # Clean up temporary file
                os.unlink(tmp_file_path)
                
                # Display results
                if results.get('success'):
                    display_results(results, analyzer)
                else:
                    st.error(f"❌ Analysis failed: {results.get('error', 'Unknown error')}")
                    
                    # Offer fallback to paste text
                    st.warning("💡 **File parsing failed. You can try pasting the text content instead.**")
                    st.info("Switch to '📝 Paste Text' tab to manually enter your resume content.")
                    
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.warning("💡 **File processing failed. You can try pasting the text content instead.**")
                st.info("Switch to '📝 Paste Text' tab to manually enter your resume content.")

def show_text_input(analyzer, top_careers):
    """Show text input interface"""
    st.header("📝 Paste Resume Text")
    
    # Text area
    resume_text = st.text_area(
        "Paste your resume text here:",
        height=300,
        placeholder="Paste your resume content here..."
    )
    
    # Analyze button
    if st.button("🔍 Analyze Resume", type="primary"):
        if resume_text.strip():
            with st.spinner("🔍 Analyzing your resume..."):
                results = analyzer.analyze_resume_text(resume_text, top_careers)
            
            if results.get('success'):
                display_results(results, analyzer)
            else:
                st.error(f"❌ Analysis failed: {results.get('error', 'Unknown error')}")
        else:
            st.warning("⚠️ Please enter some resume text to analyze.")

def show_sample_analysis(analyzer, top_careers):
    """Show sample analysis"""
    st.header("🧪 Sample Analysis")
    st.info("This will analyze a sample resume to demonstrate the tool's capabilities.")
    
    if st.button("🔍 Run Sample Analysis", type="primary"):
        with st.spinner("🔍 Running sample analysis..."):
            results = analyzer.run_sample_analysis()
        
        if results.get('success'):
            display_results(results, analyzer)
        else:
            st.error(f"❌ Sample analysis failed: {results.get('error', 'Unknown error')}")

def display_results(results, analyzer):
    """Display analysis results"""
    st.success("✅ Analysis completed successfully!")
    
    # Summary metrics
    display_summary_metrics(results)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Career Fit", 
        "💼 Extracted Skills", 
        "📊 Resume Score", 
        "📄 Parsed Content",
        "💾 Export Results"
    ])
    
    with tab1:
        display_career_fit(results)
    
    with tab2:
        display_extracted_skills(results)
    
    with tab3:
        display_resume_score(results)
    
    with tab4:
        display_parsed_content(results)
    
    with tab5:
        display_export_options(results, analyzer)

def display_summary_metrics(results):
    """Display summary metrics"""
    st.subheader("📊 Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        skills_summary = results.get('skills_summary', {})
        st.metric(
            "Total Skills", 
            skills_summary.get('total_skills', 0)
        )
    
    with col2:
        career_analysis = results.get('career_analysis', [])
        if career_analysis:
            st.metric(
                "Top Career Match", 
                career_analysis[0]['career']
            )
        else:
            st.metric("Top Career Match", "N/A")
    
    with col3:
        resume_score = results.get('resume_score', {})
        st.metric(
            "Resume Score", 
            f"{resume_score.get('overall_score', 0):.1f}/100"
        )
    
    with col4:
        file_info = results.get('file_info', {})
        st.metric(
            "Word Count", 
            file_info.get('word_count', 0)
        )

def display_career_fit(results):
    """Display career fit analysis"""
    st.subheader("🎯 Career Fit Analysis")
    
    career_analysis = results.get('career_analysis', [])
    career_recommendations = results.get('career_recommendations', {})
    
    if not career_analysis:
        st.warning("No career analysis available.")
        return
    
    # Top career match
    top_career = career_analysis[0]
    
    # Career match chart
    careers = [career['career'] for career in career_analysis]
    scores = [career['overall_score'] for career in career_analysis]
    
    fig = px.bar(
        x=careers, 
        y=scores,
        title="Career Match Scores",
        labels={'x': 'Career', 'y': 'Match Score (%)'},
        color=scores,
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Top career details
    st.markdown("### 🏆 Best Career Match")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        **{top_career['career']}**  
        {top_career['description']}
        """)
        
        # Progress bars
        st.markdown("**Required Skills Coverage:**")
        st.progress(top_career['required_coverage'] / 100)
        st.caption(f"{top_career['required_coverage']:.1f}% ({top_career['matched_required']}/{top_career['total_required']})")
        
        st.markdown("**Optional Skills Coverage:**")
        st.progress(top_career['optional_coverage'] / 100)
        st.caption(f"{top_career['optional_coverage']:.1f}% ({top_career['matched_optional']}/{top_career['total_optional']})")
    
    with col2:
        st.metric("Overall Score", f"{top_career['overall_score']:.1f}%")
        st.metric("Required Skills", f"{top_career['matched_required']}/{top_career['total_required']}")
        st.metric("Optional Skills", f"{top_career['matched_optional']}/{top_career['total_optional']}")
    
    # Matched skills
    st.markdown("### ✅ Matched Skills")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Required Skills:**")
        for skill in top_career['required_matches']:
            st.markdown(f"• {skill['skill']} (Importance: {skill['importance']}/10)")
    
    with col2:
        st.markdown("**Optional Skills:**")
        for skill in top_career['optional_matches']:
            st.markdown(f"• {skill['skill']} (Importance: {skill['importance']}/10)")
    
    # Missing skills
    st.markdown("### ❌ Missing Skills")
    
    skill_gaps = top_career.get('skill_gaps', {})
    
    if skill_gaps.get('critical_gaps'):
        st.markdown("**🔴 Critical Gaps (High Priority):**")
        for skill in skill_gaps['critical_gaps']:
            st.markdown(f"• {skill['skill']} (Importance: {skill['importance']}/10)")
    
    if skill_gaps.get('important_gaps'):
        st.markdown("**🟡 Important Gaps (Medium Priority):**")
        for skill in skill_gaps['important_gaps']:
            st.markdown(f"• {skill['skill']} (Importance: {skill['importance']}/10)")
    
    if skill_gaps.get('nice_to_have'):
        st.markdown("**🟢 Nice to Have (Low Priority):**")
        for skill in skill_gaps['nice_to_have']:
            st.markdown(f"• {skill['skill']} (Importance: {skill['importance']}/10)")
    
    # Career recommendations
    if career_recommendations:
        st.markdown("### 💡 Career Recommendations")
        
        for rec in career_recommendations.get('recommendations', []):
            priority_color = get_priority_color(rec['priority'])
            st.markdown(f"""
            <div class="suggestion-card">
                <strong>{rec['type'].replace('_', ' ').title()}</strong><br>
                {rec['message']}<br>
                <small>Priority: <span style="color: {priority_color};">{rec['priority'].title()}</span></small>
            </div>
            """, unsafe_allow_html=True)

def display_extracted_skills(results):
    """Display extracted skills"""
    st.subheader("💼 Extracted Skills")
    
    extracted_skills = results.get('extracted_skills', {})
    skills_summary = results.get('skills_summary', {})
    
    # Skills summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Skills", skills_summary.get('total_skills', 0))
    
    with col2:
        st.metric("Technical Skills", skills_summary.get('technical_skills_count', 0))
    
    with col3:
        st.metric("Soft Skills", skills_summary.get('soft_skills_count', 0))
    
    # Skills distribution chart
    if skills_summary.get('total_skills', 0) > 0:
        technical_count = skills_summary.get('technical_skills_count', 0)
        soft_count = skills_summary.get('soft_skills_count', 0)
        
        fig = px.pie(
            values=[technical_count, soft_count],
            names=['Technical Skills', 'Soft Skills'],
            title="Skills Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Technical skills by category
    technical_categories = skills_summary.get('technical_categories', {})
    if technical_categories:
        st.markdown("### 💻 Technical Skills by Category")
        
        categories = list(technical_categories.keys())
        counts = list(technical_categories.values())
        
        fig = px.bar(
            x=categories,
            y=counts,
            title="Technical Skills Distribution",
            labels={'x': 'Category', 'y': 'Number of Skills'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Display skills
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💻 Technical Skills")
        technical_skills = extracted_skills.get('technical_skills', [])
        if technical_skills:
            for skill in technical_skills:
                st.markdown(f"<span class='skill-tag'>{skill}</span>", unsafe_allow_html=True)
        else:
            st.info("No technical skills found.")
    
    with col2:
        st.markdown("### 🤝 Soft Skills")
        soft_skills = extracted_skills.get('soft_skills', [])
        if soft_skills:
            for skill in soft_skills:
                st.markdown(f"<span class='skill-tag'>{skill}</span>", unsafe_allow_html=True)
        else:
            st.info("No soft skills found.")

def display_resume_score(results):
    """Display resume scoring"""
    st.subheader("📊 Resume Score & ATS Optimization")
    
    resume_score = results.get('resume_score', {})
    
    if not resume_score:
        st.warning("No resume score available.")
        return
    
    # Overall score
    overall_score = resume_score.get('overall_score', 0)
    st.markdown(f"### Overall Resume Score: {format_score(overall_score)}")
    
    # Score breakdown
    breakdown = resume_score.get('breakdown', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Formatting", f"{breakdown.get('formatting_score', 0):.1f}/100")
    
    with col2:
        st.metric("Content", f"{breakdown.get('content_score', 0):.1f}/100")
    
    with col3:
        st.metric("Keywords", f"{breakdown.get('keyword_score', 0):.1f}/100")
    
    with col4:
        st.metric("Action Verbs", f"{breakdown.get('action_verb_score', 0):.1f}/100")
    
    # Score breakdown chart
    categories = ['Formatting', 'Content', 'Keywords', 'Action Verbs']
    scores = [
        breakdown.get('formatting_score', 0),
        breakdown.get('content_score', 0),
        breakdown.get('keyword_score', 0),
        breakdown.get('action_verb_score', 0)
    ]
    
    fig = px.bar(
        x=categories,
        y=scores,
        title="Score Breakdown",
        labels={'x': 'Category', 'y': 'Score'},
        color=scores,
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Strengths
    strengths = resume_score.get('strengths', [])
    if strengths:
        st.markdown("### ✅ Resume Strengths")
        for strength in strengths:
            st.markdown(f"""
            <div class="strength-card">
                ✅ {strength}
            </div>
            """, unsafe_allow_html=True)
    
    # Areas for improvement
    areas = resume_score.get('areas_for_improvement', [])
    if areas:
        st.markdown("### 🔧 Areas for Improvement")
        for area in areas:
            st.markdown(f"""
            <div class="suggestion-card">
                🔧 {area}
            </div>
            """, unsafe_allow_html=True)
    
    # Suggestions
    suggestions = resume_score.get('suggestions', [])
    if suggestions:
        st.markdown("### 💡 ATS Optimization Suggestions")
        
        for suggestion in suggestions:
            priority_color = get_priority_color(suggestion['priority'])
            st.markdown(f"""
            <div class="suggestion-card">
                <strong>{suggestion['category'].replace('_', ' ').title()}</strong><br>
                {suggestion['suggestion']}<br>
                <small><strong>Details:</strong> {suggestion['details']}</small><br>
                <small>Priority: <span style="color: {priority_color};">{suggestion['priority'].title()}</span></small>
            </div>
            """, unsafe_allow_html=True)

def display_parsed_content(results):
    """Display parsed content"""
    st.subheader("📄 Parsed Content")
    
    parsed_data = results.get('parsed_data', {})
    
    # Contact information
    contact_info = parsed_data.get('contact_info', {})
    if contact_info:
        st.markdown("### 📞 Contact Information")
        st.markdown(format_contact_info(contact_info))
    
    # File information
    file_info = results.get('file_info', {})
    if file_info:
        st.markdown("### 📁 File Information")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("File Type", file_info.get('file_type', 'N/A'))
        
        with col2:
            st.metric("File Size", f"{file_info.get('file_size', 0) / 1024:.1f} KB")
        
        with col3:
            st.metric("Word Count", file_info.get('word_count', 0))
        
        with col4:
            st.metric("Character Count", file_info.get('char_count', 0))
    
    # Parsed text
    text = parsed_data.get('text', '')
    if text:
        st.markdown("### 📝 Parsed Text")
        
        # Show first 500 characters with option to expand
        if len(text) > 500:
            st.text_area("Parsed Text (first 500 characters):", text[:500], height=200)
            with st.expander("View full parsed text"):
                st.text_area("Full Parsed Text:", text, height=400)
        else:
            st.text_area("Parsed Text:", text, height=300)

def display_export_options(results, analyzer):
    """Display export options"""
    st.subheader("💾 Export Results")
    
    # Export options in columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Export to JSON
        if st.button("📄 Export to JSON", type="primary", use_container_width=True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_analysis_{timestamp}.json"
            
            # Save results
            if analyzer.save_analysis_results(results, filename):
                st.success(f"✅ Results exported to {filename}")
                
                # Create download link
                with open(filename, 'r') as f:
                    json_str = f.read()
                
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=filename,
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.error("❌ Failed to export results")
    
    with col2:
        # Export to CSV
        if st.button("📊 Export to CSV", type="primary", use_container_width=True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_analysis_{timestamp}.csv"
            
            # Save results
            if analyzer.save_analysis_results_csv(results, filename):
                st.success(f"✅ Results exported to {filename}")
                
                # Create download link
                with open(filename, 'r') as f:
                    csv_str = f.read()
                
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_str,
                    file_name=filename,
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.error("❌ Failed to export results")
    
    # Summary export
    st.markdown("### 📋 Summary Export")
    
    summary = analyzer.get_analysis_summary(results)
    
    if 'error' not in summary:
        summary_text = f"""
Resume Analysis Summary
======================

Analysis Date: {results.get('analysis_timestamp', 'N/A')}
File Type: {results.get('file_info', {}).get('file_type', 'N/A')}
Word Count: {summary.get('word_count', 0)}

Skills Summary:
- Total Skills: {summary.get('total_skills', 0)}
- Technical Skills: {summary.get('technical_skills', 0)}
- Soft Skills: {summary.get('soft_skills', 0)}

Career Fit:
- Top Career Match: {summary.get('top_career', 'N/A')}
- Career Match Score: {summary.get('top_career_score', 0):.1f}%

Resume Score: {summary.get('resume_score', 0):.1f}/100
Contact Info Found: {'Yes' if summary.get('contact_info_found') else 'No'}
"""
        
        st.text_area("Summary:", summary_text, height=300)
        
        st.download_button(
            label="📥 Download Summary",
            data=summary_text,
            file_name=f"resume_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
