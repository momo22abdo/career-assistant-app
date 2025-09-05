# Career Assistant App

## 📌 Overview

An AI-powered career assistant that analyzes resumes, identifies skill gaps, provides job market insights, and suggests personalized learning paths. This intelligent application helps students and professionals discover optimal career paths through advanced machine learning algorithms and comprehensive data analysis.

## 🚀 Features

### **🎯 Smart Skill Matching**
Discover your ideal career path with our intelligent skill matching system. Simply input your current skills and watch as our AI-powered semantic matching engine analyzes your profile against 20+ career paths. Using advanced sentence transformers, the system provides percentage-based career matches with detailed breakdowns of aligned skills and missing competencies.

This feature empowers both students and professionals to make data-driven career decisions by clearly showing which roles best fit their existing skill set and where they stand in their career journey.

### **📄 AI-Powered Resume Analysis**
Transform your resume into actionable career insights with our comprehensive AI analysis engine. Upload your resume and receive intelligent skill extraction, career fit scoring, and keyword optimization recommendations. Our system analyzes your professional experience against industry standards and provides detailed feedback on how well your background aligns with specific career paths.

Beyond basic parsing, the analyzer offers improvement suggestions, identifies missing keywords that could enhance your visibility to recruiters, and provides a comprehensive career fit score to help you understand your competitive position in the job market.

### **📊 Gap Analysis & Skill Recommendations**
Bridge the gap between your current abilities and your dream career with our intelligent gap analysis system. Select any target career and receive a detailed breakdown of required skills categorized by difficulty levels (Beginner, Intermediate, Advanced). The system identifies exactly what you need to learn and provides personalized improvement suggestions tailored to your current skill level.

This feature serves as your personal career roadmap, showing you the most efficient path to acquire new competencies and advance in your chosen field with clear, actionable steps.

### **📚 Personalized Learning Path Generator**
Accelerate your professional development with structured, personalized learning paths designed specifically for your career goals. Our system generates comprehensive study plans that take you from beginner to advanced levels, complete with course recommendations from popular platforms, estimated timelines, and milestone tracking.

Each learning path is carefully curated to ensure optimal skill progression, featuring courses from top educational platforms and realistic time estimates to help you plan your professional development journey effectively.

### **💼 Comprehensive Job Market Insights**
Stay ahead of market trends with real-time job market intelligence and salary insights. Access detailed information about salary ranges, market demand data, growth projections, and hiring trends across different industries and geographic regions. Our system provides up-to-date information about job availability, competition levels, and emerging opportunities in your field.

This feature empowers you to make informed career decisions by understanding market dynamics, salary expectations, and growth potential in various career paths.

### **🤖 AI Career Chatbot**
Get instant answers to your career questions with our intelligent chatbot assistant. Powered by a comprehensive knowledge base of career-related information, the chatbot provides interactive Q&A sessions about careers, skills, learning paths, and industry insights. Each response comes with confidence scoring to help you gauge the reliability of the information.

Whether you're exploring new career options, seeking advice on skill development, or need quick answers about specific roles, our chatbot serves as your 24/7 career counselor.

### **🗺️ Interactive Career Roadmap Visualization**
Visualize your career journey with dynamic, interactive roadmaps that map your path from current skills to target career goals. Our visualization system creates personalized timelines showing skill acquisition phases, milestone achievements, and progress tracking capabilities. The interactive interface allows you to explore different career paths and understand the time investment required for each transition.

This visual approach makes career planning more engaging and helps you maintain motivation by clearly showing your progress and upcoming milestones.

### **👥 Peer Benchmarking & Comparison**
Understand your competitive position by comparing your profile with peers in your target career field. Our benchmarking system analyzes your skills, experience, and qualifications against similar professionals, providing insights into salary expectations, skill gaps, and career progression opportunities.

This feature helps you set realistic expectations, identify areas for improvement, and understand how you stack up against others in your field, enabling more strategic career planning.

### **🔮 Intelligent Recommendation Engine**
Receive personalized career recommendations powered by advanced machine learning algorithms. Our recommendation engine analyzes your skills, preferences, and career history to suggest optimal career matches, relevant job opportunities with match percentages, portfolio project ideas, and networking strategies.

The system continuously learns from user interactions and market trends to provide increasingly accurate and relevant recommendations tailored to your unique professional profile.

### **💻 Streamlit-based Interactive Interface**
Experience seamless career planning through our modern, user-friendly web interface built with Streamlit. The responsive design features real-time analysis, interactive visualizations, and intuitive navigation that makes complex career data accessible and actionable.

The interface provides instant feedback, dynamic charts, and an engaging user experience that transforms career planning from a tedious process into an interactive and insightful journey.

## 🛠️ Tech Stack

- **Python 3.x**: Core programming language
- **Streamlit**: Interactive web application framework
- **scikit-learn / NLP libraries**: Machine learning and natural language processing
- **Pandas, NumPy**: Data manipulation and numerical computing
- **Git & GitHub**: Version control and collaboration

## 📂 Project Structure

```bash
AI-Career-Assistant/
├── data/                           # Datasets and CSV files
│   ├── career_skills.csv          # Career-skill mappings
│   ├── salary_demand.csv          # Salary and demand data
│   ├── courses.csv                # Course recommendations
│   ├── job_posts.csv              # Job posting data
│   ├── peer_profiles.csv          # Peer benchmarking data
│   ├── career_keywords.csv        # Career-specific keywords
│   ├── qa_dataset.json            # Q&A dataset for chatbot
│   └── dataset_summary.json       # Dataset metadata
├── src/                            # Source code modules
│   ├── __init__.py                # Package initialization
│   ├── resume_analyzer/            # Resume analysis module
│   │   ├── app.py                 # Resume analyzer app
│   │   ├── backend/               # Backend processing
│   │   └── data/                  # Resume analyzer data
│   ├── job_insights/              # Job insights and analysis
│   │   └── __init__.py            # Job insights module
│   ├── learning_path/             # Learning path recommendation logic
│   │   └── __init__.py            # Learning path module
│   ├── ai_pipeline.py             # Main AI/ML pipeline
│   ├── ai_pipeline_simple.py      # Simplified AI pipeline
│   ├── data_generator.py          # Synthetic dataset generator
│   ├── enhanced_resume_analyzer.py # Enhanced resume analysis
│   ├── enhanced_peer_benchmarking.py # Peer comparison logic
│   └── file_parser.py             # File parsing utilities
├── tests/                          # Unit tests
│   ├── test_app.py                # Main app tests
│   ├── test_comprehensive_fixes.py # Comprehensive test suite
│   ├── test_job_insights_enhancements.py # Job insights tests
│   ├── test_learning_path_fixes.py # Learning path tests
│   ├── test_simple.py             # Simple functionality tests
│   └── test_utils.py              # Utility function tests
├── docs/                           # Documentation and notes
│   ├── GAP_ANALYSIS_IMPROVEMENTS.md # Gap analysis documentation
│   └── PROJECT_SUMMARY.md         # Project overview and summary
├── app.py                          # Main Streamlit application
├── main.py                         # Alternate entry point
├── debug.py                        # Debugging and troubleshooting
├── final_test.py                   # Final integration tests
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Career-Assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate datasets** (if needed)
   ```bash
   python src/data_generator.py
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**
   Open your browser and navigate to `http://localhost:8501`

## 💡 Usage

1. **Resume Analysis**: Upload your resume to get AI-powered career recommendations
2. **Skill Gap Analysis**: Compare your skills against target career requirements
3. **Job Market Research**: Explore salary trends and job market insights
4. **Learning Paths**: Get personalized course recommendations and study plans

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for career development and professional growth**
