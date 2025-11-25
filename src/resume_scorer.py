"""
AI-Powered Resume Scorer with Job Description Matching
Advanced NLP-based resume analysis and optimization recommendations
"""

import re
import os
from typing import Dict, List, Any, Tuple
from datetime import datetime

# Handle optional dependencies gracefully
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from docx import Document
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False

class ResumeAnalysisEngine:
    """Advanced resume analysis and scoring engine with job matching capabilities"""
    
    def __init__(self):
        self.skills_database = self._load_skills_database()
        self.action_verbs = self._load_action_verbs()
        
    def _load_skills_database(self) -> Dict[str, List[str]]:
        """Load comprehensive skills database"""
        return {
            "programming_languages": [
                "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
                "php", "ruby", "swift", "kotlin", "scala", "r"
            ],
            "web_technologies": [
                "html", "css", "react", "angular", "vue", "node.js", "express", "django",
                "flask", "spring", "bootstrap", "jquery"
            ],
            "databases": [
                "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "oracle",
                "sqlite", "cassandra", "dynamodb"
            ],
            "cloud_platforms": [
                "aws", "azure", "gcp", "google cloud", "heroku", "kubernetes", "docker"
            ],
            "data_science": [
                "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
                "pandas", "numpy", "matplotlib", "jupyter", "tableau"
            ],
            "soft_skills": [
                "leadership", "communication", "teamwork", "problem solving", "analytical",
                "project management", "agile", "scrum"
            ]
        }
    
    def _load_action_verbs(self) -> Dict[str, List[str]]:
        """Load action verbs categorized by impact level"""
        return {
            "high_impact": [
                "achieved", "accomplished", "delivered", "implemented", "developed", "created",
                "designed", "built", "established", "launched", "led", "managed", "optimized",
                "improved", "increased", "reduced", "streamlined", "transformed"
            ],
            "medium_impact": [
                "assisted", "supported", "contributed", "participated", "collaborated",
                "coordinated", "organized", "maintained", "updated", "enhanced"
            ],
            "low_impact": [
                "responsible for", "duties included", "worked on", "involved in", "helped with"
            ]
        }
    
    def parse_resume_file(self, file_path: str) -> str:
        """Extract text from resume file (PDF or DOCX)"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Resume file not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self._extract_pdf_text(file_path)
        elif file_extension == '.docx':
            return self._extract_docx_text(file_path)
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        if not PDF_SUPPORT:
            raise ImportError("PyPDF2 not available. Install with: pip install PyPDF2")
        
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
        
        return text
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        if not DOCX_SUPPORT:
            raise ImportError("python-docx not available. Install with: pip install python-docx")
        
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise ValueError(f"Error reading DOCX file: {str(e)}")
        
        return text
    
    def analyze_resume(self, resume_text: str, job_description: str = None) -> Dict[str, Any]:
        """Comprehensive resume analysis with optional job description matching"""
        
        cleaned_resume = self._clean_text(resume_text)
        
        analysis_result = {
            'analysis_timestamp': datetime.now().isoformat(),
            'resume_length': len(resume_text),
            'word_count': len(resume_text.split()),
            'section_analysis': self._analyze_sections(cleaned_resume),
            'skills_analysis': self._analyze_skills(cleaned_resume),
            'experience_analysis': self._analyze_experience(cleaned_resume),
            'language_analysis': self._analyze_language_quality(cleaned_resume),
            'overall_score': 0,
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        }
        
        # Job description matching if provided
        if job_description:
            job_match_analysis = self._analyze_job_match(cleaned_resume, job_description)
            analysis_result['job_match_analysis'] = job_match_analysis
        
        # Calculate overall score and generate insights
        analysis_result['overall_score'] = self._calculate_overall_score(analysis_result)
        analysis_result['strengths'], analysis_result['weaknesses'] = self._identify_strengths_weaknesses(analysis_result)
        analysis_result['recommendations'] = self._generate_recommendations(analysis_result)
        analysis_result['ml_features'] = self._extract_resume_ml_features(analysis_result)
        
        return analysis_result
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize resume text"""
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def _analyze_sections(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume sections and structure"""
        sections = {
            'contact_info': any(keyword in resume_text for keyword in ['email', 'phone', '@']),
            'experience': any(keyword in resume_text for keyword in ['experience', 'work', 'employment']),
            'education': any(keyword in resume_text for keyword in ['education', 'degree', 'university']),
            'skills': any(keyword in resume_text for keyword in ['skills', 'technical', 'competencies']),
            'projects': any(keyword in resume_text for keyword in ['projects', 'portfolio'])
        }
        
        section_score = (sum(sections.values()) / len(sections)) * 100
        
        return {
            'sections_present': sections,
            'section_completeness_score': round(section_score, 2),
            'missing_sections': [section for section, present in sections.items() if not present]
        }
    
    def _analyze_skills(self, resume_text: str) -> Dict[str, Any]:
        """Analyze technical and soft skills mentioned in resume"""
        skills_found = {}
        total_skills_count = 0
        
        for category, skills_list in self.skills_database.items():
            found_skills = [skill for skill in skills_list if skill in resume_text]
            skills_found[category] = {
                'skills': found_skills,
                'count': len(found_skills)
            }
            total_skills_count += len(found_skills)
        
        categories_with_skills = sum(1 for category in skills_found.values() if category['count'] > 0)
        skills_diversity_score = (categories_with_skills / len(self.skills_database)) * 100
        
        return {
            'skills_by_category': skills_found,
            'total_skills_mentioned': total_skills_count,
            'skills_diversity_score': round(skills_diversity_score, 2),
            'strongest_skill_areas': [cat for cat, data in skills_found.items() if data['count'] >= 3][:3]
        }
    
    def _analyze_experience(self, resume_text: str) -> Dict[str, Any]:
        """Analyze work experience quality and presentation"""
        
        # Count action verbs by impact level
        action_verb_analysis = {}
        for impact_level, verbs in self.action_verbs.items():
            count = sum(1 for verb in verbs if verb in resume_text)
            action_verb_analysis[impact_level] = count
        
        total_action_verbs = sum(action_verb_analysis.values())
        high_impact_ratio = action_verb_analysis['high_impact'] / max(1, total_action_verbs)
        action_verb_score = high_impact_ratio * 100
        
        # Look for quantified achievements
        numbers_pattern = r'\d+(\.\d+)?%?'
        quantified_achievements = len(re.findall(numbers_pattern, resume_text))
        
        # Estimate years of experience
        years_pattern = r'(\d+)\s*(years?|yrs?)'
        years_matches = re.findall(years_pattern, resume_text)
        estimated_years = max([int(match[0]) for match in years_matches], default=0)
        
        experience_score = (
            action_verb_score * 0.4 +
            min(quantified_achievements * 10, 50) * 0.3 +
            min(estimated_years * 10, 50) * 0.3
        )
        
        return {
            'action_verb_analysis': action_verb_analysis,
            'action_verb_score': round(action_verb_score, 2),
            'quantified_achievements_count': quantified_achievements,
            'estimated_years_experience': estimated_years,
            'experience_quality_score': round(experience_score, 2)
        }
    
    def _analyze_language_quality(self, resume_text: str) -> Dict[str, Any]:
        """Analyze language quality and readability"""
        
        sentences = resume_text.split('.')
        avg_sentence_length = sum(len(sentence.split()) for sentence in sentences) / max(len(sentences), 1)
        
        # Simple language quality assessment
        language_score = max(0, 100 - max(0, (avg_sentence_length - 20) * 2))
        
        return {
            'average_sentence_length': round(avg_sentence_length, 2),
            'language_quality_score': round(language_score, 2),
            'readability_assessment': 'Good' if language_score >= 80 else 'Needs Improvement'
        }
    
    def _analyze_job_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze how well resume matches job description"""
        
        job_desc_cleaned = self._clean_text(job_description)
        
        # Extract skills from both texts
        job_skills = self._extract_skills_from_text(job_desc_cleaned)
        resume_skills = self._extract_skills_from_text(resume_text)
        
        # Calculate skill alignment
        total_job_skills = sum(len(skills) for skills in job_skills.values())
        total_matching_skills = 0
        
        for category, job_category_skills in job_skills.items():
            resume_category_skills = resume_skills.get(category, [])
            matching_skills = set(job_category_skills) & set(resume_category_skills)
            total_matching_skills += len(matching_skills)
        
        match_percentage = (total_matching_skills / max(total_job_skills, 1)) * 100
        
        # Identify missing keywords
        all_job_keywords = []
        for skills in job_skills.values():
            all_job_keywords.extend(skills)
        
        missing_keywords = [keyword for keyword in all_job_keywords if keyword not in resume_text]
        
        return {
            'keyword_match_percentage': round(match_percentage, 2),
            'matching_skills_count': total_matching_skills,
            'total_job_skills': total_job_skills,
            'missing_keywords': missing_keywords[:10],
            'overall_job_match_score': round(match_percentage, 2),
            'recommendations_for_improvement': self._generate_job_match_recommendations(missing_keywords)
        }
    
    def _extract_skills_from_text(self, text: str) -> Dict[str, List[str]]:
        """Extract skills from any text"""
        skills_found = {}
        
        for category, skills_list in self.skills_database.items():
            found_skills = [skill for skill in skills_list if skill in text]
            skills_found[category] = found_skills
        
        return skills_found
    
    def _calculate_overall_score(self, analysis_result: Dict) -> float:
        """Calculate weighted overall resume score"""
        
        weights = {
            'section_completeness_score': 0.2,
            'skills_diversity_score': 0.3,
            'experience_quality_score': 0.3,
            'language_quality_score': 0.2
        }
        
        total_score = 0
        for component, weight in weights.items():
            if component == 'section_completeness_score':
                score = analysis_result.get('section_analysis', {}).get('section_completeness_score', 0)
            elif component == 'skills_diversity_score':
                score = analysis_result.get('skills_analysis', {}).get('skills_diversity_score', 0)
            elif component == 'experience_quality_score':
                score = analysis_result.get('experience_analysis', {}).get('experience_quality_score', 0)
            elif component == 'language_quality_score':
                score = analysis_result.get('language_analysis', {}).get('language_quality_score', 0)
            else:
                score = 0
            
            total_score += score * weight
        
        return round(total_score, 2)
    
    def _identify_strengths_weaknesses(self, analysis_result: Dict) -> Tuple[List[str], List[str]]:
        """Identify resume strengths and weaknesses"""
        strengths = []
        weaknesses = []
        
        # Skills analysis
        if analysis_result.get('skills_analysis', {}).get('total_skills_mentioned', 0) >= 10:
            strengths.append("Strong technical skills portfolio")
        elif analysis_result.get('skills_analysis', {}).get('total_skills_mentioned', 0) < 5:
            weaknesses.append("Limited technical skills mentioned")
        
        # Experience analysis
        if analysis_result.get('experience_analysis', {}).get('quantified_achievements_count', 0) >= 3:
            strengths.append("Good use of quantified achievements")
        else:
            weaknesses.append("Lack of quantified achievements")
        
        # Section completeness
        if analysis_result.get('section_analysis', {}).get('section_completeness_score', 0) >= 80:
            strengths.append("Well-structured resume with essential sections")
        else:
            weaknesses.append("Missing important resume sections")
        
        return strengths, weaknesses
    
    def _generate_recommendations(self, analysis_result: Dict) -> List[Dict[str, str]]:
        """Generate specific improvement recommendations"""
        recommendations = []
        
        # Section-based recommendations
        missing_sections = analysis_result.get('section_analysis', {}).get('missing_sections', [])
        for section in missing_sections:
            if section == 'skills':
                recommendations.append({
                    'area': 'Technical Skills',
                    'recommendation': 'Add a dedicated Skills section with relevant technologies',
                    'priority': 'critical'
                })
            elif section == 'projects':
                recommendations.append({
                    'area': 'Content Structure',
                    'recommendation': 'Add a Projects section showcasing your work',
                    'priority': 'high'
                })
        
        # Experience recommendations
        if analysis_result.get('experience_analysis', {}).get('action_verb_score', 0) < 50:
            recommendations.append({
                'area': 'Experience Description',
                'recommendation': 'Use more impactful action verbs (achieved, implemented, optimized)',
                'priority': 'medium'
            })
        
        return recommendations
    
    def _generate_job_match_recommendations(self, missing_keywords: List[str]) -> List[Dict[str, str]]:
        """Generate recommendations for improving job match"""
        recommendations = []
        
        if missing_keywords:
            top_missing = missing_keywords[:5]
            recommendations.append({
                'area': 'Keyword Optimization',
                'recommendation': f"Consider adding these job-relevant keywords: {', '.join(top_missing)}",
                'priority': 'high'
            })
        
        return recommendations
    
    def _extract_resume_ml_features(self, analysis_result: Dict) -> Dict[str, float]:
        """Extract features for ML model integration"""
        return {
            'resume_overall_score': analysis_result.get('overall_score', 0),
            'resume_skills_diversity': analysis_result.get('skills_analysis', {}).get('skills_diversity_score', 0),
            'resume_experience_quality': analysis_result.get('experience_analysis', {}).get('experience_quality_score', 0),
            'resume_language_quality': analysis_result.get('language_analysis', {}).get('language_quality_score', 0),
            'resume_total_skills_count': analysis_result.get('skills_analysis', {}).get('total_skills_mentioned', 0),
            'resume_quantified_achievements': analysis_result.get('experience_analysis', {}).get('quantified_achievements_count', 0),
            'resume_years_experience': analysis_result.get('experience_analysis', {}).get('estimated_years_experience', 0)
        }

def main():
    """Test the resume analysis engine"""
    print("📄 Testing Resume Analysis Engine")
    print("=" * 50)
    
    engine = ResumeAnalysisEngine()
    
    # Test with sample resume text
    sample_resume = """
    John Smith
    Email: john.smith@email.com | Phone: (555) 123-4567
    
    EXPERIENCE
    Software Developer at Tech Corp (2022-2024)
    • Developed and implemented 5 web applications using React and Node.js
    • Optimized database queries resulting in 30% performance improvement  
    • Led a team of 3 developers on critical project delivery
    • Collaborated with cross-functional teams to deliver features
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology (2018-2022)
    CGPA: 8.5/10
    
    SKILLS
    Programming Languages: Python, JavaScript, Java, C++
    Web Technologies: React, Node.js, HTML, CSS
    Databases: MySQL, MongoDB
    Tools: Git, Docker, AWS
    
    PROJECTS
    E-commerce Platform: Built full-stack application with 10,000+ users
    Data Analysis Tool: Created Python tool for processing large datasets
    """
    
    # Test basic analysis
    result = engine.analyze_resume(sample_resume)
    
    print(f"Analysis Results:")
    print(f"Overall Score: {result['overall_score']:.1f}/100")
    print(f"Skills Found: {result['skills_analysis']['total_skills_mentioned']}")
    print(f"Section Completeness: {result['section_analysis']['section_completeness_score']:.1f}%")
    
    print(f"\nStrengths:")
    for strength in result['strengths']:
        print(f"  • {strength}")
    
    print(f"\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  • {rec['area']}: {rec['recommendation']}")
    
    # Test job matching
    job_description = """
    We are looking for a Senior Python Developer with experience in:
    - Python programming (3+ years)
    - Flask or Django frameworks  
    - PostgreSQL database
    - AWS cloud services
    - Machine learning libraries
    - Agile development methodologies
    """
    
    job_match_result = engine.analyze_resume(sample_resume, job_description)
    
    print(f"\nJob Match Analysis:")
    print(f"Match Score: {job_match_result['job_match_analysis']['overall_job_match_score']:.1f}%")
    print(f"Missing Keywords: {job_match_result['job_match_analysis']['missing_keywords'][:3]}")
    
    print("\n✅ Resume Analysis Engine test completed!")

if __name__ == "__main__":
    main()