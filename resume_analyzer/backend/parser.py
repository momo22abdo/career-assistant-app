import pdfplumber
import docx2txt
import re
import os
from typing import Dict, List, Optional
import logging

class ResumeParser:
    """Parse resumes from PDF, DOCX, and TXT files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def parse_resume(self, file_path: str) -> Dict[str, any]:
        """
        Parse resume from file and extract text content
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Dictionary containing parsed text and metadata
        """
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                return self._parse_pdf(file_path)
            elif file_extension == '.docx':
                return self._parse_docx(file_path)
            elif file_extension == '.txt':
                return self._parse_txt(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
        except Exception as e:
            self.logger.error(f"Error parsing resume: {str(e)}")
            return {
                'text': '',
                'metadata': {},
                'error': str(e)
            }
    
    def _parse_pdf(self, file_path: str) -> Dict[str, any]:
        """Parse PDF resume using pdfplumber with OCR fallback"""
        try:
            text_content = []
            metadata = {}
            
            with pdfplumber.open(file_path) as pdf:
                # Extract metadata
                if pdf.metadata:
                    metadata = {
                        'title': pdf.metadata.get('Title', ''),
                        'author': pdf.metadata.get('Author', ''),
                        'subject': pdf.metadata.get('Subject', ''),
                        'creator': pdf.metadata.get('Creator', ''),
                        'producer': pdf.metadata.get('Producer', ''),
                        'pages': len(pdf.pages)
                    }
                
                # Extract text from each page
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
            
            full_text = '\n'.join(text_content)
            
            # If no text extracted, try OCR fallback
            if not full_text.strip():
                self.logger.warning("No text extracted from PDF, attempting OCR fallback")
                full_text = self._ocr_fallback(file_path)
            
            return {
                'text': full_text,
                'metadata': metadata,
                'file_type': 'pdf',
                'pages': metadata.get('pages', 0)
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing PDF: {str(e)}")
            # Try OCR as last resort
            try:
                self.logger.info("Attempting OCR fallback for PDF")
                ocr_text = self._ocr_fallback(file_path)
                if ocr_text:
                    return {
                        'text': ocr_text,
                        'metadata': {'file_type': 'pdf', 'ocr_used': True},
                        'file_type': 'pdf',
                        'pages': 1
                    }
            except Exception as ocr_error:
                self.logger.error(f"OCR fallback also failed: {str(ocr_error)}")
            
            return {
                'text': '',
                'metadata': {},
                'error': f"PDF parsing error: {str(e)}"
            }
    
    def _ocr_fallback(self, file_path: str) -> str:
        """OCR fallback for PDF files that can't be parsed normally"""
        try:
            import pytesseract
            from PIL import Image
            import fitz  # PyMuPDF
            
            # Convert PDF to image and extract text
            doc = fitz.open(file_path)
            text_content = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Extract text using OCR
                page_text = pytesseract.image_to_string(img)
                if page_text.strip():
                    text_content.append(page_text)
            
            doc.close()
            return '\n'.join(text_content)
            
        except ImportError:
            self.logger.warning("OCR dependencies not available (pytesseract, PIL, PyMuPDF)")
            return ""
        except Exception as e:
            self.logger.error(f"OCR fallback failed: {str(e)}")
            return ""
    
    def _parse_docx(self, file_path: str) -> Dict[str, any]:
        """Parse DOCX resume using docx2txt"""
        try:
            text_content = docx2txt.process(file_path)
            
            # Basic metadata extraction
            metadata = {
                'file_type': 'docx',
                'word_count': len(text_content.split())
            }
            
            return {
                'text': text_content,
                'metadata': metadata,
                'file_type': 'docx'
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing DOCX: {str(e)}")
            return {
                'text': '',
                'metadata': {},
                'error': f"DOCX parsing error: {str(e)}"
            }
    
    def _parse_txt(self, file_path: str) -> Dict[str, any]:
        """Parse TXT resume"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            text_content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        text_content = file.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if text_content is None:
                # Fallback: read as binary and decode with error handling
                with open(file_path, 'rb') as file:
                    text_content = file.read().decode('utf-8', errors='ignore')
            
            metadata = {
                'file_type': 'txt',
                'word_count': len(text_content.split()),
                'char_count': len(text_content)
            }
            
            return {
                'text': text_content,
                'metadata': metadata,
                'file_type': 'txt'
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing TXT: {str(e)}")
            return {
                'text': '',
                'metadata': {},
                'error': f"TXT parsing error: {str(e)}"
            }
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\+\=\*\/\(\)\[\]\{\}\@\#\$\%\&\|]', ' ', text)
        
        # Normalize bullet points
        text = re.sub(r'[•·▪▫‣⁃]', '•', text)
        
        # Clean up multiple spaces
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """
        Extract contact information from resume text
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with contact information
        """
        contact_info = {
            'email': '',
            'phone': '',
            'linkedin': '',
            'github': '',
            'website': ''
        }
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Phone pattern (various formats)
        phone_patterns = [
            r'\+?1?\s*\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{4}',
            r'\+?[0-9]{1,4}[\s\-]?[0-9]{1,4}[\s\-]?[0-9]{1,4}[\s\-]?[0-9]{1,4}',
            r'\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{4}'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact_info['phone'] = phone_match.group()
                break
        
        # LinkedIn pattern
        linkedin_pattern = r'(?:linkedin\.com/in/|linkedin\.com/company/)[a-zA-Z0-9\-_]+'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact_info['linkedin'] = linkedin_match.group()
        
        # GitHub pattern
        github_pattern = r'github\.com/[a-zA-Z0-9\-_]+'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            contact_info['github'] = github_match.group()
        
        # Website pattern
        website_pattern = r'(?:https?://)?(?:www\.)?[a-zA-Z0-9\-_]+\.(?:com|org|net|edu|io|co|tech|dev)'
        website_match = re.search(website_pattern, text)
        if website_match:
            contact_info['website'] = website_match.group()
        
        return contact_info
