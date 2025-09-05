import pandas as pd
import json
import random
from typing import List, Dict, Any

class CareerDataGenerator:
    def __init__(self):
        self.careers = [
            "Data Scientist", "Data Engineer", "Machine Learning Engineer", 
            "Software Engineer", "Frontend Developer", "Backend Developer",
            "DevOps Engineer", "Product Manager", "UX Designer", "Data Analyst",
            "Business Analyst", "Cloud Architect", "Cybersecurity Analyst",
            "AI Research Scientist", "Full Stack Developer", "Mobile Developer",
            "QA Engineer", "Technical Writer", "Data Architect", "MLOps Engineer"
        ]
        
        self.skills = [
            # Programming Languages
            "Python", "Java", "JavaScript", "SQL", "C++", "C#", "Go", "Rust", 
            "Scala", "Kotlin", "Swift", "PHP", "Ruby", "R", "MATLAB", "Julia",
            
            # Data Science & ML
            "Machine Learning", "Deep Learning", "Statistics", "Data Science",
            "Data Visualization", "Data Analysis", "Data Cleaning", "Feature Engineering",
            "Model Evaluation", "A/B Testing", "Business Intelligence",
            
            # ML/AI Frameworks
            "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "XGBoost", "LightGBM",
            
            # Data Tools
            "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly", "Jupyter",
            "Anaconda", "Tableau", "Power BI", "Looker", "Qlik", "SAS", "SPSS",
            
            # Web Development
            "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "TypeScript",
            "Flask", "Django", "FastAPI", "Spring Boot", "Express.js",
            
            # Databases
            "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Oracle",
            "SQL Server", "Cassandra", "DynamoDB", "Neo4j",
            
            # Cloud & DevOps
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Ansible",
            "Jenkins", "GitLab CI", "GitHub Actions", "CI/CD", "DevOps",
            
            # Big Data
            "Hadoop", "Spark", "Kafka", "Hive", "Pig", "Storm", "Flink",
            
            # Tools & Platforms
            "Git", "Linux", "Shell Scripting", "Bash", "PowerShell", "JIRA",
            "Confluence", "Agile", "Scrum", "Kanban",
            
            # Design & UX
            "Figma", "Adobe XD", "Sketch", "InVision", "Principle", "Protopie",
            "User Research", "Prototyping", "Usability Testing", "Design Systems",
            
            # Testing
            "Selenium", "JUnit", "Pytest", "Cypress", "Postman", "Swagger",
            "API Testing", "Performance Testing", "Security Testing",
            
            # Security
            "Cybersecurity", "Network Security", "Application Security", "Incident Response",
            "Threat Intelligence", "Vulnerability Assessment", "Penetration Testing",
            
            # Business & Management
            "Product Management", "Business Analysis", "Project Management",
            "Stakeholder Management", "Requirements Gathering", "Process Improvement",
            "Change Management", "Risk Assessment", "Cost-Benefit Analysis",
            
            # Communication & Documentation
            "Technical Writing", "Documentation", "Markdown", "Content Strategy",
            "Knowledge Management", "Training", "Presentation Skills",
            
            # Specialized Skills
            "Computer Vision", "NLP", "Reinforcement Learning", "MLOps",
            "Data Engineering", "ETL", "Data Warehousing", "Data Governance",
            "Microservices", "API Design", "System Design", "Distributed Systems",
            "Mobile Development", "Game Development", "Blockchain", "IoT"
        ]
        
        self.platforms = ["Coursera", "edX", "Udemy", "DataCamp", "Pluralsight", 
                         "LinkedIn Learning", "MIT OpenCourseWare", "Stanford Online"]
        
        self.countries = ["United States", "United Kingdom", "Germany", "Canada", 
                         "Australia", "Netherlands", "Sweden", "Switzerland", 
                         "Singapore", "Japan", "India", "Brazil", "France", "Spain"]
    
    def generate_career_skills_mapping(self) -> pd.DataFrame:
        """Generate mapping of careers to required skills with difficulty levels"""
        data = []
        
        career_skill_mapping = {
            "Data Scientist": [
                "Python", "SQL", "Machine Learning", "Statistics", "Data Visualization", 
                "Pandas", "NumPy", "Scikit-learn", "Jupyter", "Matplotlib", "Seaborn", 
                "Plotly", "R", "TensorFlow", "PyTorch", "Deep Learning", "Data Cleaning",
                "Feature Engineering", "Model Evaluation", "A/B Testing", "Business Intelligence"
            ],
            "Data Engineer": [
                "Python", "SQL", "Hadoop", "Spark", "Kafka", "Docker", "AWS", "Data Architecture",
                "ETL", "Data Warehousing", "Data Modeling", "NoSQL", "PostgreSQL", "MongoDB", 
                "Redis", "Elasticsearch", "Kubernetes", "Terraform", "CI/CD", "Data Governance",
                "Data Quality", "Streaming Data", "Big Data", "Cloud Platforms", "Linux"
            ],
            "Machine Learning Engineer": [
                "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", 
                "MLOps", "Docker", "Kubernetes", "Scikit-learn", "NumPy", "Pandas", 
                "Jupyter", "Statistics", "Mathematics", "Linear Algebra", "Calculus",
                "Probability", "Optimization", "Neural Networks", "Computer Vision", 
                "NLP", "Model Deployment", "MLOps Tools", "Cloud ML", "Monitoring"
            ],
            "Software Engineer": [
                "Java", "Python", "JavaScript", "Git", "Data Structures", "Algorithms", 
                "SQL", "Docker", "REST APIs", "Microservices", "Design Patterns", 
                "Object-Oriented Programming", "Functional Programming", "Testing", 
                "CI/CD", "Agile", "Scrum", "Code Review", "Performance Optimization",
                "Security", "Database Design", "System Design", "Distributed Systems"
            ],
            "Frontend Developer": [
                "HTML", "CSS", "JavaScript", "React", "TypeScript", "Responsive Design", 
                "Git", "Web APIs", "Angular", "Vue.js", "SASS", "LESS", "Webpack", 
                "Babel", "ES6+", "DOM Manipulation", "AJAX", "REST APIs", "GraphQL",
                "Progressive Web Apps", "Accessibility", "Performance", "Testing", "SEO"
            ],
            "Backend Developer": [
                "Python", "Java", "Node.js", "SQL", "REST APIs", "Microservices", 
                "Docker", "Cloud Platforms", "Flask", "Django", "Spring Boot", 
                "Express.js", "Database Design", "Authentication", "Authorization",
                "API Design", "Caching", "Message Queues", "WebSockets", "GraphQL",
                "Testing", "Performance", "Security", "Monitoring", "Logging"
            ],
            "DevOps Engineer": [
                "Docker", "Kubernetes", "AWS", "Jenkins", "Terraform", "Linux", 
                "Shell Scripting", "CI/CD", "Azure", "GCP", "Ansible", "Chef", 
                "Puppet", "GitLab CI", "GitHub Actions", "Monitoring", "Logging",
                "Infrastructure as Code", "Networking", "Security", "Compliance",
                "Backup", "Disaster Recovery", "Performance Tuning", "Automation"
            ],
            "Product Manager": [
                "Agile", "Scrum", "JIRA", "User Research", "Data Analysis", "SQL", 
                "Excel", "Product Strategy", "User Stories", "Requirements Gathering",
                "Stakeholder Management", "Market Research", "Competitive Analysis",
                "Product Roadmap", "A/B Testing", "Analytics", "User Experience",
                "Business Model", "Go-to-Market Strategy", "Customer Development",
                "Metrics", "KPIs", "Product Launch", "Customer Success"
            ],
            "UX Designer": [
                "Figma", "Adobe XD", "User Research", "Prototyping", "Usability Testing", 
                "Design Systems", "HTML", "CSS", "Sketch", "InVision", "Principle",
                "User Interviews", "Surveys", "Personas", "User Journey Maps",
                "Wireframing", "Information Architecture", "Interaction Design",
                "Visual Design", "Typography", "Color Theory", "Accessibility",
                "Design Thinking", "Human-Centered Design", "A/B Testing"
            ],
            "Data Analyst": [
                "SQL", "Excel", "Python", "Tableau", "Power BI", "Statistics", 
                "Data Cleaning", "Data Visualization", "Pandas", "NumPy", "R",
                "Business Intelligence", "Data Storytelling", "Dashboard Design",
                "KPI Tracking", "Trend Analysis", "Forecasting", "Hypothesis Testing",
                "Correlation Analysis", "Regression", "Data Quality", "ETL"
            ],
            "Business Analyst": [
                "SQL", "Excel", "Business Process", "Requirements Gathering", 
                "Stakeholder Management", "Data Analysis", "JIRA", "Business Process Modeling",
                "Process Improvement", "Change Management", "Risk Assessment",
                "Cost-Benefit Analysis", "ROI Analysis", "Business Rules", "Use Cases",
                "User Stories", "Workflow Design", "Documentation", "Training",
                "Business Intelligence", "Reporting", "Analytics"
            ],
            "Cloud Architect": [
                "AWS", "Azure", "GCP", "Terraform", "Docker", "Kubernetes", 
                "Networking", "Security", "Cloud Computing", "Microservices",
                "Serverless", "Containerization", "Infrastructure as Code",
                "Cloud Security", "Compliance", "Cost Optimization", "Performance",
                "Scalability", "High Availability", "Disaster Recovery", "Monitoring",
                "Logging", "Backup", "Migration", "Multi-Cloud Strategy"
            ],
            "Cybersecurity Analyst": [
                "Linux", "Networking", "Security Tools", "Incident Response", 
                "Threat Intelligence", "Python", "SIEM", "Vulnerability Assessment",
                "Penetration Testing", "Security Monitoring", "Forensics",
                "Compliance", "Risk Assessment", "Security Policies", "Access Control",
                "Encryption", "Firewall", "IDS/IPS", "Security Awareness", "Training",
                "Incident Management", "Threat Hunting", "Malware Analysis"
            ],
            "AI Research Scientist": [
                "Python", "Machine Learning", "Deep Learning", "Mathematics", 
                "Research Methods", "PyTorch", "TensorFlow", "Linear Algebra",
                "Calculus", "Probability", "Statistics", "Optimization", "Neural Networks",
                "Computer Vision", "NLP", "Reinforcement Learning", "Research Design",
                "Data Collection", "Experimental Design", "Academic Writing", "Publications",
                "Conference Presentations", "Grant Writing", "Collaboration"
            ],
            "Full Stack Developer": [
                "HTML", "CSS", "JavaScript", "Python", "Java", "SQL", "React", 
                "Node.js", "Docker", "Full Stack Development", "Web Development",
                "Frontend", "Backend", "Database Design", "API Development",
                "Authentication", "Deployment", "DevOps", "Testing", "Performance",
                "Security", "Responsive Design", "Mobile-First", "Progressive Web Apps"
            ],
            "Mobile Developer": [
                "Swift", "Kotlin", "React Native", "Flutter", "Mobile UI/UX", 
                "Git", "APIs", "App Store", "iOS Development", "Android Development",
                "Mobile App Design", "Performance", "Testing", "Debugging",
                "App Store Optimization", "Push Notifications", "Offline Support",
                "Mobile Security", "Cross-Platform Development", "Native Development"
            ],
            "QA Engineer": [
                "Testing Tools", "Python", "Selenium", "JIRA", "Test Automation", 
                "SQL", "API Testing", "Performance Testing", "Manual Testing",
                "Test Planning", "Test Cases", "Bug Tracking", "Regression Testing",
                "User Acceptance Testing", "Load Testing", "Security Testing",
                "Mobile Testing", "Web Testing", "Database Testing", "Test Reports"
            ],
            "Technical Writer": [
                "Technical Writing", "Markdown", "Git", "Documentation Tools", 
                "Subject Matter Expertise", "Editing", "Research", "Content Strategy",
                "Information Architecture", "User Documentation", "API Documentation",
                "User Guides", "Tutorials", "Knowledge Management", "Content Management",
                "Localization", "Translation", "Style Guides", "Documentation Standards"
            ],
            "Data Architect": [
                "Data Modeling", "SQL", "NoSQL", "Data Governance", "ETL", 
                "Data Warehousing", "Cloud Platforms", "Architecture", "Data Strategy",
                "Data Quality", "Data Security", "Data Privacy", "Master Data Management",
                "Data Integration", "Data Migration", "Data Catalog", "Metadata Management",
                "Data Lineage", "Data Architecture Patterns", "Enterprise Architecture"
            ],
            "MLOps Engineer": [
                "Machine Learning", "Docker", "Kubernetes", "CI/CD", "Monitoring", 
                "Python", "MLOps Tools", "Cloud Platforms", "Model Deployment",
                "Model Versioning", "Model Monitoring", "A/B Testing", "Feature Stores",
                "Data Pipelines", "ML Infrastructure", "Model Registry", "MLOps Best Practices",
                "Performance Monitoring", "Alerting", "Incident Response", "Automation"
            ]
        }
        
        # Define skill categories and their weights
        skill_categories = {
            "core": 1.0,           # Core skills (highest weight)
            "intermediate": 0.7,    # Intermediate skills (medium weight)  
            "supporting": 0.4,      # Supporting tools (lower weight)
            "soft": 0.6             # Soft skills (moderate weight)
        }
        
        # Categorize skills by importance
        skill_category_mapping = {
            # Core Skills (High Weight)
            "Python": "core", "SQL": "core", "Machine Learning": "core", "Deep Learning": "core",
            "Statistics": "core", "Data Science": "core", "Java": "core", "JavaScript": "core",
            "Data Modeling": "core", "ETL": "core", "Data Architecture": "core", "MLOps": "core",
            "Computer Vision": "core", "NLP": "core", "Neural Networks": "core", "TensorFlow": "core",
            "PyTorch": "core", "Scikit-learn": "core", "Data Engineering": "core", "Big Data": "core",
            
            # Intermediate Skills (Medium Weight)
            "Pandas": "intermediate", "NumPy": "intermediate", "Matplotlib": "intermediate", 
            "Seaborn": "intermediate", "Plotly": "intermediate", "Hadoop": "intermediate",
            "Spark": "intermediate", "Kafka": "intermediate", "Docker": "intermediate",
            "Kubernetes": "intermediate", "AWS": "intermediate", "Azure": "intermediate",
            "React": "intermediate", "Angular": "intermediate", "Node.js": "intermediate",
            "Flask": "intermediate", "Django": "intermediate", "Spring Boot": "intermediate",
            
            # Supporting Tools (Lower Weight)
            "Tableau": "supporting", "Power BI": "supporting", "Excel": "supporting",
            "Jupyter": "supporting", "Git": "supporting", "JIRA": "supporting",
            "Figma": "supporting", "Adobe XD": "supporting", "Selenium": "supporting",
            "Jenkins": "supporting", "Terraform": "supporting", "Ansible": "supporting",
            
            # Soft Skills (Moderate Weight)
            "Communication": "soft", "Problem Solving": "soft", "Teamwork": "soft",
            "Critical Thinking": "soft", "Leadership": "soft", "Adaptability": "soft",
            "Time Management": "soft", "Creativity": "soft", "Analytical Thinking": "soft",
            "Project Management": "soft", "Stakeholder Management": "soft", "Mentoring": "soft"
        }
        
        # Add soft skills to the skills list
        soft_skills = [
            "Communication", "Problem Solving", "Teamwork", "Critical Thinking", 
            "Leadership", "Adaptability", "Time Management", "Creativity", 
            "Analytical Thinking", "Project Management", "Stakeholder Management", 
            "Mentoring", "Negotiation", "Presentation Skills", "Active Listening",
            "Conflict Resolution", "Strategic Thinking", "Innovation", "Collaboration"
        ]
        self.skills.extend(soft_skills)
        
        difficulty_levels = ["Beginner", "Intermediate", "Advanced"]
        
        for career in self.careers:
            if career in career_skill_mapping:
                skills = career_skill_mapping[career]
                for skill in skills:
                    if skill in self.skills:
                        # Determine skill category and weight
                        category = skill_category_mapping.get(skill, "intermediate")
                        weight = skill_categories[category]
                        
                        # Adjust importance based on category
                        base_importance = random.randint(7, 10)
                        weighted_importance = int(base_importance * weight)
                        
                        data.append({
                            "career": career,
                            "skill": skill,
                            "difficulty": random.choice(difficulty_levels),
                            "importance": weighted_importance,
                            "is_required": random.choice([True, False]),
                            "category": category,
                            "weight": weight
                        })
        
        return pd.DataFrame(data)
    
    def generate_salary_demand_data(self) -> pd.DataFrame:
        """Generate salary and demand data for careers"""
        data = []
        
        for career in self.careers:
            # Generate realistic salary ranges based on career type
            if "Data" in career or "ML" in career or "AI" in career:
                base_salary = random.randint(80000, 150000)
            elif "Engineer" in career or "Developer" in career:
                base_salary = random.randint(70000, 130000)
            elif "Manager" in career or "Architect" in career:
                base_salary = random.randint(90000, 160000)
            else:
                base_salary = random.randint(60000, 110000)
            
            # Add some variation
            min_salary = int(base_salary * 0.8)
            max_salary = int(base_salary * 1.3)
            
            # Generate demand index (0-100)
            demand_index = random.randint(60, 95)
            
            # Select top hiring countries
            top_countries = random.sample(self.countries, random.randint(3, 6))
            
            data.append({
                "career": career,
                "min_salary": min_salary,
                "max_salary": max_salary,
                "avg_salary": base_salary,
                "demand_index": demand_index,
                "top_countries": ", ".join(top_countries),
                "growth_rate": random.randint(5, 25),
                "remote_friendly": random.choice([True, False])
            })
        
        return pd.DataFrame(data)
    
    def generate_courses_data(self) -> pd.DataFrame:
        """Generate synthetic online courses data"""
        data = []
        
        course_templates = [
            "Complete {skill} Course for {level}",
            "{skill} Masterclass: From {level} to Advanced",
            "Learn {skill} - {level} Tutorial",
            "{skill} Fundamentals for {level}",
            "Advanced {skill} Techniques",
            "{skill} Bootcamp: {level} Edition"
        ]
        
        levels = ["Beginner", "Intermediate", "Advanced"]
        
        for skill in self.skills[:30]:  # Limit to first 30 skills for variety
            for level in levels:
                for _ in range(random.randint(1, 3)):  # 1-3 courses per skill-level combination
                    course_title = random.choice(course_templates).format(skill=skill, level=level)
                    
                    # Generate realistic course data
                    duration_hours = random.randint(2, 20)
                    rating = round(random.uniform(3.5, 5.0), 1)
                    price = random.choice([0, 9.99, 19.99, 29.99, 49.99, 99.99])
                    
                    data.append({
                        "title": course_title,
                        "skill": skill,
                        "level": level,
                        "platform": random.choice(self.platforms),
                        "duration_hours": duration_hours,
                        "rating": rating,
                        "price": price,
                        "students_enrolled": random.randint(100, 50000),
                        "instructor": f"Dr. {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller'])}",
                        "last_updated": f"2024-{random.randint(1, 12):02d}",
                        "certificate": random.choice([True, False]),
                        "url": f"https://example.com/courses/{skill.lower().replace(' ', '-')}-{level.lower()}"
                    })
        
        return pd.DataFrame(data)
    
    def generate_job_posts_data(self) -> pd.DataFrame:
        """Generate synthetic job postings data"""
        data = []
        
        companies = [
            "TechCorp", "DataFlow Inc", "InnovateTech", "FutureSystems", "CloudWorks",
            "AILabs", "Digital Solutions", "TechStart", "Enterprise Corp", "StartupXYZ",
            "BigTech Company", "Innovation Hub", "Tech Giants", "Digital Future", "Smart Solutions"
        ]
        
        job_titles = [
            "Senior {career}", "Junior {career}", "{career} Lead", "Principal {career}",
            "Staff {career}", "Associate {career}", "Senior {career} II", "{career} Manager"
        ]
        
        for career in self.careers:
            for _ in range(random.randint(3, 8)):  # 3-8 jobs per career
                job_title = random.choice(job_titles).format(career=career)
                company = random.choice(companies)
                
                # Generate location
                location = random.choice(self.countries)
                
                # Generate salary range
                base_salary = random.randint(60000, 150000)
                min_salary = int(base_salary * 0.8)
                max_salary = int(base_salary * 1.2)
                
                # Generate required skills
                required_skills = random.sample(self.skills[:20], random.randint(3, 6))
                
                data.append({
                    "job_id": f"JOB_{random.randint(1000, 9999)}",
                    "title": job_title,
                    "company": company,
                    "location": location,
                    "min_salary": min_salary,
                    "max_salary": max_salary,
                    "required_skills": ", ".join(required_skills),
                    "experience_level": random.choice(["Entry", "Mid", "Senior", "Lead"]),
                    "job_type": random.choice(["Full-time", "Contract", "Part-time", "Remote"]),
                    "posted_date": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                    "application_deadline": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                    "url": f"https://example.com/jobs/{random.randint(1000, 9999)}"
                })
        
        return pd.DataFrame(data)
    
    def generate_peer_profiles_data(self) -> pd.DataFrame:
        """Generate synthetic peer profiles for benchmarking"""
        data = []
        
        for career in self.careers:
            for _ in range(random.randint(5, 15)):  # 5-15 peers per career
                # Generate skills for this peer
                num_skills = random.randint(5, 12)
                peer_skills = random.sample(self.skills, num_skills)
                
                # Generate experience level
                experience_years = random.randint(1, 15)
                
                # Generate education
                education = random.choice(["Bachelor's", "Master's", "PhD", "Bootcamp", "Self-taught"])
                
                # Generate location
                location = random.choice(self.countries)
                
                # Generate salary (within career range)
                base_salary = random.randint(50000, 120000)
                
                data.append({
                    "profile_id": f"PROF_{random.randint(1000, 9999)}",
                    "career": career,
                    "skills": ", ".join(peer_skills),
                    "experience_years": experience_years,
                    "education": education,
                    "location": location,
                    "salary": base_salary,
                    "company_size": random.choice(["Startup", "Mid-size", "Enterprise", "FAANG"]),
                    "certifications": random.randint(0, 5),
                    "projects_completed": random.randint(1, 20),
                    "github_stars": random.randint(0, 100),
                    "linkedin_connections": random.randint(50, 1000)
                })
        
        return pd.DataFrame(data)
    
    def generate_career_keywords_data(self) -> pd.DataFrame:
        """Generate keywords and skill-frequency data for resume analysis"""
        data = []
        
        for career in self.careers:
            # Generate keywords commonly found in resumes for this career
            keywords = []
            
            if "Data" in career:
                keywords.extend(["data analysis", "data visualization", "statistics", "machine learning", "python", "sql"])
            elif "Engineer" in career:
                keywords.extend(["software development", "programming", "algorithms", "data structures", "git", "testing"])
            elif "Designer" in career:
                keywords.extend(["user experience", "user interface", "prototyping", "wireframing", "design systems"])
            elif "Manager" in career:
                keywords.extend(["project management", "team leadership", "stakeholder management", "agile", "scrum"])
            elif "Analyst" in career:
                keywords.extend(["business analysis", "requirements gathering", "process improvement", "data analysis"])
            
            # Add some generic keywords
            keywords.extend(["problem solving", "communication", "collaboration", "time management", "leadership"])
            
            # Generate frequency scores
            for keyword in keywords:
                frequency = random.randint(60, 95)  # 60-95% frequency
                importance = random.randint(7, 10)  # 7-10 importance score
                
                data.append({
                    "career": career,
                    "keyword": keyword,
                    "frequency_percentage": frequency,
                    "importance_score": importance,
                    "category": random.choice(["Technical", "Soft Skills", "Tools", "Methodologies"])
                })
        
        return pd.DataFrame(data)
    
    def generate_qa_dataset(self) -> List[Dict[str, Any]]:
        """Generate Q&A dataset for the chatbot"""
        qa_data = [
            {
                "question": "Which career suits me if I love AI?",
                "answer": "If you're passionate about AI, consider these careers: Data Scientist, Machine Learning Engineer, AI Research Scientist, or MLOps Engineer. These roles involve working with AI algorithms, neural networks, and machine learning models.",
                "category": "Career Guidance",
                "tags": ["AI", "career choice", "machine learning"]
            },
            {
                "question": "How do I start to become a Software Engineer?",
                "answer": "To become a Software Engineer: 1) Learn programming fundamentals (Python/Java), 2) Study data structures and algorithms, 3) Build projects and contribute to open source, 4) Learn version control (Git), 5) Practice coding interviews, 6) Get internships or entry-level positions.",
                "category": "Learning Path",
                "tags": ["software engineering", "learning path", "programming"]
            },
            {
                "question": "What skills do I need for Data Science?",
                "answer": "Essential skills for Data Science: Python, SQL, Statistics, Machine Learning, Data Visualization (Tableau/Power BI), Pandas/NumPy, and domain knowledge. Also important: critical thinking, communication, and business acumen.",
                "category": "Skills",
                "tags": ["data science", "skills", "requirements"]
            },
            {
                "question": "Is a degree necessary for tech careers?",
                "answer": "While a degree can be helpful, many tech careers value skills and experience over formal education. Bootcamps, online courses, and self-study can be effective alternatives. Focus on building a strong portfolio and gaining practical experience.",
                "category": "Education",
                "tags": ["education", "degree", "bootcamp", "self-study"]
            },
            {
                "question": "How much can I earn as a Data Engineer?",
                "answer": "Data Engineer salaries vary by location and experience: Entry-level: $60K-80K, Mid-level: $80K-120K, Senior: $120K-180K+. High demand in tech hubs like San Francisco, New York, and London.",
                "category": "Salary",
                "tags": ["data engineering", "salary", "compensation"]
            },
            {
                "question": "What's the difference between Data Scientist and Data Analyst?",
                "answer": "Data Analysts focus on descriptive analytics, creating reports and dashboards. Data Scientists do predictive analytics, build ML models, and work on complex algorithms. Data Scientists typically need more advanced statistical and programming skills.",
                "category": "Career Comparison",
                "tags": ["data scientist", "data analyst", "differences"]
            },
            {
                "question": "How do I transition from non-tech to tech?",
                "answer": "Transitioning to tech: 1) Identify transferable skills, 2) Learn programming fundamentals, 3) Build projects in your target area, 4) Network with tech professionals, 5) Consider bootcamps or certifications, 6) Start with entry-level positions.",
                "category": "Career Transition",
                "tags": ["career change", "transition", "non-tech to tech"]
            },
            {
                "question": "What programming language should I learn first?",
                "answer": "Python is excellent for beginners due to readable syntax and versatility. It's used in data science, web development, AI, and automation. JavaScript is great if you're interested in web development. Start with one and master the fundamentals.",
                "category": "Programming",
                "tags": ["programming", "python", "javascript", "first language"]
            }
        ]
        
        return qa_data
    
    def generate_all_datasets(self):
        """Generate all datasets and save them"""
        print("Generating synthetic datasets...")
        
        # Create data directory if it doesn't exist
        import os
        os.makedirs("data", exist_ok=True)
        
        # Generate and save all datasets
        datasets = {
            "career_skills": self.generate_career_skills_mapping(),
            "salary_demand": self.generate_salary_demand_data(),
            "courses": self.generate_courses_data(),
            "job_posts": self.generate_job_posts_data(),
            "peer_profiles": self.generate_peer_profiles_data(),
            "career_keywords": self.generate_career_keywords_data()
        }
        
        # Save as CSV
        for name, df in datasets.items():
            csv_path = f"data/{name}.csv"
            df.to_csv(csv_path, index=False)
            print(f"Saved {csv_path} with {len(df)} records")
        
        # Save Q&A dataset as JSON
        qa_data = self.generate_qa_dataset()
        qa_path = "data/qa_dataset.json"
        with open(qa_path, 'w') as f:
            json.dump(qa_data, f, indent=2)
        print(f"Saved {qa_path} with {len(qa_data)} Q&A pairs")
        
        # Create a summary dataset info file
        summary = {
            "total_careers": len(self.careers),
            "total_skills": len(self.skills),
            "datasets_generated": list(datasets.keys()) + ["qa_dataset"],
            "total_records": sum(len(df) for df in datasets.values()) + len(qa_data)
        }
        
        summary_path = "data/dataset_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"Saved {summary_path}")
        
        print("\nAll datasets generated successfully!")
        return datasets

if __name__ == "__main__":
    generator = CareerDataGenerator()
    datasets = generator.generate_all_datasets()
