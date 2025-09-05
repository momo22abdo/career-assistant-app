import json
import os
from typing import Dict, List, Any
import logging

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('resume_analyzer.log')
        ]
    )

def save_results(results: Dict[str, Any], output_path: str = "resume_analysis_results.json"):
    """
    Save analysis results to JSON file
    
    Args:
        results: Analysis results dictionary
        output_path: Output file path
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logging.error(f"Error saving results: {str(e)}")
        return False

def save_results_csv(results: Dict[str, Any], output_path: str = "resume_analysis_results.csv") -> bool:
    """
    Save analysis results to CSV file
    
    Args:
        results: Analysis results
        output_path: Output file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        import pandas as pd
        
        if not results.get('success'):
            return False
        
        # Extract key data for CSV
        data = []
        
        # File info
        file_info = results.get('file_info', {})
        data.append({
            'Category': 'File Info',
            'Field': 'File Type',
            'Value': file_info.get('file_type', 'N/A')
        })
        data.append({
            'Category': 'File Info',
            'Field': 'File Size (KB)',
            'Value': f"{file_info.get('file_size', 0) / 1024:.1f}"
        })
        data.append({
            'Category': 'File Info',
            'Field': 'Word Count',
            'Value': file_info.get('word_count', 0)
        })
        
        # Skills summary
        skills_summary = results.get('skills_summary', {})
        data.append({
            'Category': 'Skills',
            'Field': 'Total Skills',
            'Value': skills_summary.get('total_skills', 0)
        })
        data.append({
            'Category': 'Skills',
            'Field': 'Technical Skills',
            'Value': skills_summary.get('technical_skills_count', 0)
        })
        data.append({
            'Category': 'Skills',
            'Field': 'Soft Skills',
            'Value': skills_summary.get('soft_skills_count', 0)
        })
        
        # Career analysis
        career_analysis = results.get('career_analysis', [])
        if career_analysis:
            for i, career in enumerate(career_analysis[:5], 1):
                data.append({
                    'Category': f'Career {i}',
                    'Field': 'Career Name',
                    'Value': career.get('career', 'N/A')
                })
                data.append({
                    'Category': f'Career {i}',
                    'Field': 'Overall Score (%)',
                    'Value': f"{career.get('overall_score', 0):.1f}"
                })
                data.append({
                    'Category': f'Career {i}',
                    'Field': 'Required Coverage (%)',
                    'Value': f"{career.get('required_coverage', 0):.1f}"
                })
                data.append({
                    'Category': f'Career {i}',
                    'Field': 'Optional Coverage (%)',
                    'Value': f"{career.get('optional_coverage', 0):.1f}"
                })
        
        # Resume score
        resume_score = results.get('resume_score', {})
        data.append({
            'Category': 'Resume Score',
            'Field': 'Overall Score',
            'Value': f"{resume_score.get('overall_score', 0):.1f}/100"
        })
        data.append({
            'Category': 'Resume Score',
            'Field': 'Formatting Score',
            'Value': f"{resume_score.get('breakdown', {}).get('formatting_score', 0):.1f}/100"
        })
        data.append({
            'Category': 'Resume Score',
            'Field': 'Content Score',
            'Value': f"{resume_score.get('breakdown', {}).get('content_score', 0):.1f}/100"
        })
        data.append({
            'Category': 'Resume Score',
            'Field': 'Keyword Score',
            'Value': f"{resume_score.get('breakdown', {}).get('keyword_score', 0):.1f}/100"
        })
        data.append({
            'Category': 'Resume Score',
            'Field': 'Action Verb Score',
            'Value': f"{resume_score.get('breakdown', {}).get('action_verb_score', 0):.1f}/100"
        })
        
        # Create DataFrame and save
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        return True
        
    except Exception as e:
        logging.error(f"Error saving CSV results: {str(e)}")
        return False

def load_results(input_path: str) -> Dict[str, Any]:
    """
    Load analysis results from JSON file
    
    Args:
        input_path: Input file path
        
    Returns:
        Loaded results dictionary
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading results: {str(e)}")
        return {}

def validate_file_upload(file_path: str) -> Dict[str, Any]:
    """
    Validate uploaded file
    
    Args:
        file_path: Path to uploaded file
        
    Returns:
        Validation result dictionary
    """
    result = {
        'valid': False,
        'error': '',
        'file_type': '',
        'file_size': 0
    }
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            result['error'] = 'File does not exist'
            return result
        
        # Get file size
        file_size = os.path.getsize(file_path)
        result['file_size'] = file_size
        
        # Check file size (max 200MB)
        if file_size > 200 * 1024 * 1024:
            result['error'] = 'File size too large (max 200MB)'
            return result
        
        # Check file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        supported_extensions = ['.pdf', '.docx', '.txt']
        
        if file_extension not in supported_extensions:
            result['error'] = f'Unsupported file type: {file_extension}'
            return result
        
        result['file_type'] = file_extension
        result['valid'] = True
        
    except Exception as e:
        result['error'] = f'Error validating file: {str(e)}'
    
    return result

def format_contact_info(contact_info: Dict[str, str]) -> str:
    """
    Format contact information for display
    
    Args:
        contact_info: Contact information dictionary
        
    Returns:
        Formatted contact information string
    """
    formatted_parts = []
    
    if contact_info.get('email'):
        formatted_parts.append(f"📧 {contact_info['email']}")
    
    if contact_info.get('phone'):
        formatted_parts.append(f"📞 {contact_info['phone']}")
    
    if contact_info.get('linkedin'):
        formatted_parts.append(f"💼 {contact_info['linkedin']}")
    
    if contact_info.get('github'):
        formatted_parts.append(f"🐙 {contact_info['github']}")
    
    if contact_info.get('website'):
        formatted_parts.append(f"🌐 {contact_info['website']}")
    
    return '\n'.join(formatted_parts) if formatted_parts else "No contact information found"

def get_skill_category_icon(category: str) -> str:
    """
    Get icon for skill category
    
    Args:
        category: Skill category name
        
    Returns:
        Category icon
    """
    icons = {
        'programming_languages': '💻',
        'web_technologies': '🌐',
        'databases': '🗄️',
        'cloud_platforms': '☁️',
        'devops_tools': '🔧',
        'machine_learning': '🤖',
        'mobile_development': '📱',
        'soft_skills': '🤝',
        'communication': '💬',
        'leadership': '👑',
        'problem_solving': '🧩',
        'teamwork': '👥',
        'time_management': '⏰',
        'learning': '📚'
    }
    
    return icons.get(category, '⚙️')

def get_priority_color(priority: str) -> str:
    """
    Get color for priority level
    
    Args:
        priority: Priority level (high, medium, low)
        
    Returns:
        Color string
    """
    colors = {
        'high': 'red',
        'medium': 'orange',
        'low': 'green'
    }
    
    return colors.get(priority, 'blue')

def format_score(score: float) -> str:
    """
    Format score with color coding
    
    Args:
        score: Score value
        
    Returns:
        Formatted score string
    """
    if score >= 80:
        return f"🟢 {score}/100"
    elif score >= 60:
        return f"🟡 {score}/100"
    else:
        return f"🔴 {score}/100"

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Input text
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def create_sample_resume() -> str:
    """
    Create a sample resume for testing
    
    Returns:
        Sample resume text
    """
    return """
JOHN DOE
Software Engineer
john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe | github.com/johndoe

SUMMARY
Experienced software engineer with 5+ years developing scalable web applications using modern technologies. 
Skilled in Python, JavaScript, React, and cloud platforms. Strong problem-solving abilities and team collaboration.

EXPERIENCE
Senior Software Engineer | TechCorp Inc. | 2021-Present
• Developed and maintained microservices using Python and Flask
• Led a team of 3 developers in building a React-based dashboard
• Implemented CI/CD pipelines using Docker and AWS
• Optimized database queries resulting in 40% performance improvement
• Collaborated with product managers to define technical requirements

Software Engineer | StartupXYZ | 2019-2021
• Built RESTful APIs using Node.js and Express
• Created responsive web applications with React and TypeScript
• Managed PostgreSQL database and implemented data migrations
• Deployed applications using Docker and Kubernetes
• Participated in code reviews and mentored junior developers

EDUCATION
Bachelor of Science in Computer Science | University of Technology | 2019

SKILLS
Technical Skills: Python, JavaScript, React, Node.js, SQL, Git, Docker, AWS, TypeScript, HTML, CSS
Soft Skills: Communication, Problem Solving, Teamwork, Leadership, Time Management
"""
