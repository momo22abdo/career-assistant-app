# Resume Analyzer

An AI-powered resume analysis tool that extracts skills, analyzes career fit, and provides ATS optimization suggestions.

## Features

### 📄 Parsing Layer
- **PDF Support**: Uses `pdfplumber` for robust PDF parsing with OCR fallback
- **DOCX Support**: Uses `docx2txt` for Word document parsing  
- **TXT Support**: Direct text file reading
- **OCR Fallback**: Automatic OCR for image-based PDFs using `pytesseract` and `PyMuPDF`
- **Large File Support**: Handles files up to 200MB
- **Error Recovery**: Graceful fallback to text input when file parsing fails

### 🔍 Skills Extraction
- **Automatic Detection**: Extracts technical and soft skills from resume text
- **Fuzzy Matching**: Uses `rapidfuzz` for intelligent skill matching
- **Normalization**: Maps variations to canonical skill names
- **Comprehensive Vocabulary**: Pre-defined skills database with synonyms

### 🎯 Career Fit Analysis
- **Multi-Career Comparison**: Analyzes fit across multiple career paths
- **Importance-Weighted Scoring**: Considers skill importance levels
- **Gap Analysis**: Identifies missing critical and optional skills
- **Career Recommendations**: Provides actionable improvement suggestions

### 📊 Resume Scoring & ATS Optimization
- **Comprehensive Scoring**: 0-100 score based on multiple factors
- **Formatting Analysis**: Evaluates resume structure and presentation
- **Keyword Optimization**: Analyzes keyword density and relevance
- **Action Verb Detection**: Identifies strong action verb usage
- **Improvement Suggestions**: Specific recommendations for enhancement

### 🎨 Modern UI
- **Streamlit Interface**: Clean, responsive web interface
- **Interactive Charts**: Visual data representation with Plotly
- **Export Options**: JSON, CSV, and text export capabilities
- **Real-time Analysis**: Instant feedback and results
- **Enhanced File Upload**: File size display and better error handling
- **Fallback Suggestions**: Helpful guidance when file parsing fails

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd resume_analyzer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

## Usage

### File Upload
1. Select "📁 Upload File" from the sidebar
2. Upload your resume (PDF, DOCX, or TXT format)
3. View comprehensive analysis results

### Text Input
1. Select "📝 Paste Text" from the sidebar
2. Paste your resume text directly
3. Get instant analysis and recommendations

### Sample Analysis
1. Select "🧪 Sample Analysis" from the sidebar
2. Run analysis on a sample resume
3. Explore the tool's capabilities

## Project Structure

```
resume_analyzer/
├── app.py                 # Streamlit UI application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── backend/              # Core analysis engine
│   ├── __init__.py       # Main ResumeAnalyzer class
│   ├── parser.py         # File parsing and text extraction
│   ├── skills_extractor.py # Skills detection and matching
│   ├── career_analyzer.py # Career fit analysis
│   ├── resume_scorer.py  # Resume scoring and ATS optimization
│   └── utils.py          # Utility functions
└── data/                 # Data files
    ├── skills_vocab.json # Skills vocabulary and synonyms
    └── careers.json      # Career definitions and requirements
```

## Data Files

### skills_vocab.json
Comprehensive vocabulary of technical and soft skills with:
- Canonical skill names
- Synonyms and variations
- Category organization
- Fuzzy matching support

### careers.json
Career definitions including:
- Career descriptions
- Required skills with importance weights
- Optional skills with importance weights
- Skill categorization

## API Usage

```python
from backend import ResumeAnalyzer

# Initialize analyzer
analyzer = ResumeAnalyzer()

# Analyze resume file
results = analyzer.analyze_resume_file("path/to/resume.pdf")

# Analyze resume text
results = analyzer.analyze_resume_text("resume text content")

# Run sample analysis
results = analyzer.run_sample_analysis()

# Export results
analyzer.save_analysis_results(results, "output.json")
```

## Output Format

The analysis returns a comprehensive JSON object containing:

```json
{
  "success": true,
  "file_info": {
    "file_path": "resume.pdf",
    "file_type": ".pdf",
    "file_size": 123456,
    "word_count": 500,
    "char_count": 2500
  },
  "parsed_data": {
    "text": "cleaned resume text",
    "contact_info": {
      "email": "user@example.com",
      "phone": "(555) 123-4567",
      "linkedin": "linkedin.com/in/user",
      "github": "github.com/user",
      "website": "user.com"
    }
  },
  "extracted_skills": {
    "technical_skills": ["Python", "JavaScript", "React"],
    "soft_skills": ["Communication", "Leadership"],
    "all_skills": ["Python", "JavaScript", "React", "Communication", "Leadership"]
  },
  "skills_summary": {
    "total_skills": 5,
    "technical_skills_count": 3,
    "soft_skills_count": 2,
    "technical_categories": {
      "programming_languages": 2,
      "web_technologies": 1
    }
  },
  "career_analysis": [
    {
      "career": "Software Engineer",
      "overall_score": 85.5,
      "required_coverage": 90.0,
      "optional_coverage": 75.0,
      "required_matches": [...],
      "required_missing": [...],
      "skill_gaps": {...}
    }
  ],
  "resume_score": {
    "overall_score": 78.5,
    "breakdown": {
      "formatting_score": 85.0,
      "content_score": 75.0,
      "keyword_score": 80.0,
      "action_verb_score": 70.0
    },
    "suggestions": [...],
    "strengths": [...],
    "areas_for_improvement": [...]
  }
}
```

## Dependencies

### Core Libraries
- **streamlit**: Web interface framework
- **pdfplumber**: PDF parsing and text extraction
- **docx2txt**: DOCX file parsing
- **rapidfuzz**: Fuzzy string matching for skills
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing

### Optional Libraries
- **sentence-transformers**: Semantic skill matching
- **scikit-learn**: Machine learning utilities
- **plotly**: Interactive data visualization
- **Pillow**: Image processing
- **pytesseract**: OCR capabilities
- **PyMuPDF**: PDF processing for OCR fallback

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue in the repository
- Check the documentation
- Review the example usage

## Roadmap

- [x] Enhanced OCR support with PyMuPDF
- [x] Large file support (200MB)
- [x] CSV export functionality
- [x] Better error handling and fallback suggestions
- [ ] Multi-language support
- [ ] Resume template suggestions
- [ ] Integration with job boards
- [ ] Advanced skill recommendations
- [ ] Resume comparison features
