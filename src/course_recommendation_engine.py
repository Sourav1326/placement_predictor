"""
Intelligent Course Recommendation Engine
Provides personalized course suggestions from multiple platforms
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Course:
    title: str
    platform: str
    instructor: str
    duration: str
    level: str
    price: str
    rating: float
    url: str
    description: str
    skills_covered: List[str]

class CourseRecommendationEngine:
    def __init__(self):
        self.course_database = self._initialize_courses()
        self.company_requirements = self._initialize_company_requirements()
    
    def _initialize_courses(self) -> Dict:
        """Initialize course database"""
        return {
            'python': {
                'beginner': [
                    Course("Python for Everybody", "Coursera", "Charles Severance", "8 months", 
                          "beginner", "$49/month", 4.8, "https://coursera.org/specializations/python",
                          "Learn Python fundamentals", ["Python basics", "Data structures"]),
                    Course("Complete Python Bootcamp", "Udemy", "Jose Portilla", "22 hours",
                          "beginner", "$84.99", 4.6, "https://udemy.com/course/complete-python-bootcamp",
                          "Python from zero to hero", ["Python fundamentals", "OOP"])
                ],
                'intermediate': [
                    Course("Python for Data Science", "Udemy", "Jose Portilla", "25 hours",
                          "intermediate", "$94.99", 4.6, "https://udemy.com/course/python-for-data-science",
                          "Python for data analysis", ["NumPy", "Pandas", "Machine Learning"]),
                    Course("Django Web Development", "Coursera", "University of Michigan", "4 months",
                          "intermediate", "$49/month", 4.7, "https://coursera.org/specializations/django",
                          "Build web apps with Django", ["Django", "Web development"])
                ]
            },
            'java': {
                'beginner': [
                    Course("Java Programming Masterclass", "Udemy", "Tim Buchalka", "80 hours",
                          "beginner", "$94.99", 4.6, "https://udemy.com/course/java-complete",
                          "Complete Java course", ["Java basics", "OOP", "Collections"]),
                    Course("Java Programming Fundamentals", "Coursera", "Duke University", "5 months",
                          "beginner", "$49/month", 4.6, "https://coursera.org/specializations/java",
                          "Java and software engineering", ["Java fundamentals", "Problem solving"])
                ],
                'intermediate': [
                    Course("Spring Boot Microservices", "Udemy", "In28Minutes", "17 hours",
                          "intermediate", "$84.99", 4.5, "https://udemy.com/course/microservices-spring",
                          "Build microservices", ["Spring Boot", "Microservices", "REST APIs"])
                ]
            },
            'javascript': {
                'beginner': [
                    Course("Complete JavaScript Course", "Udemy", "Jonas Schmedtmann", "69 hours",
                          "beginner", "$94.99", 4.7, "https://udemy.com/course/complete-javascript",
                          "Modern JavaScript", ["JavaScript fundamentals", "ES6+", "DOM"]),
                    Course("JavaScript Algorithms", "freeCodeCamp", "freeCodeCamp", "300 hours",
                          "beginner", "Free", 4.8, "https://freecodecamp.org/learn/javascript",
                          "Learn JS through coding", ["JavaScript basics", "Algorithms"])
                ],
                'intermediate': [
                    Course("React Complete Guide", "Udemy", "Maximilian Schwarzmüller", "48 hours",
                          "intermediate", "$94.99", 4.6, "https://udemy.com/course/react-complete",
                          "Build modern web apps", ["React", "Redux", "Hooks"])
                ]
            },
            'data_science': [
                Course("IBM Data Science Certificate", "Coursera", "IBM", "11 months",
                      "beginner", "$49/month", 4.6, "https://coursera.org/professional-certificates/ibm-data-science",
                      "Complete data science program", ["Python", "SQL", "Machine learning"]),
                Course("Machine Learning A-Z", "Udemy", "Kirill Eremenko", "44 hours",
                      "intermediate", "$94.99", 4.5, "https://udemy.com/course/machinelearning",
                      "Hands-on ML", ["Machine Learning", "Python", "Deep Learning"])
            ],
            'competitive_programming': [
                Course("Algorithms Specialization", "Coursera", "Stanford", "4 months",
                      "intermediate", "$49/month", 4.9, "https://coursera.org/specializations/algorithms",
                      "Comprehensive algorithms", ["Algorithms", "Data structures", "Graph algorithms"]),
                Course("LeetCode Patterns", "Educative", "Educative", "self-paced",
                      "intermediate", "$79", 4.7, "https://educative.io/courses/grokking-coding-interview",
                      "Coding interview prep", ["Problem patterns", "Algorithm design"])
            ]
        }
    
    def _initialize_company_requirements(self) -> Dict:
        """Company skill requirements"""
        return {
            'FAANG': {
                'required_skills': ['Algorithms', 'System design', 'Data structures'],
                'preferred_languages': ['Python', 'Java', 'C++'],
                'min_leetcode_score': 1800,
                'min_projects': 3
            },
            'product_companies': {
                'required_skills': ['Full-stack', 'API design', 'Databases'],
                'preferred_languages': ['JavaScript', 'Python', 'Java'],
                'min_leetcode_score': 1200,
                'min_projects': 2
            },
            'startups': {
                'required_skills': ['Rapid prototyping', 'Full-stack', 'Adaptability'],
                'preferred_languages': ['Python', 'JavaScript', 'Go'],
                'min_leetcode_score': 800,
                'min_projects': 3
            }
        }
    
    def recommend_courses_for_student(self, student_profile: Dict, target_companies: List[str] = None) -> Dict:
        """Generate personalized course recommendations"""
        recommendations = {
            'immediate_priorities': [],
            'skill_gap_courses': [],
            'company_specific': {},
            'free_alternatives': []
        }
        
        # Analyze skill gaps
        skill_gaps = self._identify_skill_gaps(student_profile, target_companies)
        
        # Get course recommendations for each gap
        for gap in skill_gaps:
            gap_courses = self._find_courses_for_skill_gap(gap)
            recommendations['skill_gap_courses'].extend(gap_courses)
        
        # Immediate priorities (top 3 most important)
        recommendations['immediate_priorities'] = recommendations['skill_gap_courses'][:3]
        
        # Company-specific recommendations
        if target_companies:
            for company_type in target_companies:
                if company_type in self.company_requirements:
                    company_courses = self._get_company_courses(company_type, student_profile)
                    recommendations['company_specific'][company_type] = company_courses
        
        # Free alternatives
        recommendations['free_alternatives'] = self._get_free_courses()
        
        return recommendations
    
    def _identify_skill_gaps(self, student_profile: Dict, target_companies: List[str] = None) -> List[str]:
        """Identify skill gaps based on profile"""
        gaps = []
        
        # Check basic requirements
        if student_profile.get('num_projects', 0) < 2:
            gaps.append('project_development')
        
        if student_profile.get('leetcode_score', 0) < 1000:
            gaps.append('competitive_programming')
        
        if student_profile.get('num_internships', 0) == 0:
            gaps.append('practical_experience')
        
        # Language-specific gaps
        languages = student_profile.get('programming_languages', '').lower()
        if 'python' in languages:
            gaps.append('python_advanced')
        if 'java' in languages:
            gaps.append('java_frameworks')
        if 'javascript' in languages:
            gaps.append('javascript_frameworks')
        
        # Company-specific gaps
        if target_companies:
            for company in target_companies:
                if company in self.company_requirements:
                    req = self.company_requirements[company]
                    if student_profile.get('leetcode_score', 0) < req['min_leetcode_score']:
                        gaps.append('algorithms_for_interviews')
        
        return gaps
    
    def _find_courses_for_skill_gap(self, gap: str) -> List[Course]:
        """Find courses for specific skill gap"""
        if gap == 'python_advanced' and 'python' in self.course_database:
            return self.course_database['python']['intermediate']
        elif gap == 'java_frameworks' and 'java' in self.course_database:
            return self.course_database['java']['intermediate']
        elif gap == 'javascript_frameworks' and 'javascript' in self.course_database:
            return self.course_database['javascript']['intermediate']
        elif gap in ['competitive_programming', 'algorithms_for_interviews']:
            return self.course_database.get('competitive_programming', [])
        elif gap == 'project_development':
            return self.course_database.get('data_science', [])[:1]  # Practical courses
        else:
            return []
    
    def _get_company_courses(self, company_type: str, student_profile: Dict) -> List[Course]:
        """Get courses specific to company requirements"""
        courses = []
        req = self.company_requirements[company_type]
        
        # Add algorithm courses for high LeetCode requirements
        if student_profile.get('leetcode_score', 0) < req['min_leetcode_score']:
            courses.extend(self.course_database.get('competitive_programming', []))
        
        # Add language-specific courses
        for lang in req['preferred_languages']:
            lang_lower = lang.lower()
            if lang_lower in self.course_database:
                courses.extend(self.course_database[lang_lower].get('intermediate', []))
        
        return courses[:3]  # Limit to top 3
    
    def _get_free_courses(self) -> List[Course]:
        """Get free course alternatives"""
        free_courses = []
        
        # Find all free courses in database
        for category in self.course_database:
            if isinstance(self.course_database[category], dict):
                for level in self.course_database[category]:
                    for course in self.course_database[category][level]:
                        if 'free' in course.price.lower():
                            free_courses.append(course)
            elif isinstance(self.course_database[category], list):
                for course in self.course_database[category]:
                    if 'free' in course.price.lower():
                        free_courses.append(course)
        
        # Add additional free resources
        free_courses.extend([
            Course("FreeCodeCamp Complete", "freeCodeCamp", "freeCodeCamp", "600+ hours",
                  "beginner", "Free", 4.8, "https://freecodecamp.org",
                  "Complete web development", ["HTML", "CSS", "JavaScript", "React"]),
            Course("MIT CS Course", "MIT OCW", "MIT", "semester", "beginner", "Free", 4.9,
                  "https://ocw.mit.edu", "Computer science fundamentals", ["Programming", "Algorithms"])
        ])
        
        return free_courses

def test_course_recommendations():
    """Test the course recommendation system"""
    print("🎓 Course Recommendation Engine Test")
    print("=" * 40)
    
    engine = CourseRecommendationEngine()
    
    # Sample student with low placement probability
    student = {
        'programming_languages': 'Python, Java',
        'num_projects': 1,
        'num_internships': 0,
        'leetcode_score': 600,
        'cgpa': 7.2
    }
    
    recommendations = engine.recommend_courses_for_student(
        student, 
        target_companies=['FAANG', 'product_companies']
    )
    
    print(f"📚 Immediate Priorities ({len(recommendations['immediate_priorities'])}):")
    for course in recommendations['immediate_priorities']:
        print(f"  - {course.title} ({course.platform}) - {course.price}")
    
    print(f"\n🏢 Company-Specific Recommendations:")
    for company, courses in recommendations['company_specific'].items():
        print(f"  {company}: {len(courses)} courses")
    
    print(f"\n🆓 Free Alternatives: {len(recommendations['free_alternatives'])}")
    for course in recommendations['free_alternatives'][:3]:
        print(f"  - {course.title} ({course.platform})")

if __name__ == "__main__":
    test_course_recommendations()