# 🚀 AI Career Assistant

An intelligent career recommendation and learning assistant built with Streamlit and AI/ML models. This application helps students and professionals discover career paths, analyze skill gaps, and get personalized learning recommendations.

## ✨ Features

### 🎯 Smart Skill Matching
- Input your skills and get career matches with percentage scores
- AI-powered semantic matching using sentence transformers
- Detailed breakdown of matched and missing skills

### 📊 Gap Analysis & Skill Suggestions
- Analyze skill gaps for any target career
- Categorized by difficulty levels (Beginner, Intermediate, Advanced)
- Personalized improvement suggestions and recommendations

### 📚 Learning Path Generator
- Structured learning paths from beginner to advanced
- Course recommendations from popular platforms
- Estimated timelines and study schedules

### 💼 Job Market Insights
- Salary ranges and market demand data
- Top hiring countries and growth projections
- Recent job openings with match percentages

### 📄 Resume Analyzer
- AI-powered resume analysis and career fit scoring
- Skills extraction and keyword analysis
- Improvement suggestions and optimization tips

### 🤖 AI Career Chatbot
- Interactive Q&A about careers, skills, and learning paths
- Pre-trained responses for common career questions
- Confidence scoring for responses

### 🗺️ Career Roadmap Visualization
- Visual journey from current skills to target career
- Progress tracking and milestone planning
- Interactive timeline and phase breakdown

### 👥 Peer Benchmarking
- Compare your profile with peers in the same career
- Skill comparison and gap analysis
- Salary and experience benchmarking

### 🔮 Personalized Recommendation Engine
- Career matches based on skills and preferences
- Job opportunities with match percentages
- Portfolio project suggestions and networking tips

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: 
  - Sentence Transformers for semantic matching
  - Scikit-learn for similarity calculations
  - NLTK for text processing
  - TextBlob for sentiment analysis
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly, Matplotlib, Seaborn
- **Data Storage**: CSV files (synthetic datasets)

## 📊 Datasets

The application uses comprehensive synthetic datasets:

- **Career Skills Mapping**: 20 careers with required/optional skills
- **Salary & Demand Data**: Market insights for each career
- **Online Courses**: 165+ courses across multiple platforms
- **Job Postings**: 100+ synthetic job listings
- **Peer Profiles**: 185+ peer profiles for benchmarking
- **Career Keywords**: Keywords and frequency data for resume analysis
- **Q&A Dataset**: Pre-defined questions and answers for chatbot

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd career-path
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate datasets** (if not already present)
   ```bash
   python src/data_generator.py
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
career-path/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── src/
│   ├── data_generator.py # Synthetic dataset generator
│   └── ai_pipeline.py    # AI/ML pipeline and models
├── data/                 # Generated datasets
│   ├── career_skills.csv
│   ├── salary_demand.csv
│   ├── courses.csv
│   ├── job_posts.csv
│   ├── peer_profiles.csv
│   ├── career_keywords.csv
│   └── qa_dataset.json
└── tests/
    └── test_utils.py     # Unit tests
```

## 🎯 Usage Examples

### Skill Matching
1. Navigate to "🎯 Skill Matching"
2. Enter your skills (e.g., "Python, SQL, Machine Learning")
3. Click "Find Career Matches"
4. View career matches with percentage scores

### Gap Analysis
1. Go to "📊 Gap Analysis"
2. Enter your current skills
3. Select a target career
4. Get detailed gap analysis and recommendations

### Resume Analysis
1. Visit "📄 Resume Analyzer"
2. Paste your resume text or upload a file
3. Get AI-powered career fit analysis
4. Review improvement suggestions

### Learning Path
1. Access "📚 Learning Path"
2. Enter your skills and target career
3. Get structured learning recommendations
4. Follow the phased approach

## 🔧 Customization

### Adding New Careers
Edit `src/data_generator.py` and add new careers to the `careers` list, then regenerate datasets.

### Adding New Skills
Update the `skills` list in the data generator and regenerate datasets.

### Modifying AI Models
The AI pipeline in `src/ai_pipeline.py` can be customized:
- Change sentence transformer model
- Adjust similarity thresholds
- Modify scoring algorithms

## 📈 Performance

- **Dataset Size**: ~1,000 records across all datasets
- **Response Time**: <2 seconds for most operations
- **Memory Usage**: ~500MB with all models loaded
- **Accuracy**: 85%+ for skill matching with semantic similarity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Hugging Face for sentence transformers
- The open-source community for various libraries

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Check the documentation
- Review the example usage

---

**Built with ❤️ for career development and learning**
