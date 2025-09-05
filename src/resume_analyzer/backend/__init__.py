import os
import tempfile
from typing import Dict, List, Any, Optional
import logging

from .parser import ResumeParser
from .skills_extractor import SkillsExtractor
from .career_analyzer import CareerAnalyzer
from .resume_scorer import ResumeScorer
from .utils import setup_logging, save_results, save_results_csv, validate_file_upload, create_sample_resume

class ResumeAnalyzer:
    """Main Resume Analyzer class that orchestrates the entire analysis process"""
    
    def __init__(self, skills_vocab_path: str = "data/skills_vocab.json", 
                 careers_path: str = "data/careers.json"):
        """
        Initialize Resume Analyzer
        
        Args:
            skills_vocab_path: Path to skills vocabulary file
            careers_path: Path to careers definition file
        """
        setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.parser = ResumeParser()
        self.skills_extractor = SkillsExtractor(skills_vocab_path)
        self.career_analyzer = CareerAnalyzer(careers_path)
        self.resume_scorer = ResumeScorer()
        
        self.logger.info("Resume Analyzer initialized successfully")
    
    def analyze_resume_file(self, file_path: str, top_careers: int = 5) -> Dict[str, Any]:
        """
        Analyze resume from file
        
        Args:
            file_path: Path to resume file
            top_careers: Number of top career matches to return
            
        Returns:
            Complete analysis results
        """
        try:
            self.logger.info(f"Starting analysis of file: {file_path}")
            
            # Validate file
            validation = validate_file_upload(file_path)
            if not validation['valid']:
                return {
                    'error': validation['error'],
                    'success': False
                }
            
            # Parse resume
            parsed_data = self.parser.parse_resume(file_path)
            if parsed_data.get('error'):
                return {
                    'error': parsed_data['error'],
                    'success': False
                }
            
            # Clean text
            cleaned_text = self.parser.clean_text(parsed_data['text'])
            
            # Extract contact information
            contact_info = self.parser.extract_contact_info(cleaned_text)
            
            # Extract skills
            extracted_skills = self.skills_extractor.extract_skills(cleaned_text)
            
            # Analyze career fit
            career_analysis = self.career_analyzer.analyze_career_fit(
                extracted_skills, top_careers
            )
            
            # Score resume
            resume_score = self.resume_scorer.score_resume(
                cleaned_text, extracted_skills, career_analysis
            )
            
            # Generate career recommendations
            career_recommendations = self.career_analyzer.get_career_recommendations(
                career_analysis
            )
            
            # Generate career comparison
            career_comparison = self.career_analyzer.get_career_comparison(
                career_analysis
            )
            
            # Get skills summary
            skills_summary = self.skills_extractor.get_skills_summary(extracted_skills)
            
            # Compile results
            results = {
                'success': True,
                'file_info': {
                    'file_path': file_path,
                    'file_type': validation['file_type'],
                    'file_size': validation['file_size'],
                    'word_count': len(cleaned_text.split()),
                    'char_count': len(cleaned_text)
                },
                'parsed_data': {
                    'text': cleaned_text,
                    'contact_info': contact_info,
                    'metadata': parsed_data.get('metadata', {})
                },
                'extracted_skills': extracted_skills,
                'skills_summary': skills_summary,
                'career_analysis': career_analysis,
                'career_recommendations': career_recommendations,
                'career_comparison': career_comparison,
                'resume_score': resume_score,
                'analysis_timestamp': self._get_timestamp()
            }
            
            self.logger.info("Resume analysis completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Error during resume analysis: {str(e)}")
            return {
                'error': f"Analysis failed: {str(e)}",
                'success': False
            }
    
    def analyze_resume_text(self, text: str, top_careers: int = 5) -> Dict[str, Any]:
        """
        Analyze resume from text input
        
        Args:
            text: Resume text
            top_careers: Number of top career matches to return
            
        Returns:
            Complete analysis results
        """
        try:
            self.logger.info("Starting analysis of resume text")
            
            if not text.strip():
                return {
                    'error': 'Empty resume text provided',
                    'success': False
                }
            
            # Clean text
            cleaned_text = self.parser.clean_text(text)
            
            # Extract contact information
            contact_info = self.parser.extract_contact_info(cleaned_text)
            
            # Extract skills
            extracted_skills = self.skills_extractor.extract_skills(cleaned_text)
            
            # Analyze career fit
            career_analysis = self.career_analyzer.analyze_career_fit(
                extracted_skills, top_careers
            )
            
            # Score resume
            resume_score = self.resume_scorer.score_resume(
                cleaned_text, extracted_skills, career_analysis
            )
            
            # Generate career recommendations
            career_recommendations = self.career_analyzer.get_career_recommendations(
                career_analysis
            )
            
            # Generate career comparison
            career_comparison = self.career_analyzer.get_career_comparison(
                career_analysis
            )
            
            # Get skills summary
            skills_summary = self.skills_extractor.get_skills_summary(extracted_skills)
            
            # Compile results
            results = {
                'success': True,
                'file_info': {
                    'file_path': 'text_input',
                    'file_type': 'text',
                    'file_size': len(text.encode('utf-8')),
                    'word_count': len(cleaned_text.split()),
                    'char_count': len(cleaned_text)
                },
                'parsed_data': {
                    'text': cleaned_text,
                    'contact_info': contact_info,
                    'metadata': {}
                },
                'extracted_skills': extracted_skills,
                'skills_summary': skills_summary,
                'career_analysis': career_analysis,
                'career_recommendations': career_recommendations,
                'career_comparison': career_comparison,
                'resume_score': resume_score,
                'analysis_timestamp': self._get_timestamp()
            }
            
            self.logger.info("Resume text analysis completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Error during resume text analysis: {str(e)}")
            return {
                'error': f"Analysis failed: {str(e)}",
                'success': False
            }
    
    def run_sample_analysis(self) -> Dict[str, Any]:
        """
        Run analysis on sample resume for testing
        
        Returns:
            Sample analysis results
        """
        self.logger.info("Running sample analysis")
        
        sample_text = create_sample_resume()
        return self.analyze_resume_text(sample_text)
    
    def save_analysis_results(self, results: Dict[str, Any], 
                             output_path: str = "resume_analysis_results.json") -> bool:
        """
        Save analysis results to file
        
        Args:
            results: Analysis results
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        return save_results(results, output_path)
    
    def save_analysis_results_csv(self, results: Dict[str, Any], 
                                 output_path: str = "resume_analysis_results.csv") -> bool:
        """
        Save analysis results to CSV file
        
        Args:
            results: Analysis results
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        return save_results_csv(results, output_path)
    
    def get_analysis_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of analysis results
        
        Args:
            results: Complete analysis results
            
        Returns:
            Summary dictionary
        """
        if not results.get('success'):
            return {'error': results.get('error', 'Analysis failed')}
        
        skills_summary = results.get('skills_summary', {})
        career_analysis = results.get('career_analysis', [])
        resume_score = results.get('resume_score', {})
        
        summary = {
            'total_skills': skills_summary.get('total_skills', 0),
            'technical_skills': skills_summary.get('technical_skills_count', 0),
            'soft_skills': skills_summary.get('soft_skills_count', 0),
            'top_career': career_analysis[0]['career'] if career_analysis else 'N/A',
            'top_career_score': career_analysis[0]['overall_score'] if career_analysis else 0,
            'resume_score': resume_score.get('overall_score', 0),
            'contact_info_found': bool(results.get('parsed_data', {}).get('contact_info', {}).get('email')),
            'word_count': results.get('file_info', {}).get('word_count', 0)
        }
        
        return summary
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_supported_file_types(self) -> List[str]:
        """Get list of supported file types"""
        return ['.pdf', '.docx', '.txt']
    
    def get_max_file_size(self) -> int:
        """Get maximum file size in bytes"""
        return 200 * 1024 * 1024  # 200MB
